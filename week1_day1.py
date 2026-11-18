#Task 1
# TASK 1: Sales Report Basics
print("=" * 50)
print("TASK 1: Sales Report Basics")
print("=" * 50)
age = 25                                
rating = 4.5                            
name = "Yoho"                           
fruits = ["apple", "banana", "mango"]   
student = {"name": "Sadhurth", "age": 21}   
unique_ids = {101, 102, 103}            
coordinates = (10.36, 77.97)           

for value in (age, rating, name, fruits, student, unique_ids, coordinates):
    print(value, type(value))

print()

# 2. Sales loop with continue / break ---
sales = [12000, 0, 8500, 15000, -200, 9800]
total_sales = 0

for x in sales:
    if x <= 0:
        print("Skipped invalid value", x)
        continue                        

    total_sales += x
    print("Added", x, "total", total_sales)

    if total_sales > 30000:
        break                           

#  3. if / elif / else after the loop
if total_sales > 30000:
    print("Target reached. Stopped at", total_sales)
elif total_sales == 30000:
    print("Target reached. Stopped at", total_sales)
else:
    print("Target not reached")

# TASK 2: Functions and Comprehensions
print()
print("=" * 50)
print("TASK 2: Functions and Comprehensions")
print("=" * 50)

prices = [500, 1200, 800, 2500, 300]


def apply_discount(price, discount=10):
    """Return the price after applying a percentage discount."""
    return price - (price * discount / 100)


def total(*args):
    """Return the sum of any number of values."""
    return sum(args)


def describe(**kwargs):
    """Print every key and value passed in."""
    for key, value in kwargs.items():
        print(f"{key}: {value}")


# Function results
print("apply_discount(1000) ->", apply_discount(1000))
print("apply_discount(1000, 25) ->", apply_discount(1000, 25))
print("total(5, 10, 15) ->", total(5, 10, 15))
describe(name="Laptop", price=55000, brand="Dell")

# List comprehension: prices above 1000
above_1000 = [p for p in prices if p > 1000]
print("Above 1000:", above_1000)

#  map() with lambda: add 18% GST, round to 2 decimals
with_gst = list(map(lambda p: round(p * 1.18, 2), prices))
print("With GST:", with_gst)

# filter(): keep prices below 1000
below_1000 = list(filter(lambda p: p < 1000, prices))
print("Below 1000:", below_1000)

# BONUS CHALLENGE: Sales loop rewritten with while

print()
print("=" * 50)
print("BONUS: while loop version")
print("=" * 50)

running_total = 0
i = 0

while i < len(sales):
    x = sales[i]
    i += 1                            

    if x <= 0:
        print("Skipped invalid value", x)
        continue

    running_total += x
    print("Added", x, "total", running_total)

    if running_total > 30000:
        break

if running_total > 30000:
    print("Target reached. Stopped at", running_total)
else:
    print("Target not reached")

print()
print("Comparison:")
print("- for loop  : Python handles the index automatically; shorter and cleaner.")
print("- while loop: you manage the index (i) yourself; more code and a risk of")
print("              an infinite loop if you forget i += 1 (especially before 'continue').")
print("- Both give the same result. Use 'for' when iterating over a known list,")
print("  and 'while' when the number of iterations depends on a condition.")

#week1_day1_secondhalf
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
    arun.withdraw(2000)          
except InsufficientFundsError as e:
    print("Error:", e)
finally:
    print("Transaction finished")   


# TASK 2: Inheritance and Overriding
class SavingsAccount(Account):
    def __init__(self, owner, balance=0, min_balance=500):
        super().__init__(owner, balance)  
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
# BONUS: __str__ demo
print()
print("=" * 50)
print("BONUS: __str__ method")
print("=" * 50)

print(arun)
print(priya)