from typing import Dict, Callable

# Categories for instance 3: Complex Month-Day Combinations
CATEGORIES = {
    "Invalid Feb 30": lambda d, m, y: m == 2 and d == 30,
    "Invalid Apr 31": lambda d, m, y: m == 4 and d == 31,
    "Invalid Jun 31": lambda d, m, y: m == 6 and d == 31,
    "Invalid Sep 31": lambda d, m, y: m == 9 and d == 31,
    "Invalid Nov 31": lambda d, m, y: m == 11 and d == 31,
}

# Default parameters for instance 3
DEFAULT_PARAMS = {
    "pop_size": 40,
    "generations": 80,
    "valid_min": 0,
    "invalid_min": 10,
    "boundary_min": 0,
    "instance_name": "Instance 3"
}
