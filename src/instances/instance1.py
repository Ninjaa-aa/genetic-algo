from typing import Dict, Callable

# Categories for instance 1: Basic Date Validation
CATEGORIES = {
    "Valid 30-Day Month": lambda d, m, y: m in (4, 6, 9, 11) and d == 30,
    "Invalid Day > 31": lambda d, m, y: d > 31,
    "Invalid Month > 12": lambda d, m, y: m > 12,
    "Invalid 30-Day Month": lambda d, m, y: m in (4, 6, 9, 11) and d > 30,
    "Boundary 31-Day Month": lambda d, m, y: d == 31 and m == 1 and y == 2023,
}

# Default parameters for instance 1
DEFAULT_PARAMS = {
    "pop_size": 30,
    "generations": 70,
    "valid_min": 5,
    "invalid_min": 5,
    "boundary_min": 1,
    "instance_name": "Instance 1"
}
