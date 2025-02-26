import grpc
import bank_pb2
import bank_pb2_grpc


def create_account(stub, account_id, account_type):
    response = stub.CreateAccount(bank_pb2.AccountRequest(account_id=account_id, account_type=account_type))
    print(f"Create Account: {response.message}")


def get_balance(stub, account_id):
    try:
        response = stub.GetBalance(bank_pb2.AccountRequest(account_id=account_id))
        print(f"Balance: {response.balance}")
    except grpc.RpcError as e:
        print(f"Error: {e.details()}")


def deposit(stub, account_id, amount):
    try:
        response = stub.Deposit(bank_pb2.DepositRequest(account_id=account_id, amount=amount))
        print(f"Deposit: {response.message}, New Balance: {response.balance}")
    except grpc.RpcError as e:
        print(f"Error: {e.details()}")


def withdraw(stub, account_id, amount):
    try:
        response = stub.Withdraw(bank_pb2.WithdrawRequest(account_id=account_id, amount=amount))
        print(f"Withdraw: {response.message}, New Balance: {response.balance}")
    except grpc.RpcError as e:
        print(f"Error: {e.details()}")


def calculate_interest(stub, account_id, annual_interest_rate):
    try:
        response = stub.CalculateInterest(
            bank_pb2.InterestRequest(account_id=account_id, annual_interest_rate=annual_interest_rate))
        print(f"Interest: {response.message}, New Balance: {response.balance}")
    except grpc.RpcError as e:
        print(f"Error: {e.details()}")


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = bank_pb2_grpc.BankServiceStub(channel)

    # Sample operations
    create_account(stub, "123", "savings")
    deposit(stub, "123", 500)
    get_balance(stub, "123")
    withdraw(stub, "123", 316)
    calculate_interest(stub, "123", 5)
    get_balance(stub, "123")


if __name__ == "__main__":
    run()
