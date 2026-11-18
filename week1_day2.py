
import csv
import json
import os
import sys
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
sys.path.insert(0, BASE_DIR)


def header(title):
    print("\n" + "=" * 8 + f" {title} " + "=" * 8)
# PART 1 - TASK 1 : Reading and Writing Files
def part1_task1():
    header("Part 1 / Task 1: File I/O")
    students = [
        {"name": "Arun", "marks": 45},
        {"name": "Priya", "marks": 58},
        {"name": "Rahul", "marks": 72},
        {"name": "Divya", "marks": 88},
        {"name": "Karthik", "marks": 60},
    ]

    with open("names.txt", "w") as f:
        for s in students:
            f.write(s["name"] + "\n")
    with open("names.txt", "r") as f:
        for i, line in enumerate(f, start=1):
            print(f"{i}. {line.strip()}")

    # CSV
    with open("students.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "marks"])
        writer.writeheader()
        writer.writerows(students)
    with open("students.csv", "r", newline="") as f:
        above = [f"{r['name']} {r['marks']}" for r in csv.DictReader(f) if int(r["marks"]) > 60]
    print("Above 60:", " | ".join(above))
    with open("students.json", "w") as f:
        json.dump(students, f, indent=2)
    with open("students.json", "r") as f:
        print("Loaded from JSON:", json.load(f))

    try:
        with open("missing.txt", "r") as f:
            f.read()
    except FileNotFoundError:
        print("missing.txt -> File not found")

MATH_TOOLS_CODE = '''def add(a, b):
    """Return the sum of a and b."""
    return a + b


def average(numbers):
    """Return the average of a list of numbers."""
    return sum(numbers) / len(numbers) if numbers else 0

if __name__ == "__main__":
    print("Testing math_tools...")
    print(add(2, 3))
    print(average([10, 20, 30]))
'''

MAIN_CODE = '''from utils.math_tools import add, average

print("add(10, 5)        =", add(10, 5))
print("average([4,8,12]) =", average([4, 8, 12]))
'''


def part1_task2():
    header("Part 1 / Task 2: Modules & Packages")
    os.makedirs("utils", exist_ok=True)
    with open("utils/__init__.py", "w") as f:
        f.write("# makes utils a package\n")
    with open("utils/math_tools.py", "w") as f:
        f.write(MATH_TOOLS_CODE)
    with open("main.py", "w") as f:
        f.write(MAIN_CODE)

    from utils.math_tools import add, average  # same import as main.py
    print("add(10, 5)        =", add(10, 5))
    print("average([4,8,12]) =", average([4, 8, 12]))
# PART 2 - TASK 1 : REST Calls and Status Codes
def explain_status(code):
    messages = {
        200: "OK - request succeeded",
        201: "Created - resource was created",
        400: "Bad Request - check your input",
        401: "Unauthorized - missing or invalid credentials",
        404: "Not found",
        500: "Server Error - something went wrong on the server",
    }
    return messages.get(code, "Unknown status")


def part2_task1():
    header("Part 2 / Task 1: REST calls")
    url = "https://jsonplaceholder.typicode.com"
    try:
        r = requests.get(f"{url}/users", timeout=5)
        for u in r.json()[:5]:
            print(f"{u['id']} - {u['name']} - {u['email']}")

        r = requests.post(f"{url}/posts",
                          json={"title": "Hello", "body": "My first post", "userId": 1},
                          timeout=5)
        print(f"POST: {r.status_code}, id: {r.json()['id']}")

        put = requests.put(f"{url}/posts/1",
                           json={"id": 1, "title": "Updated", "body": "New", "userId": 1},
                           timeout=5)
        patch = requests.patch(f"{url}/posts/1", json={"title": "Patched"}, timeout=5)
        delete = requests.delete(f"{url}/posts/1", timeout=5)
        print(f"PUT: {put.status_code} | PATCH: {patch.status_code} | DELETE: {delete.status_code}")

        r = requests.get(f"{url}/posts/9999", timeout=5)
        print(f"GET /posts/9999 -> {r.status_code} {explain_status(r.status_code)}")
    except requests.exceptions.Timeout:
        print("Request timed out: please try again")
    except requests.exceptions.ConnectionError:
        print("Connection error: check your internet")

# PART 2 - TASK 2 : JSON, Environment Variables and Timeouts
def safe_get(url, retries=3, timeout=3):
    """Bonus: retry up to 3 times on timeout before giving up."""
    for attempt in range(1, retries + 1):
        try:
            return requests.get(url, timeout=timeout)
        except requests.exceptions.Timeout:
            print(f"  Attempt {attempt} timed out")
        except requests.exceptions.ConnectionError:
            print("  Connection error")
            return None
    print("  Giving up after 3 timeouts")
    return None


def part2_task2():
    header("Part 2 / Task 2: Env vars & timeouts")
    with open(".env", "w") as f:
        f.write("API_KEY=demo-key-123\n")
    existing = open(".gitignore").read() if os.path.exists(".gitignore") else ""
    if ".env" not in existing.split():
        with open(".gitignore", "a") as f:
            f.write(".env\n.venv/\n__pycache__/\n")

    load_dotenv()
    api_key = os.getenv("API_KEY")

    try:
        r = requests.get("https://httpbin.org/headers",
                         headers={"X-API-Key": api_key}, timeout=5)
        print("Server received key:", r.json()["headers"].get("X-Api-Key"))
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.ConnectionError:
        print("Could not connect to server")

    try:
        requests.get("https://httpbin.org/delay/10", timeout=3)
    except requests.exceptions.Timeout:
        print("Timeout after 3 seconds: please try again")
    except requests.exceptions.ConnectionError:
        print("Could not connect to server")

    try:
        r = requests.get("https://httpbin.org/status/500", timeout=5)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Server error 500 handled")
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.ConnectionError:
        print("Could not connect to server")

    # Nested JSON -> result.json
    try:
        data = requests.get("https://httpbin.org/get", params={"q": "python"}, timeout=5).json()
        result = {
            "url": data.get("url"),
            "query": data.get("args", {}).get("q"),
            "user_agent": data.get("headers", {}).get("User-Agent"),
        }
        with open("result.json", "w") as f:
            json.dump(result, f, indent=2)
        print("Saved result.json:", result)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        print("Network problem while fetching nested JSON")

    print("Bonus safe_get:")
    safe_get("https://httpbin.org/delay/10")


if __name__ == "__main__":
    part1_task1()
    part1_task2()
    part2_task1()
    part2_task2()