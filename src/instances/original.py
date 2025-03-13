from typing import Dict, Callable

# Categories for the original problem
CATEGORIES = {
    "Valid Leap Year": lambda d, m, y: m == 2 and d == 29 and y % 4 == 0 and (y % 100 != 0 or y % 400 == 0),
    "Valid 30-Day Month": lambda d, m, y: m in (4, 6, 9, 11) and d == 30,
    "Valid 31-Day Month": lambda d, m, y: m in (1, 3, 5, 7, 8, 10, 12) and d == 31,
    "Invalid Day > 31": lambda d, m, y: d > 31,
    "Invalid Month > 12": lambda d, m, y: m > 12,
    "Invalid Feb 29 Non-Leap": lambda d, m, y: m == 2 and d == 29 and (y % 4 != 0 or (y % 100 == 0 and y % 400 != 0)),
    "Boundary Min Year": lambda d, m, y: y == 0,
    "Boundary Max Year": lambda d, m, y: y == 9999,
}

# Default parameters for the original problem
DEFAULT_PARAMS = {
    "pop_size": 50,
    "generations": 100,
    "valid_min": 10,
    "invalid_min": 10,
    "boundary_min": 5,
    "instance_name": "Original"
}
