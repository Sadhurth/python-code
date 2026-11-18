# Custom Exception
class InsufficientFundsError(Exception):
    """Raised when a withdrawal is not allowed due to low balance."""
    pass

# TASK 1: Bank Account Class

class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"{self.owner} deposited {amount} -> balance {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(
                f"Insufficient funds: balance {self.balance}, requested {amount}"
            )
        self.balance -= amount
        print(f"{self.owner} withdrew {amount} -> balance {self.balance}")

    def show(self):
        print(f"Owner: {self.owner}, Balance: {self.balance}")

    # BONUS: print(account) shows owner and balance
    def __str__(self):
        return f"Account(owner={self.owner}, balance={self.balance})"


print("=" * 50)
print("TASK 1: Bank Account Class")
print("=" * 50)

arun = Account("Arun", 1000)
try:
    arun.deposit(500)
    arun.withdraw(2000)          # raises InsufficientFundsError
except InsufficientFundsError as e:
    print("Error:", e)
finally:
    print("Transaction finished")   # always prints

# TASK 2: Inheritance and Overriding

class SavingsAccount(Account):
    def __init__(self, owner, balance=0, min_balance=500):
        super().__init__(owner, balance)   # reuse parent constructor
        self.min_balance = min_balance

    # Override: balance must never go below min_balance
    def withdraw(self, amount):
        if self.balance - amount < self.min_balance:
            raise InsufficientFundsError(
                f"Insufficient funds: balance {self.balance}, requested {amount}"
            )
        self.balance -= amount
        print(f"{self.owner} withdrew {amount} -> balance {self.balance}")


print()
print("=" * 50)
print("TASK 2: Inheritance and Overriding")
print("=" * 50)

priya = SavingsAccount("Priya", 1500)

for amount in (1200, 800):
    try:
        priya.withdraw(amount)
    except InsufficientFundsError as e:
        print("Error:", e)

print(isinstance(priya, Account))
# Explanation: True, because SavingsAccount inherits from Account,
# so a SavingsAccount object "is an" Account object too.

# BONUS: __str__ demo
print()
print("=" * 50)
print("BONUS: __str__ method")
print("=" * 50)

print(arun)
print(priya)