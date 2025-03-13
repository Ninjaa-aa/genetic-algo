from typing import Dict, Callable

# Categories for instance 2: Advanced Leap Year & Boundaries
CATEGORIES = {
    "Valid Leap Year": lambda d, m, y: m == 2 and d == 29 and y % 4 == 0 and (y % 100 != 0 or y % 400 == 0),
    "Valid Non-Leap Feb": lambda d, m, y: m == 2 and d == 28 and y == 1900,
    "Invalid Feb 29 Non-Leap": lambda d, m, y: m == 2 and d == 29 and (y % 4 != 0 or (y % 100 == 0 and y % 400 != 0)),
    "Invalid Feb 29 1900": lambda d, m, y: m == 2 and d == 29 and y == 1900,
    "Boundary Min Year": lambda d, m, y: y == 0,
    "Boundary Max Year": lambda d, m, y: y == 9999,
}

# Default parameters for instance 2
DEFAULT_PARAMS = {
    "pop_size": 50,
    "generations": 100,
    "valid_min": 10,
    "invalid_min": 10,
    "boundary_min": 2,
    "instance_name": "Instance 2"
}
