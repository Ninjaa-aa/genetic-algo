from typing import List, Set, Any
import random
from .test_case import TestCase, TestCaseFormat

def calculate_fitness(population: List[TestCase]) -> List[float]:
    """
    Calculate fitness values for a population of test cases.
    
    Args:
        population: List of TestCase objects
        
    Returns:
        List of fitness values corresponding to each test case
    """
    covered_categories = set()
    redundant_count = 0
    
    # First pass to calculate coverage metrics
    for ind in population:
        new_cats = set(ind.categories) - covered_categories
        covered_categories.update(new_cats)
        redundant_count += len(set(ind.categories) & covered_categories) - len(new_cats)
    
    # Second pass to calculate fitness for each individual
    fitness = []
    for ind in population:
        unique_cats = set(ind.categories) - (covered_categories - set(ind.categories))
        if 1 + redundant_count > 0:
            ind_fitness = len(unique_cats) / (1 + redundant_count)
        else:
            ind_fitness = len(unique_cats)
        fitness.append(ind_fitness)
    
    return fitness

def calculate_fitness_instance_4(population: List[TestCaseFormat], category_dict=None) -> List[float]:
    """
    Calculate fitness values for a population of format-specific test cases.
    
    Args:
        population: List of TestCaseFormat objects
        category_dict: Dictionary of category definitions to use for fitness calculation
        
    Returns:
        List of fitness values corresponding to each test case
    """
    covered_categories = set()
    redundant_count = 0
    
    # First pass to calculate coverage metrics
    for ind in population:
        new_cats = set(ind.categories) - covered_categories
        covered_categories.update(new_cats)
        redundant_count += len(set(ind.categories) & covered_categories) - len(new_cats)
    
    # Second pass to calculate fitness for each individual
    fitness = []
    for ind in population:
        unique_cats = set(ind.categories) - (covered_categories - set(ind.categories))
        if 1 + redundant_count > 0:
            ind_fitness = len(unique_cats) / (1 + redundant_count)
        else:
            ind_fitness = len(unique_cats)
        fitness.append(ind_fitness)
    
    return fitness

def select_parents(population: List[Any], fitness: List[float], num_parents: int) -> List[Any]:
    """
    Select parent test cases for reproduction based on fitness.
    
    Args:
        population: List of test case objects
        fitness: List of fitness values corresponding to each test case
        num_parents: Number of parents to select
        
    Returns:
        List of selected parent test cases
    """
    ranked = sorted(zip(population, fitness), key=lambda x: x[1], reverse=True)
    return [ind for ind, _ in ranked[:num_parents]]

def crossover(parent1: TestCase, parent2: TestCase) -> TestCase:
    """
    Perform crossover between two parent test cases.
    
    Args:
        parent1: First parent test case
        parent2: Second parent test case
        
    Returns:
        New test case resulting from crossover
    """
    day = random.choice([parent1.day, parent2.day])
    month = random.choice([parent1.month, parent2.month])
    year = random.choice([parent1.year, parent2.year])
    
    # Pass the category dictionary and validator from parent1
    return TestCase(day, month, year, parent1.category_dict, parent1.validator)

def mutate(individual: TestCase, mutation_rate: float = 0.15) -> TestCase:
    """
    Mutate a test case.
    
    Args:
        individual: The test case to mutate
        mutation_rate: Probability of mutation for each component
        
    Returns:
        Mutated test case
    """
    day, month, year = individual.day, individual.month, individual.year
    
    if random.random() < mutation_rate:
        day = random.choice([1, 28, 29, 30, 31, random.randint(32, 40)])
    if random.random() < mutation_rate:
        month = random.choice([1, 2, 4, 6, 9, 11, 12, random.randint(13, 15)])
    if random.random() < mutation_rate:
        year = random.choice([0, 9999, 2020, 2021, random.randint(0, 9999)])
    
    return TestCase(day, month, year, individual.category_dict, individual.validator)
