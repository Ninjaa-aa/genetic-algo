import re

def is_valid_date(date_str: str) -> bool:
    """
    Validate if a date string in the format DD/MM/YYYY is a valid date.
    
    Args:
        date_str: A string representing a date in DD/MM/YYYY format
        
    Returns:
        bool: True if the date is valid, False otherwise
    """
    if not re.match(r"^\d{2}/\d{2}/\d{4}$", date_str):
        return False
    
    day_str, month_str, year_str = date_str.split("/")
    try:
        day, month, year = int(day_str), int(month_str), int(year_str)
    except ValueError:
        return False
    
    if year < 0 or year > 9999 or month < 1 or month > 12 or day < 1:
        return False
    
    if month in (4, 6, 9, 11) and day > 30:
        return False
    elif month == 2:
        is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        max_day = 29 if is_leap else 28
        if day > max_day:
            return False
    elif day > 31:
        return False
    
    return True

def validator_instance_1(date_str: str) -> bool:
    """
    Basic date validation function for Instance 1.
    Simpler than the original - doesn't check for leap years.
    
    Args:
        date_str: A string representing a date in DD/MM/YYYY format
        
    Returns:
        bool: True if the date is valid according to Instance 1 rules, False otherwise
    """
    if not re.match(r"^\d{2}/\d{2}/\d{4}$", date_str):
        return False
    
    day_str, month_str, year_str = date_str.split("/")
    try:
        day, month, year = int(day_str), int(month_str), int(year_str)
    except ValueError:
        return False
    
    if year < 0 or year > 9999 or month < 1 or month > 12 or day < 1:
        return False
    
    if month in (4, 6, 9, 11) and day > 30:
        return False
    
    if day > 31:
        return False
    
    return True

def validator_instance_2(date_str: str) -> bool:
    """
    Validation function for Instance 2.
    Same as the original validator, with focus on leap years.
    
    Args:
        date_str: A string representing a date in DD/MM/YYYY format
        
    Returns:
        bool: True if the date is valid, False otherwise
    """
    return is_valid_date(date_str)

def validator_instance_3(date_str: str) -> bool:
    """
    Validation function for Instance 3.
    Same as the original validator, with focus on month-day combinations.
    
    Args:
        date_str: A string representing a date in DD/MM/YYYY format
        
    Returns:
        bool: True if the date is valid, False otherwise
    """
    return is_valid_date(date_str)

def validator_instance_4(date_str: str, format_type: str) -> bool:
    """
    Validation function for Instance 4.
    Validates dates with different formats.
    
    Args:
        date_str: A string representing a date in the specified format
        format_type: The format of the date string ("DD/MM/YYYY", "MM/DD/YYYY", or "YYYY/MM/DD")
        
    Returns:
        bool: True if the date is valid in the specified format, False otherwise
    """
    if format_type == "DD/MM/YYYY":
        return is_valid_date(date_str)
    elif format_type == "MM/DD/YYYY":
        if not re.match(r"^\d{2}/\d{2}/\d{4}$", date_str):
            return False
        month_str, day_str, year_str = date_str.split("/")
        try:
            day, month, year = int(day_str), int(month_str), int(year_str)
        except ValueError:
            return False
        return is_valid_date(f"{day:02d}/{month:02d}/{year:04d}")
    elif format_type == "YYYY/MM/DD":
        if not re.match(r"^\d{4}/\d{2}/\d{2}$", date_str):
            return False
        year_str, month_str, day_str = date_str.split("/")
        try:
            day, month, year = int(day_str), int(month_str), int(year_str)
        except ValueError:
            return False
        return is_valid_date(f"{day:02d}/{month:02d}/{year:04d}")
    return False
