from typing import List, Dict, Callable, Any
import random

class TestCase:
    """Base TestCase class for date validation test cases."""
    
    def __init__(self, day: int, month: int, year: int, category_dict=None, validator=None):
        """
        Initialize a test case for date validation.
        
        Args:
            day: The day component of the date
            month: The month component of the date
            year: The year component of the date
            category_dict: Dictionary mapping category names to validation functions
            validator: The validation function to use
        """
        self.day = day
        self.month = month
        self.year = year
        self.date_str = f"{day:02d}/{month:02d}/{year:04d}"
        self.category_dict = category_dict
        self.validator = validator
        self.is_valid = self.validator(self.date_str) if self.validator else False
        self.categories = [cat for cat, check in self.category_dict.items() 
                          if check(day, month, year)] if self.category_dict else []

    def __str__(self):
        """String representation of the test case."""
        validity = "Valid" if self.is_valid else "Invalid"
        cats = ", ".join(self.categories) if self.categories else "General"
        return f"{self.date_str} ({validity}: {cats})"

    def __eq__(self, other):
        """Compare two test cases for equality."""
        return self.date_str == other.date_str


class TestCaseFormat(TestCase):
    """TestCase class for format variation (Instance 4)."""
    
    def __init__(self, day: int, month: int, year: int, format_type: str, 
                 category_dict=None, validator=None):
        """
        Initialize a test case for format variation.
        
        Args:
            day: The day component of the date
            month: The month component of the date
            year: The year component of the date
            format_type: The format of the date string
            category_dict: Dictionary mapping category names to validation functions
            validator: The validation function to use
        """
        self.day = day
        self.month = month
        self.year = year
        self.format_type = format_type
        
        # Format the date string according to the format type
        if format_type == "DD/MM/YYYY":
            self.date_str = f"{day:02d}/{month:02d}/{year:04d}"
        elif format_type == "MM/DD/YYYY":
            self.date_str = f"{month:02d}/{day:02d}/{year:04d}"
        elif format_type == "YYYY/MM/DD":
            self.date_str = f"{year:04d}/{month:02d}/{day:02d}"
        
        self.category_dict = category_dict
        self.validator = validator
        
        # Validate the date if a validator is provided
        self.is_valid = False
        if self.validator:
            self.is_valid = self.validator(self.date_str, format_type)
        
        # Check which categories this test case belongs to
        self.categories = []
        if self.category_dict:
            self.categories = [cat for cat, check in self.category_dict.items() 
                              if check(day, month, year, format_type)]

    def __str__(self):
        """String representation of the test case with format type."""
        validity = "Valid" if self.is_valid else "Invalid"
        cats = ", ".join(self.categories) if self.categories else "General"
        return f"{self.date_str} ({self.format_type}) ({validity}: {cats})"

    def __eq__(self, other):
        """Compare two test cases for equality, including format type."""
        return self.date_str == other.date_str and self.format_type == other.format_type


# Population initialization functions
def initialize_population(size: int, category_dict=None, validator=None) -> List[TestCase]:
    """
    Initialize a population of test cases.
    
    Args:
        size: The size of the population
        category_dict: Dictionary mapping category names to validation functions
        validator: The validation function to use
        
    Returns:
        A list of TestCase objects
    """
    population = [
        TestCase(29, 2, 2020, category_dict, validator),  # Valid Leap Year
        TestCase(30, 4, 2023, category_dict, validator),  # Valid 30-Day Month
        TestCase(31, 12, 9999, category_dict, validator),  # Valid 31-Day Month, Boundary Max Year
        TestCase(32, 5, 2023, category_dict, validator),  # Invalid Day > 31
        TestCase(15, 13, 2023, category_dict, validator),  # Invalid Month > 12
        TestCase(29, 2, 2021, category_dict, validator),  # Invalid Feb 29 Non-Leap
        TestCase(1, 1, 0, category_dict, validator),  # Boundary Min Year
        TestCase(1, 1, 9999, category_dict, validator),  # Boundary Max Year
    ]
    
    # Add random test cases
    for _ in range(size - 8):
        day = random.randint(1, 40)
        month = random.randint(1, 15)
        year = random.choice([0, 9999, random.randint(0, 9999)])
        population.append(TestCase(day, month, year, category_dict, validator))
    
    return population


def initialize_population_instance_4(size: int, category_dict=None, validator=None) -> List[TestCaseFormat]:
    """
    Initialize a population of test cases for Instance 4 (format variations).
    
    Args:
        size: The size of the population
        category_dict: Dictionary mapping category names to validation functions
        validator: The validation function to use
        
    Returns:
        A list of TestCaseFormat objects
    """
    population = [
        TestCaseFormat(15, 5, 2023, "DD/MM/YYYY", category_dict, validator),
        TestCaseFormat(5, 15, 2023, "MM/DD/YYYY", category_dict, validator),
        TestCaseFormat(15, 5, 2023, "YYYY/MM/DD", category_dict, validator),
        TestCaseFormat(5, 6, 2023, "DD/MM/YYYY", category_dict, validator),  # Ambiguous
    ]
    
    formats = ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY/MM/DD"]
    for _ in range(size - 4):
        day = random.randint(1, 40)
        month = random.randint(1, 15)
        year = random.randint(0, 9999)
        format_type = random.choice(formats)
        population.append(TestCaseFormat(day, month, year, format_type, category_dict, validator))
    
    return population
