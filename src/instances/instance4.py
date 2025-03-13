from typing import Dict, Callable

# Categories for instance 4: Format Variations
CATEGORIES = {
    "Valid DD/MM/YYYY": lambda d, m, y, f: f == "DD/MM/YYYY" and d <= 31 and m <= 12,
    "Valid MM/DD/YYYY": lambda d, m, y, f: f == "MM/DD/YYYY" and d <= 31 and m <= 12,
    "Valid YYYY/MM/DD": lambda d, m, y, f: f == "YYYY/MM/DD" and d <= 31 and m <= 12,
    "Invalid Ambiguous": lambda d, m, y, f: d <= 12 and m <= 12 and f in ("DD/MM/YYYY", "MM/DD/YYYY"),
}

# Default parameters for instance 4
DEFAULT_PARAMS = {
    "pop_size": 50,
    "generations": 100,
    "valid_min": 10,
    "invalid_min": 10,
    "instance_name": "Instance 4"
}
