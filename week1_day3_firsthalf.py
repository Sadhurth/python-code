import os
import numpy as np
import pandas as pd
# TASK 1 : NumPy Arrays
print("=" * 60)
print("TASK 1 : NumPy Arrays")
print("=" * 60)

marks = np.array([[70, 80, 90],
                  [60, 75, 85],
                  [88, 92, 79],
                  [55, 65, 70]])

print("Shape:", marks.shape)
print("Dtype:", marks.dtype)
print("Size:", marks.size)

print("\nFirst two students, last subject:")
print(marks[:2, -1])          # -> [90 85]

student_avg = marks.mean(axis=1)
subject_avg = marks.mean(axis=0)
print("\nStudent averages:", np.round(student_avg, 2))
print("Subject averages:", np.round(subject_avg, 2))

print("Total per student:", marks.sum(axis=1))
print("Total per subject:", marks.sum(axis=0))

with_grace = marks + 5
print("\nMarks after +5 grace marks:")
print(with_grace)

weights = np.array([0.3, 0.3, 0.4])
weighted_scores = np.dot(marks, weights)     
print("\nWeighted scores:", np.round(weighted_scores, 2))

reshaped = np.arange(12).reshape(3, 4)
print("\nnp.arange(12) reshaped to 3x4:")
print(reshaped)
# TASK 2 : Pandas DataFrame Basics
print("\n" + "=" * 60)
print("TASK 2 : Pandas DataFrame Basics")
print("=" * 60)

# 1. Create employees.csv (next to this script) and load it
csv_data = """id,name,department,salary,city
1,Arun,Sales,30000,Chennai
2,Priya,HR,45000,Chennai
3,Rahul,IT,60000,Bangalore
4,Divya,IT,75000,Chennai
5,Karthik,Finance,90000,Mumbai
6,Meena,Sales,52000,Bangalore
7,Suresh,IT,68000,Chennai
8,Anitha,HR,48000,Mumbai
"""

csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "employees.csv")
with open(csv_path, "w") as f:
    f.write(csv_data)

df = pd.read_csv(csv_path)
# 2. head, info, describe
print("\n--- df.head() ---")
print(df.head())

print("\n--- df.info() ---")
df.info()

print("\n--- df.describe() ---")
print(df.describe())

print("""
What they show:
1. head()     -> displays the first 5 rows so we can quickly see the columns and sample values.
2. info()     -> shows 8 rows, 5 columns, the data type of each column and that there are no missing values.
3. describe() -> gives count, mean, std, min, quartiles and max for numeric columns (e.g. salary mean = 58500).
""")

# 3. Column selection
print("--- name column ---")
print(df["name"])

print("\n--- name and salary together ---")
print(df[["name", "salary"]])

# 4. loc and iloc
chennai_names = df.loc[df["city"] == "Chennai", "name"]
print("\nChennai:", ", ".join(chennai_names))

print("\n--- df.iloc[0:3, 1:3] ---")
print(df.iloc[0:3, 1:3])

# 5. Filtering
high_salary = df[df["salary"] > 50000]
it_dept = df[df["department"] == "IT"]

print(f"\nSalary above 50000: {len(high_salary)} employees")
print("IT department:", ", ".join(it_dept["name"]))
print(f"IT department count: {len(it_dept)}")
# BONUS CHALLENGE
print("\n" + "=" * 60)
print("BONUS : Reshape 24 values into 2x3x4")
print("=" * 60)

arr3d = np.arange(24).reshape(2, 3, 4)
print("3D array shape:", arr3d.shape)
print(arr3d)

for i in range(arr3d.shape[0]):
    print(f"Slice {i} along axis 0 -> shape: {arr3d[i].shape}")

    