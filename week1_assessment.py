#Task 1 - Python core, OOP and errors

# 1. bonus() with default arg, *args and **kwargs
def bonus(salary, rate=0.1, *extras, **options):
    """Return salary * rate plus all extras; apply options['cap'] if given."""
    result = salary * rate + sum(extras)
    if "cap" in options:
        result = min(result, options["cap"])
    return result


# 2. Custom exception + classes
class InvalidSalaryError(Exception):
    """Raised when a salary is negative."""

    def __init__(self, salary):
        self.salary = salary
        super().__init__(f"Invalid salary: {salary}")


class Employee:
    def __init__(self, name, salary):
        if salary < 0:
            raise InvalidSalaryError(salary)
        self.name = name
        self.salary = salary

    def annual_salary(self):
        return self.salary * 12          

    def get_details(self):
        return f"{self.name} earns {self.salary} per month"


class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)   
        self.team_size = team_size

    def get_details(self):               
        return f"{super().get_details()} and manages {self.team_size} people"


employees = [
    {"id": 1, "name": "Arun", "department": "Sales", "salary": 30000, "city": "Chennai"},
    {"id": 2, "name": "Priya", "department": "HR", "salary": 45000, "city": "Chennai"},
    {"id": 3, "name": "Rahul", "department": "IT", "salary": 60000, "city": "Bangalore"},
    {"id": 4, "name": "Divya", "department": "IT", "salary": 75000, "city": "Chennai"},
    {"id": 5, "name": "Karthik", "department": "Finance", "salary": 90000, "city": "Mumbai"},
    {"id": 6, "name": "Meena", "department": "Sales", "salary": 52000, "city": "Bangalore"},
    {"id": 7, "name": "Suresh", "department": "IT", "salary": 68000, "city": "Chennai"},
    {"id": 8, "name": "Anitha", "department": "HR", "salary": 48000, "city": "Mumbai"},
]

if __name__ == "__main__":
    #bonus demo
    print("bonus(50000):", bonus(50000))
    print("bonus(50000, 0.2, 500, 1000):", bonus(50000, 0.2, 500, 1000))
    print("bonus(50000, 0.2, 500, cap=8000):", bonus(50000, 0.2, 500, cap=8000))

    #OOP demo
    emp = Employee("Arun", 30000)
    mgr = Manager("Divya", 75000, 4)
    print(emp.get_details(), "| annual:", emp.annual_salary())
    print(mgr.get_details(), "| annual:", mgr.annual_salary())
    print("-" * 40)

    # comprehension / map+lambda / filter 
    above_50k = [e["name"] for e in employees if e["salary"] > 50000]
    print("Above 50000:", above_50k)

    raised = list(map(lambda e: {**e, "salary": round(e["salary"] * 1.1)}, employees))
    print("After 10% raise:", [(e["name"], e["salary"]) for e in raised])

    chennai = [e["name"] for e in filter(lambda e: e["city"] == "Chennai", employees)]
    print("Chennai:", chennai)

    # exception handling with try/except/finally
    try:
        Employee("Test", -500)
    except InvalidSalaryError as err:
        print(f"Error: {err}")
    finally:
        print("Transaction finished")

    # loop with continue and break
    print("-" * 40)
    salaries = [30000, 0, 45000, 60000, 0, 90000, 52000]   
    for s in salaries:
        if s == 0:
            continue                       
        print("Processing salary:", s)
        if s > 85000:
            print("First salary above 85000 found -> stopping")
            break

#Task 2 - Files, APIs and environment variables
import csv
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

FOLDER = Path(__file__).resolve().parent   
BASE = DATA = FOLDER
URL = "https://jsonplaceholder.typicode.com"

# creates the CSV files next to this script if they do not exist 
def make_file(name, text):
    path = FOLDER / name
    if not path.exists():
        path.write_text(text, encoding="utf-8")

make_file("employees.csv", """id,name,department,salary,city
1,Arun,Sales,30000,Chennai
2,Priya,HR,45000,Chennai
3,Rahul,IT,60000,Bangalore
4,Divya,IT,75000,Chennai
5,Karthik,Finance,90000,Mumbai
6,Meena,Sales,52000,Bangalore
7,Suresh,IT,68000,Chennai
8,Anitha,HR,48000,Mumbai
""")

if not (FOLDER / ".env").exists():
    (FOLDER / ".env").write_text("API_KEY=your_api_key_here\n")   # demo key; .env must be in .gitignore


# 1. CSV -> JSON and high earners CSV 
with open(DATA / "employees.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
for r in rows:                      
    r["id"] = int(r["id"])
    r["salary"] = int(r["salary"])

high = [r for r in rows if r["salary"] > 50000]

with open(DATA / "employees.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2)

with open(DATA / "high_earners.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(high)

print(f"Rows read: {len(rows)} | High earners: {len(high)}")

#  2. API key from .env (never hard-coded, never printed)
load_dotenv(BASE / ".env")
api_key = os.getenv("API_KEY")
if not api_key:
    print("Warning: API_KEY not found in .env")
headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

#  3. GET /users with error handling 
try:
    resp = requests.get(f"{URL}/users", headers=headers, timeout=5)
    resp.raise_for_status()
    users = resp.json()

    for u in users[:3]:
        print(f"{u['id']} - {u['name']} - {u['email']}")

    #  4. nested JSON with .get() 
    cleaned = []
    for u in users:
        cleaned.append({
            "id": u.get("id"),
            "name": u.get("name"),
            "email": u.get("email"),
            "city": u.get("address", {}).get("city"),
            "lat": u.get("address", {}).get("geo", {}).get("lat"),
            "lng": u.get("address", {}).get("geo", {}).get("lng"),
            "company": u.get("company", {}).get("name"),
        })
    with open(DATA / "users.json", "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2)
    print(f"Saved {len(cleaned)} users to data/users.json")

except requests.exceptions.Timeout:
    print("Error: request timed out (5 s)")
except requests.exceptions.ConnectionError:
    print("Error: could not connect - check your internet")
except requests.exceptions.HTTPError as err:
    print("HTTP error:", err)

#  5. 404 handling
try:
    r404 = requests.get(f"{URL}/users/9999", timeout=5)
    if r404.status_code == 404:
        print("/users/9999 -> 404 Not found")
    else:
        print(f"/users/9999 -> {r404.status_code}")
except requests.exceptions.Timeout:
    print("Error: request timed out (5 s)")
except requests.exceptions.ConnectionError:
    print("Error: could not connect - check your internet")        

#Task 3 - NumPy, Pandas and Matplotlib
from pathlib import Path

import matplotlib
matplotlib.use("Agg")                      
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

FOLDER = Path(__file__).resolve().parent  
DATA = REPORTS = FOLDER

#  creates the CSV files next to this script if they do not exist 
def make_file(name, text):
    path = FOLDER / name
    if not path.exists():
        path.write_text(text, encoding="utf-8")

make_file("employees.csv", """id,name,department,salary,city
1,Arun,Sales,30000,Chennai
2,Priya,HR,45000,Chennai
3,Rahul,IT,60000,Bangalore
4,Divya,IT,75000,Chennai
5,Karthik,Finance,90000,Mumbai
6,Meena,Sales,52000,Bangalore
7,Suresh,IT,68000,Chennai
8,Anitha,HR,48000,Mumbai
""")
make_file("employees_messy.csv", """id,name,department,salary,city
1,Arun,Sales,30000,Chennai
2,Priya,HR,,Chennai
3,Rahul,IT,60000,Bangalore
4,Divya,IT,75000,Chennai
5,Karthik,Finance,90000,Mumbai
6,Meena,Sales,52000,Bangalore
7,Suresh,IT,,Chennai
8,Anitha,HR,48000,Mumbai
8,Anitha,HR,48000,Mumbai
""")
make_file("departments.csv", """department,head,budget
Sales,Ravi Kumar,500000
HR,Lakshmi Devi,300000
IT,Vikram Rao,900000
Finance,Sanjay Mehta,600000
Marketing,Nisha Patel,400000
""")


# NumPy
print("=== NumPy ===")
marks = np.array([[78, 85, 90],
                  [62, 70, 68],
                  [95, 88, 92],
                  [55, 60, 58]])            
print("Shape:", marks.shape)
print("Student averages:", marks.mean(axis=1).round(2))
print("Subject averages:", marks.mean(axis=0).round(2))
print("With 5 grace marks (broadcasting):\n", marks + 5)
weights = np.array([0.5, 0.3, 0.2])         # subject weightage
print("Weighted scores (np.dot):", np.dot(marks, weights).round(2))

# Pandas basics
print("\n=== Pandas basics ===")
emp = pd.read_csv(DATA / "employees.csv")
emp.info()
print(emp.describe())
print("loc  (rows 0-2, name & salary):\n", emp.loc[0:2, ["name", "salary"]])
print("iloc (first 3 rows, first 3 cols):\n", emp.iloc[:3, :3])
print("Filter salary > 50000 and IT:\n", emp[(emp["salary"] > 50000) & (emp["department"] == "IT")])

# Cleaning 
print("\n=== Cleaning ===")
messy = pd.read_csv(DATA / "employees_messy.csv")
print("Before: rows =", len(messy), "| missing salaries =", messy["salary"].isna().sum(),
      "| duplicates =", messy.duplicated().sum())
messy = messy.drop_duplicates()
messy["salary"] = messy["salary"].fillna(messy["salary"].median())   
messy["salary"] = messy["salary"].astype(int)                        
messy["id"] = messy["id"].astype(int)
print("After : rows =", len(messy), "| missing salaries =", messy["salary"].isna().sum())
clean = messy.reset_index(drop=True)
clean.to_csv(DATA / "employees_clean.csv", index=False)

# groupby + merge 
print("\n=== groupby / merge ===")
stats = (clean.groupby("department")["salary"]
              .agg(headcount="count", avg_salary="mean", max_salary="max")
              .reset_index())
print(stats)
print("Headcount:", " | ".join(f"{d} {h}" for d, h in clean["department"].value_counts(sort=False).items()))

depts = pd.read_csv(DATA / "departments.csv")
inner = pd.merge(stats, depts, on="department", how="inner")
left = pd.merge(stats, depts, on="department", how="left")
outer = pd.merge(stats, depts, on="department", how="outer")
print("\nInner join rows:", len(inner), "| Left join rows:", len(left), "| Outer join rows:", len(outer))
print(outer)
empty = outer[outer["headcount"].isna()]["department"].tolist()
print("Outer join: department with no employees ->", empty)

# Charts
print("\n=== Charts ===")
insights = {}

# 1. Bar - average salary per department
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.bar(stats["department"], stats["avg_salary"], color="#4C78A8", label="Average salary")
ax.set(title="Average Salary by Department", xlabel="Department", ylabel="Salary (INR)")
ax.legend(); fig.tight_layout(); fig.savefig(REPORTS / "bar_avg_salary.png", dpi=120); plt.close(fig)
top = stats.loc[stats["avg_salary"].idxmax()]
insights["bar_avg_salary.png"] = f"{top.department} has the highest average salary (INR {top.avg_salary:,.0f})."

# 2. Histogram - salary distribution
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.hist(clean["salary"], bins=5, color="#F58518", edgecolor="black", label="Employees")
ax.set(title="Salary Distribution", xlabel="Salary (INR)", ylabel="Number of employees")
ax.legend(); fig.tight_layout(); fig.savefig(REPORTS / "hist_salary.png", dpi=120); plt.close(fig)
insights["hist_salary.png"] = (f"Most employees earn between 45,000 and 75,000; "
                               f"the median salary is INR {clean['salary'].median():,.0f}.")

# 3. Scatter - employee id vs salary, coloured by department
fig, ax = plt.subplots(figsize=(7, 4.5))
for d, g in clean.groupby("department"):
    ax.scatter(g["id"], g["salary"], s=80, label=d)
ax.set(title="Salary by Employee ID", xlabel="Employee ID", ylabel="Salary (INR)")
ax.legend(title="Department"); fig.tight_layout(); fig.savefig(REPORTS / "scatter_salary.png", dpi=120); plt.close(fig)
lo, hi = clean.loc[clean["salary"].idxmin()], clean.loc[clean["salary"].idxmax()]
insights["scatter_salary.png"] = (f"{hi['name']} ({hi['department']}) earns the most at INR {hi['salary']:,}, "
                                  f"while {lo['name']} ({lo['department']}) earns the least at INR {lo['salary']:,}.")

# 4. Line - average salary per city
city = clean.groupby("city")["salary"].mean().sort_values()
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(city.index, city.values, marker="o", color="#54A24B", label="Average salary")
ax.set(title="Average Salary by City", xlabel="City", ylabel="Salary (INR)")
ax.legend(); fig.tight_layout(); fig.savefig(REPORTS / "line_city_salary.png", dpi=120); plt.close(fig)
insights["line_city_salary.png"] = f"{city.index[-1]} pays the highest average salary and {city.index[0]} the lowest."

with open(REPORTS / "insights.txt", "w", encoding="utf-8") as f:
    for name, text in insights.items():
        print(f"{name}: {text}")
        f.write(f"{name}: {text}\n")
