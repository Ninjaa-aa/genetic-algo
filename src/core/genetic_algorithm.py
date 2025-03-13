from typing import List, Dict, Any, Tuple, Set
import random
from .test_case import TestCase, TestCaseFormat, initialize_population, initialize_population_instance_4
from .fitness import calculate_fitness, calculate_fitness_instance_4, select_parents, crossover, mutate

def local_search(population: List[TestCase], category_dict=None, validator=None, iterations=5) -> List[TestCase]:
    """
    Apply local search to refine a population of test cases.
    
    Args:
        population: List of TestCase objects
        category_dict: Dictionary mapping category names to validation functions
        validator: The validation function to use
        iterations: Number of iterations for each test case
        
    Returns:
        Refined list of TestCase objects
    """
    refined_population = population.copy()
    
    # Calculate initial coverage to identify missing categories
    covered_categories = set()
    for ind in refined_population:
        covered_categories.update(ind.categories)
    
    all_categories = set(category_dict.keys() if category_dict else [])
    missing_categories = all_categories - covered_categories

    for i in range(len(refined_population)):
        current = refined_population[i]
        best_fitness = calculate_fitness(refined_population)[i]
        
        for _ in range(iterations):
            # Generate a neighbor by perturbing day, month, or year
            day = current.day + random.choice([-1, 0, 1])
            month = current.month + random.choice([-1, 0, 1])
            year = current.year + random.choice([-1, 0, 1, -100, 100])
            
            # If there are missing categories, bias perturbations towards them
            if missing_categories:
                # Example: Bias towards invalid months (>12) or invalid days (>31) for certain categories
                if any("Invalid Month > 12" in cat for cat in missing_categories):
                    month = random.randint(13, 15)
                if any("Invalid Day > 31" in cat for cat in missing_categories):
                    day = random.randint(32, 40)
                if any("Boundary Min Year" in cat for cat in missing_categories):
                    year = 0
                if any("Boundary Max Year" in cat for cat in missing_categories):
                    year = 9999
                if any("Invalid Feb 29" in cat for cat in missing_categories):
                    month = 2
                    day = 29
                    year = random.choice([1900, 2021])  # Non-leap years
                if any("Valid Leap Year" in cat for cat in missing_categories):
                    month = 2
                    day = 29
                    year = 2020  # Leap year
            
            # Ensure values are within valid ranges
            day = max(1, min(40, day))
            month = max(1, min(15, month))
            year = max(0, min(9999, year))
            
            neighbor = TestCase(day, month, year, category_dict, validator)
            
            # Replace the current individual in the population temporarily
            temp_population = refined_population.copy()
            temp_population[i] = neighbor
            neighbor_fitness = calculate_fitness(temp_population)[i]
            
            # Check if the neighbor improves overall coverage
            temp_covered = set()
            for ind in temp_population:
                temp_covered.update(ind.categories)
            
            temp_coverage = len(temp_covered) / len(category_dict if category_dict else []) * 100 if category_dict else 0
            current_coverage = len(covered_categories) / len(category_dict if category_dict else []) * 100 if category_dict else 0
            
            # Keep the neighbor if it improves fitness or coverage
            if neighbor_fitness > best_fitness or temp_coverage > current_coverage:
                refined_population[i] = neighbor
                best_fitness = neighbor_fitness
                covered_categories = temp_covered  # Update covered categories
                missing_categories = all_categories - covered_categories  # Update missing categories
    
    return refined_population

def local_search_instance_4(population: List[TestCaseFormat], category_dict=None, validator=None, iterations=5) -> List[TestCaseFormat]:
    """
    Apply local search to refine a population of format-specific test cases.
    
    Args:
        population: List of TestCaseFormat objects
        category_dict: Dictionary mapping category names to validation functions
        validator: The validation function to use
        iterations: Number of iterations for each test case
        
    Returns:
        Refined list of TestCaseFormat objects
    """
    refined_population = population.copy()
    
    # Calculate initial coverage to identify missing categories
    covered_categories = set()
    for ind in refined_population:
        covered_categories.update(ind.categories)
    
    all_categories = set(category_dict.keys() if category_dict else [])
    missing_categories = all_categories - covered_categories

    formats = ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY/MM/DD"]
    
    for i in range(len(refined_population)):
        current = refined_population[i]
        best_fitness = calculate_fitness_instance_4(refined_population)[i]
        
        for _ in range(iterations):
            # Generate a neighbor by perturbing day, month, year, or format
            day = current.day + random.choice([-1, 0, 1])
            month = current.month + random.choice([-1, 0, 1])
            year = current.year + random.choice([-1, 0, 1, -100, 100])
            
            # Bias towards missing categories
            if missing_categories:
                if "Invalid Ambiguous" in missing_categories:
                    day = random.randint(1, 12)  # Ambiguous dates (e.g., 05/06 or 06/05)
                    month = random.randint(1, 12)
                    format_type = random.choice(["DD/MM/YYYY", "MM/DD/YYYY"])
                else:
                    format_type = random.choice(formats)
            else:
                format_type = random.choice(formats)
            
            # Ensure values are within valid ranges
            day = max(1, min(40, day))
            month = max(1, min(15, month))
            year = max(0, min(9999, year))
            
            neighbor = TestCaseFormat(day, month, year, format_type, category_dict, validator)
            
            # Replace the current individual in the population temporarily
            temp_population = refined_population.copy()
            temp_population[i] = neighbor
            neighbor_fitness = calculate_fitness_instance_4(temp_population)[i]
            
            # Check if the neighbor improves overall coverage
            temp_covered = set()
            for ind in temp_population:
                temp_covered.update(ind.categories)
            
            temp_coverage = len(temp_covered) / len(category_dict if category_dict else []) * 100 if category_dict else 0
            current_coverage = len(covered_categories) / len(category_dict if category_dict else []) * 100 if category_dict else 0
            
            # Keep the neighbor if it improves fitness or coverage
            if neighbor_fitness > best_fitness or temp_coverage > current_coverage:
                refined_population[i] = neighbor
                best_fitness = neighbor_fitness
                covered_categories = temp_covered  # Update covered categories
                missing_categories = all_categories - covered_categories  # Update missing categories
    
    return refined_population

def genetic_algorithm(
    pop_size: int = 50, 
    generations: int = 100, 
    category_dict=None,
    validator=None,
    use_local_search=False, 
    instance_name="Original",
    force_full_generations=False
) -> Tuple[List[TestCase], List[float]]:
    """
    Run the genetic algorithm to generate test cases.
    
    Args:
        pop_size: Size of the population
        generations: Maximum number of generations
        category_dict: Dictionary mapping category names to validation functions
        validator: The validation function to use
        use_local_search: Whether to apply local search to refine the population
        instance_name: Name of the problem instance
        force_full_generations: Whether to run all generations regardless of coverage
        
    Returns:
        Tuple of (population, coverages) where population is the final list of TestCase objects
        and coverages is a list of coverage values per generation
    """
    population = initialize_population(pop_size, category_dict, validator)
    coverages = []  # List to store coverage values per generation

    for gen in range(generations):
        fitness = calculate_fitness(population)
        parents = select_parents(population, fitness, pop_size // 2)
        offspring = []
        
        for _ in range(pop_size - len(parents)):
            p1, p2 = random.sample(parents, 2)
            child = crossover(p1, p2)
            child = mutate(child)
            offspring.append(child)
        
        population = parents + offspring
        
        # Calculate coverage for the current generation
        covered = set()
        for ind in population:
            covered.update(ind.categories)
        
        coverage = len(covered) / len(category_dict) * 100 if category_dict else 0
        coverages.append(coverage)  # Store the coverage for this generation
        
        if coverage >= 95 and not force_full_generations:
            print(f"Terminated at generation {gen + 1} with {coverage:.2f}% coverage")
            break
    
    # Apply local search if enabled
    if use_local_search:
        population = local_search(population, category_dict, validator)
        
        # Recalculate coverage after local search
        covered = set()
        for ind in population:
            covered.update(ind.categories)
        
        coverage = len(covered) / len(category_dict) * 100 if category_dict else 0
        coverages.append(coverage)  # Add the final coverage after local search
        print(f"Coverage after local search: {coverage:.2f}%")
    
    # The visualization is handled by the utility function in utils/visualization.py
    
    return population, coverages

def genetic_algorithm_instance_4(
    pop_size: int = 50, 
    generations: int = 100, 
    category_dict=None,
    validator=None,
    use_local_search=False, 
    instance_name="Instance 4",
    force_full_generations=False
) -> Tuple[List[TestCaseFormat], List[float]]:
    """
    Run the genetic algorithm to generate format-specific test cases.
    
    Args:
        pop_size: Size of the population
        generations: Maximum number of generations
        category_dict: Dictionary mapping category names to validation functions
        validator: The validation function to use
        use_local_search: Whether to apply local search to refine the population
        instance_name: Name of the problem instance
        force_full_generations: Whether to run all generations regardless of coverage
        
    Returns:
        Tuple of (population, coverages) where population is the final list of TestCaseFormat objects
        and coverages is a list of coverage values per generation
    """
    population = initialize_population_instance_4(pop_size, category_dict, validator)
    coverages = []  # List to store coverage values per generation

    for gen in range(generations):
        fitness = calculate_fitness_instance_4(population, category_dict)
        parents = select_parents(population, fitness, pop_size // 2)
        offspring = []
        
        for _ in range(pop_size - len(parents)):
            p1, p2 = random.sample(parents, 2)
            
            # Crossover
            day = random.choice([p1.day, p2.day])
            month = random.choice([p1.month, p2.month])
            year = random.choice([p1.year, p2.year])
            format_type = random.choice([p1.format_type, p2.format_type])
            
            child = TestCaseFormat(day, month, year, format_type, category_dict, validator)
            
            # Mutation
            if random.random() < 0.15:  # mutation rate
                day = random.choice([1, 28, 29, 30, 31, random.randint(32, 40)])
            if random.random() < 0.15:
                month = random.choice([1, 2, 4, 6, 9, 11, 12, random.randint(13, 15)])
            if random.random() < 0.15:
                year = random.choice([0, 9999, 2020, 2021, random.randint(0, 9999)])
            if random.random() < 0.15:
                format_type = random.choice(["DD/MM/YYYY", "MM/DD/YYYY", "YYYY/MM/DD"])
            
            child = TestCaseFormat(day, month, year, format_type, category_dict, validator)
            offspring.append(child)
        
        population = parents + offspring
        
        # Calculate coverage for the current generation
        covered = set()
        for ind in population:
            covered.update(ind.categories)
        
        coverage = len(covered) / len(category_dict) * 100 if category_dict else 0
        coverages.append(coverage)  # Store the coverage for this generation
        
        if coverage >= 95 and not force_full_generations:
            print(f"Terminated at generation {gen + 1} with {coverage:.2f}% coverage")
            break
    
    # Apply local search if enabled
    if use_local_search:
        population = local_search_instance_4(population, category_dict, validator, 5)
        
        # Recalculate coverage after local search
        covered = set()
        for ind in population:
            covered.update(ind.categories)
        
        coverage = len(covered) / len(category_dict) * 100 if category_dict else 0
        coverages.append(coverage)  # Add the final coverage after local search
        print(f"Coverage after local search: {coverage:.2f}%")
    
    # The visualization is handled by the utility function in utils/visualization.py
    
    return population, coverages
