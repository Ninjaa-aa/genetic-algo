import random
from typing import List, Dict, Tuple, Any, Optional, Set
from ..core.test_case import TestCase
from ..core.genetic_algorithm import genetic_algorithm
from ..core.fitness import calculate_fitness
from ..utils.visualization import plot_coverage, print_test_cases
from ..instances.original import CATEGORIES

def run_instance(
    category_dict=None, 
    validator=None, 
    instance_name="Original", 
    valid_min=10, 
    invalid_min=10, 
    boundary_min=5, 
    use_local_search=False,
    pop_size=50,
    generations=100,
    force_full_generations=False
) -> Tuple[float, List[TestCase]]:
    """
    Run the genetic algorithm on a problem instance.
    
    Args:
        category_dict: Dictionary mapping category names to validation functions
        validator: The validation function to use
        instance_name: Name of the problem instance
        valid_min: Minimum number of valid test cases to generate
        invalid_min: Minimum number of invalid test cases to generate
        boundary_min: Minimum number of boundary test cases to generate
        use_local_search: Whether to apply local search to refine the population
        pop_size: Size of the population
        generations: Maximum number of generations
        force_full_generations: Whether to run all generations regardless of coverage
        
    Returns:
        Tuple of (coverage, test_cases) where coverage is the percentage coverage achieved
        and test_cases is the list of generated test cases
    """
    # Use provided category dictionary or default to CATEGORIES
    cat_dict = category_dict if category_dict else CATEGORIES
    
    # Run the genetic algorithm
    population, coverages = genetic_algorithm(
        pop_size=pop_size,
        generations=generations,
        category_dict=cat_dict, 
        validator=validator, 
        use_local_search=use_local_search, 
        instance_name=instance_name,
        force_full_generations=force_full_generations
    )
    
    # Calculate fitness for selecting the best test cases
    fitness = calculate_fitness(population)
    best_cases = sorted(zip(population, fitness), key=lambda x: x[1], reverse=True)
    
    # Separate the test cases into different categories
    valid_cases = []
    invalid_cases = []
    boundary_cases = []
    seen = set()
    
    for tc, _ in best_cases:
        if tc.date_str not in seen:
            seen.add(tc.date_str)
            if tc.is_valid and len(valid_cases) < valid_min:
                valid_cases.append(tc)
            elif not tc.is_valid and len(invalid_cases) < invalid_min:
                invalid_cases.append(tc)
            if any(c.startswith("Boundary") for c in tc.categories) and len(boundary_cases) < boundary_min:
                boundary_cases.append(tc)
    
    # If we don't have enough of each type, generate random ones
    while len(valid_cases) < valid_min:
        tc = TestCase(random.randint(1, 28), random.randint(1, 12), random.randint(1, 9998), cat_dict, validator)
        if tc.date_str not in seen and tc.is_valid:
            seen.add(tc.date_str)
            valid_cases.append(tc)
    
    while len(invalid_cases) < invalid_min:
        tc = TestCase(random.randint(32, 40), random.randint(1, 15), random.randint(0, 9999), cat_dict, validator)
        if tc.date_str not in seen and not tc.is_valid:
            seen.add(tc.date_str)
            invalid_cases.append(tc)
    
    while len(boundary_cases) < boundary_min and boundary_min > 0:
        tc = TestCase(random.randint(1, 31), random.randint(1, 12), random.choice([0, 9999]), cat_dict, validator)
        if tc.date_str not in seen:
            seen.add(tc.date_str)
            boundary_cases.append(tc)

    # Print the results
    print_test_cases(valid_cases, invalid_cases, boundary_cases, instance_name)
    
    # Plot the coverage
    plot_coverage(coverages, instance_name, use_local_search)
    
    # Calculate the final coverage
    covered = set()
    for tc, _ in best_cases:
        covered.update(tc.categories)
    coverage = len(covered) / len(cat_dict) * 100
    print(f"\nCoverage Achieved: {coverage:.2f}%")
    
    return coverage, valid_cases + invalid_cases + boundary_cases
