from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).parent
CSV_PATH = BASE_DIR / "employees.csv"

#Load data
df = pd.read_csv(CSV_PATH)
df.columns = df.columns.str.strip().str.lower()   # id, department, salary
df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
df = df.dropna(subset=["salary"])

avg_salary = df.groupby("department")["salary"].mean().sort_values(ascending=False)

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [12, 15, 14, 18, 22, 25]


# Chart drawing functions (take an axes so they work for both single and 2x2)
def draw_bar(ax):
    bars = ax.bar(avg_salary.index, avg_salary.values, color="steelblue")
    ax.set_title("Average Salary per Department")
    ax.set_xlabel("Department")
    ax.set_ylabel("Average Salary")
    for bar in bars:                                   # values on the bars
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f"{bar.get_height():,.0f}", ha="center", va="bottom", fontsize=8)


def draw_hist(ax):
    ax.hist(df["salary"], bins=5, color="seagreen", edgecolor="black")
    ax.set_title("Salary Distribution (5 bins)")
    ax.set_xlabel("Salary")
    ax.set_ylabel("Number of Employees")


def draw_scatter(ax):
    for dept, group in df.groupby("department"): 
        ax.scatter(group["id"], group["salary"], label=dept)
    ax.set_title("Employee ID vs Salary")
    ax.set_xlabel("Employee ID")
    ax.set_ylabel("Salary")
    ax.legend(title="Department")


def draw_line(ax):
    ax.plot(months, sales, marker="o", color="darkorange")
    ax.set_title("Monthly Sales (Jan - Jun)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales")
    ax.grid(True, alpha=0.3)


charts = {
    "bar_avg_salary.png": draw_bar,
    "histogram_salary.png": draw_hist,
    "scatter_id_vs_salary.png": draw_scatter,
    "line_monthly_sales.png": draw_line,
}

#Task 1: save each chart as its own PNG 
for filename, draw in charts.items():
    fig, ax = plt.subplots(figsize=(8, 5))
    draw(ax)
    fig.tight_layout()
    fig.savefig(BASE_DIR / filename, dpi=150)
    plt.close(fig)
    print(f"Saved {filename}")

# Bonus: all four charts on one figure
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
draw_bar(axes[0, 0])
draw_hist(axes[0, 1])
draw_scatter(axes[1, 0])
draw_line(axes[1, 1])
fig.suptitle("Week 1 - Day 4: All Charts", fontsize=16)
fig.tight_layout()
fig.savefig(BASE_DIR / "all_charts.png", dpi=150)
print("Saved all_charts.png")
plt.show()