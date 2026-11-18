def add(a, b):
    """Return the sum of a and b."""
    return a + b


def average(numbers):
    """Return the average of a list of numbers."""
    return sum(numbers) / len(numbers) if numbers else 0

if __name__ == "__main__":
    print("Testing math_tools...")
    print(add(2, 3))
    print(average([10, 20, 30]))
