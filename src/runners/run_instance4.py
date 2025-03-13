import random
from typing import List, Dict, Tuple, Any, Optional, Set
from ..core.test_case import TestCaseFormat
from ..core.genetic_algorithm import genetic_algorithm_instance_4
from ..core.fitness import calculate_fitness_instance_4
from ..utils.visualization import plot_coverage, print_test_cases
from ..instances.instance4 import CATEGORIES as CATEGORIES_INSTANCE_4

def run_instance_4(
    category_dict=None, 
    validator=None, 
    instance_name="Instance 4", 
    valid_min=10, 
    invalid_min=10, 
    use_local_search=False,
    pop_size=50,
    generations=100,
    force_full_generations=False
) -> Tuple[float, List[TestCaseFormat]]:
    """
    Run the genetic algorithm on the format variation problem instance.
    
    Args:
        category_dict: Dictionary mapping category names to validation functions
        validator: The validation function to use
        instance_name: Name of the problem instance
        valid_min: Minimum number of valid test cases to generate
        invalid_min: Minimum number of invalid test cases to generate
        use_local_search: Whether to apply local search to refine the population
        pop_size: Size of the population
        generations: Maximum number of generations
        force_full_generations: Whether to run all generations regardless of coverage
        
    Returns:
        Tuple of (coverage, test_cases) where coverage is the percentage coverage achieved
        and test_cases is the list of generated test cases
    """
    # Use provided category dictionary or default to CATEGORIES_INSTANCE_4
    cat_dict = category_dict if category_dict else CATEGORIES_INSTANCE_4
    
    # Run the genetic algorithm
    population, coverages = genetic_algorithm_instance_4(
        pop_size=pop_size,
        generations=generations,
        category_dict=cat_dict, 
        validator=validator, 
        use_local_search=use_local_search, 
        instance_name=instance_name,
        force_full_generations=force_full_generations
    )
    
    # Calculate fitness for selecting the best test cases
    fitness = calculate_fitness_instance_4(population, cat_dict)
    best_cases = sorted(zip(population, fitness), key=lambda x: x[1], reverse=True)
    
    # Separate the test cases into different categories
    valid_cases = []
    invalid_cases = []
    seen = set()
    
    for tc, _ in best_cases:
        if (tc.date_str, tc.format_type) not in seen:
            seen.add((tc.date_str, tc.format_type))
            if tc.is_valid and len(valid_cases) < valid_min:
                valid_cases.append(tc)
            elif not tc.is_valid and len(invalid_cases) < invalid_min:
                invalid_cases.append(tc)
    
    # If we don't have enough of each type, generate random ones
    formats = ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY/MM/DD"]
    
    while len(valid_cases) < valid_min:
        format_type = random.choice(formats) if category_dict else "DD/MM/YYYY"
        tc = TestCaseFormat(
            random.randint(1, 28), 
            random.randint(1, 12), 
            random.randint(1, 9998), 
            format_type,
            cat_dict, 
            validator
        )
        if (tc.date_str, tc.format_type) not in seen and tc.is_valid:
            seen.add((tc.date_str, tc.format_type))
            valid_cases.append(tc)
    
    while len(invalid_cases) < invalid_min:
        format_type = random.choice(formats) if category_dict else "DD/MM/YYYY"
        tc = TestCaseFormat(
            random.randint(32, 40), 
            random.randint(1, 15), 
            random.randint(0, 9999), 
            format_type,
            cat_dict, 
            validator
        )
        if (tc.date_str, tc.format_type) not in seen and not tc.is_valid:
            seen.add((tc.date_str, tc.format_type))
            invalid_cases.append(tc)

    # Print the results
    print_test_cases(valid_cases, invalid_cases, None, instance_name)
    
    # Plot the coverage
    plot_coverage(coverages, instance_name, use_local_search)
    
    # Calculate the final coverage
    covered = set()
    for tc, _ in best_cases:
        covered.update(tc.categories)
    coverage = len(covered) / len(cat_dict) * 100
    print(f"\nCoverage Achieved: {coverage:.2f}%")
    
    return coverage, valid_cases + invalid_cases 