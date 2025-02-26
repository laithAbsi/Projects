import time
import grpc
from concurrent import futures
import redis
import threading
import bank_pb2
import bank_pb2_grpc

# Initialize Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
lock = threading.Lock()


class BankService(bank_pb2_grpc.BankServiceServicer):
    def CreateAccount(self, request, context):
        with lock:
            if redis_client.exists(request.account_id):
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details("Account already exists.")
                return bank_pb2.AccountResponse(account_id=request.account_id, message="Account already exists.")

            account_data = {"account_type": request.account_type, "balance": "0.0"}
            redis_client.hset(request.account_id, account_data)
            return bank_pb2.AccountResponse(account_id=request.account_id, message="Account created successfully.")

    def GetBalance(self, request, context):
        if not redis_client.exists(request.account_id):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Account not found. Please check the account ID.")
            return bank_pb2.BalanceResponse(account_id=request.account_id, balance=0.0, message="Account not found.")

        balance = float(redis_client.hget(request.account_id, "balance"))
        return bank_pb2.BalanceResponse(account_id=request.account_id, balance=balance,
                                        message="Balance retrieved successfully.")

    def Deposit(self, request, context):
        if request.amount <= 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Transaction amount must be positive.")
            return bank_pb2.TransactionResponse(account_id=request.account_id, balance=0.0,
                                                message="Invalid deposit amount.")

        with lock:
            if not redis_client.exists(request.account_id):
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Account not found. Please check the account ID.")
                return bank_pb2.TransactionResponse(account_id=request.account_id, balance=0.0,
                                                    message="Account not found.")

            balance = float(redis_client.hget(request.account_id, "balance"))
            balance += request.amount
            redis_client.hset(request.account_id, "balance", balance)
            return bank_pb2.TransactionResponse(account_id=request.account_id, balance=balance,
                                                message="Deposit successful.")

    def Withdraw(self, request, context):
        if request.amount <= 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Transaction amount must be positive.")
            return bank_pb2.TransactionResponse(account_id=request.account_id, balance=0.0,
                                                message="Invalid withdrawal amount.")

        with lock:
            if not redis_client.exists(request.account_id):
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Account not found. Please check the account ID.")
                return bank_pb2.TransactionResponse(account_id=request.account_id, balance=0.0,
                                                    message="Account not found.")

            balance = float(redis_client.hget(request.account_id, "balance"))
            if balance < request.amount:
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
                context.set_details("Insufficient funds for the requested withdrawal.")
                return bank_pb2.TransactionResponse(account_id=request.account_id, balance=balance,
                                                    message="Insufficient funds.")

            balance -= request.amount
            redis_client.hset(request.account_id, "balance", balance)
            return bank_pb2.TransactionResponse(account_id=request.account_id, balance=balance,
                                                message="Withdrawal successful.")

    def CalculateInterest(self, request, context):
        if request.annual_interest_rate <= 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Annual interest rate must be a positive value.")
            return bank_pb2.TransactionResponse(account_id=request.account_id, balance=0.0,
                                                message="Invalid interest rate.")

        with lock:
            if not redis_client.exists(request.account_id):
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Account not found. Please check the account ID.")
                return bank_pb2.TransactionResponse(account_id=request.account_id, balance=0.0,
                                                    message="Account not found.")

            balance = float(redis_client.hget(request.account_id, "balance"))
            interest = balance * (request.annual_interest_rate / 100)
            balance += interest
            redis_client.hset(request.account_id, "balance", balance)
            return bank_pb2.TransactionResponse(account_id=request.account_id, balance=balance,
                                                message="Interest applied successfully.")


# Start the gRPC server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bank_pb2_grpc.add_BankServiceServicer_to_server(BankService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("BankService gRPC Server started at port 50051")
    try:
        while True:
            time.sleep(86400)  # Keep server running
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
