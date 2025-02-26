import grpc
import bank_pb2
import bank_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = bank_pb2_grpc.BankServiceStub(channel)

    # Create an account
    response = stub.CreateAccount(bank_pb2.AccountRequest(account_id="124", account_type="savings"))
    print(f"CreateAccount: {response.message}")

    # Deposit money
    response = stub.Deposit(bank_pb2.DepositRequest(account_id="123", amount=1000))
    print(f"Deposit: {response.message}, New Balance: {response.balance}")

    # Get balance
    response = stub.GetBalance(bank_pb2.AccountRequest(account_id="123"))
    print(f"Balance: {response.balance}")

    # Withdraw money
    response = stub.Withdraw(bank_pb2.WithdrawRequest(account_id="123", amount=200))
    print(f"Withdraw: {response.message}, New Balance: {response.balance}")

    # Calculate interest
    response = stub.CalculateInterest(bank_pb2.InterestRequest(account_id="123", annual_interest_rate=5))
    print(f"Interest Applied: {response.message}, New Balance: {response.balance}")

if __name__ == "__main__":
    run()
