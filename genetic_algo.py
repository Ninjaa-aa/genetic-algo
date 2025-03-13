import random
import re
from typing import List
import matplotlib.pyplot as plt

# Date validation function (for original problem)
def is_valid_date(date_str: str) -> bool:
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

# Categories for original problem
CATEGORIES = {
    "Valid Leap Year": lambda d, m, y: m == 2 and d == 29 and is_valid_date(f"{d:02d}/{m:02d}/{y:04d}"),
    "Valid 30-Day Month": lambda d, m, y: m in (4, 6, 9, 11) and d == 30 and is_valid_date(f"{d:02d}/{m:02d}/{y:04d}"),
    "Valid 31-Day Month": lambda d, m, y: m in (1, 3, 5, 7, 8, 10, 12) and d == 31 and is_valid_date(f"{d:02d}/{m:02d}/{y:04d}"),
    "Invalid Day > 31": lambda d, m, y: d > 31 and not is_valid_date(f"{d:02d}/{m:02d}/{y:04d}"),
    "Invalid Month > 12": lambda d, m, y: m > 12 and not is_valid_date(f"{d:02d}/{m:02d}/{y:04d}"),
    "Invalid Feb 29 Non-Leap": lambda d, m, y: m == 2 and d == 29 and not is_valid_date(f"{d:02d}/{m:02d}/{y:04d}"),
    "Boundary Min Year": lambda d, m, y: y == 0 and is_valid_date(f"{d:02d}/{m:02d}/{y:04d}"),
    "Boundary Max Year": lambda d, m, y: y == 9999 and is_valid_date(f"{d:02d}/{m:02d}/{y:04d}"),
}

# Chromosome representation
class TestCase:
    def __init__(self, day: int, month: int, year: int, category_dict=None, validator=None):
        self.day = day
        self.month = month
        self.year = year
        self.date_str = f"{day:02d}/{month:02d}/{year:04d}"
        self.category_dict = category_dict if category_dict else CATEGORIES
        self.validator = validator if validator else is_valid_date
        self.is_valid = self.validator(self.date_str)
        self.categories = [cat for cat, check in self.category_dict.items() if check(day, month, year)]

    def __str__(self):
        validity = "Valid" if self.is_valid else "Invalid"
        cats = ", ".join(self.categories) if self.categories else "General"
        return f"{self.date_str} ({validity}: {cats})"

    def __eq__(self, other):
        return self.date_str == other.date_str

# Population initialization
def initialize_population(size: int, category_dict=None, validator=None) -> List[TestCase]:
    population = [
        TestCase(29, 2, 2020, category_dict, validator),  # Valid Leap Year
        TestCase(31, 12, 9999, category_dict, validator),  # Valid 31-Day Month, Boundary Max Year
        TestCase(32, 5, 2023, category_dict, validator),  # Invalid Day > 31
    ]
    for _ in range(size - 3):
        day = random.randint(1, 40)
        month = random.randint(1, 15)
        year = random.choice([0, 9999, random.randint(0, 9999)])
        population.append(TestCase(day, month, year, category_dict, validator))
    return population

# Fitness function
def calculate_fitness(population: List[TestCase]) -> List[float]:
    covered_categories = set()
    redundant_count = 0
    for ind in population:
        new_cats = set(ind.categories) - covered_categories
        covered_categories.update(new_cats)
        redundant_count += len(set(ind.categories) & covered_categories) - len(new_cats)
    
    fitness = []
    for ind in population:
        unique_cats = set(ind.categories) - (covered_categories - set(ind.categories))
        if 1 + redundant_count > 0:
            ind_fitness = len(unique_cats) / (1 + redundant_count)
        else:
            ind_fitness = len(unique_cats)
        fitness.append(ind_fitness)
    return fitness

# Local Search (Hill-Climbing)
def local_search(population: List[TestCase], category_dict=None, validator=None, iterations=5) -> List[TestCase]:
    refined_population = population.copy()
    # Calculate initial coverage to identify missing categories
    covered_categories = set()
    for ind in refined_population:
        covered_categories.update(ind.categories)
    all_categories = set(category_dict.keys() if category_dict else CATEGORIES.keys())
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
            temp_coverage = len(temp_covered) / len(category_dict if category_dict else CATEGORIES) * 100
            current_coverage = len(covered_categories) / len(category_dict if category_dict else CATEGORIES) * 100
            
            # Keep the neighbor if it improves fitness or coverage
            if neighbor_fitness > best_fitness or temp_coverage > current_coverage:
                refined_population[i] = neighbor
                best_fitness = neighbor_fitness
                covered_categories = temp_covered  # Update covered categories
                missing_categories = all_categories - covered_categories  # Update missing categories
    
    return refined_population

# Selection (rank-based)
def select_parents(population: List[TestCase], fitness: List[float], num_parents: int) -> List[TestCase]:
    ranked = sorted(zip(population, fitness), key=lambda x: x[1], reverse=True)
    return [ind for ind, _ in ranked[:num_parents]]

# Crossover
def crossover(parent1: TestCase, parent2: TestCase) -> TestCase:
    day = random.choice([parent1.day, parent2.day])
    month = random.choice([parent1.month, parent2.month])
    year = random.choice([parent1.year, parent2.year])
    # Pass the category dictionary and validator from parent1
    return TestCase(day, month, year, parent1.category_dict, parent1.validator)

# Mutation
def mutate(individual: TestCase, mutation_rate: float = 0.15) -> TestCase:
    day, month, year = individual.day, individual.month, individual.year
    if random.random() < mutation_rate:
        day = random.choice([1, 28, 29, 30, 31, random.randint(32, 40)])
    if random.random() < mutation_rate:
        month = random.choice([1, 2, 4, 6, 9, 11, 12, random.randint(13, 15)])
    if random.random() < mutation_rate:
        year = random.choice([0, 9999, 2020, 2021, random.randint(0, 9999)])
    return TestCase(day, month, year, individual.category_dict, individual.validator)

# Genetic Algorithm
import matplotlib.pyplot as plt  # Add this import at the top of your file

def genetic_algorithm(pop_size: int = 50, generations: int = 100, category_dict=None, validator=None, use_local_search=False, instance_name="Original", force_full_generations=False) -> List[TestCase]:
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
        coverage = len(covered) / len(category_dict if category_dict else CATEGORIES) * 100
        coverages.append(coverage)  # Store the coverage for this generation
        
        if coverage >= 95 and not force_full_generations:
            print(f"Terminated at generation {gen + 1} with {coverage:.2f}% coverage")
            break
    
    # Apply local search if enabled
    if use_local_search:
        population = local_search(population, category_dict, validator)
        # Recalculate coverage after local search and append it
        covered = set()
        for ind in population:
            covered.update(ind.categories)
        coverage = len(covered) / len(category_dict if category_dict else CATEGORIES) * 100
        coverages.append(coverage)  # Add the final coverage after local search
        print(f"Coverage after local search: {coverage:.2f}%")
    
    # Plot coverage over generations
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(coverages) + 1), coverages, marker='o', linestyle='-', color='b', label="GA Evolution")
    if use_local_search and len(coverages) > 1:
        plt.plot(len(coverages), coverages[-1], marker='o', color='r', label="Post Local Search")
    plt.xlabel("Generation")
    plt.ylabel("Coverage (%)")
    plt.title(f"Coverage vs Generation ({instance_name})")
    plt.grid(True)
    plt.xticks(range(1, len(coverages) + 1))  # Show all generation numbers on x-axis
    plt.ylim(0, 100)  # Set y-axis range from 0 to 100
    plt.legend()  # Add legend if local search is applied
    # Save plot with instance-specific filename
    plot_filename = f"coverage_plot_{instance_name.replace(' ', '_').lower()}_{'local_search' if use_local_search else 'baseline'}.png"
    plt.savefig(plot_filename)
    plt.close()  # Close the plot to free memory
    
    return population

# Main execution
def run_instance(category_dict=None, validator=None, instance_name="Original", valid_min=10, invalid_min=10, boundary_min=5, use_local_search=False, force_full_generations=False):
    population = genetic_algorithm(category_dict=category_dict, validator=validator, use_local_search=use_local_search, instance_name=instance_name, force_full_generations=force_full_generations)
    fitness = calculate_fitness(population)
    best_cases = sorted(zip(population, fitness), key=lambda x: x[1], reverse=True)
    
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
    
    while len(valid_cases) < valid_min:
        tc = TestCase(random.randint(1, 28), random.randint(1, 12), random.randint(1, 9998), category_dict, validator)
        if tc.date_str not in seen:
            seen.add(tc.date_str)
            valid_cases.append(tc)
    while len(invalid_cases) < invalid_min:
        tc = TestCase(random.randint(32, 40), random.randint(1, 15), random.randint(0, 9999), category_dict, validator)
        if tc.date_str not in seen:
            seen.add(tc.date_str)
            invalid_cases.append(tc)
    while len(boundary_cases) < boundary_min:
        tc = TestCase(random.randint(1, 31), random.randint(1, 12), random.choice([0, 9999]), category_dict, validator)
        if tc.date_str not in seen:
            seen.add(tc.date_str)
            boundary_cases.append(tc)

    print(f"\nResults for {instance_name}:")
    print("Valid Cases:")
    for tc in valid_cases:
        print(tc)
    print("\nInvalid Cases:")
    for tc in invalid_cases:
        print(tc)
    print("\nBoundary Cases:")
    for tc in boundary_cases:
        print(tc)
    
    covered = set()
    for tc, _ in best_cases:
        covered.update(tc.categories)
    coverage = len(covered) / len(category_dict if category_dict else CATEGORIES) * 100
    print(f"\nCoverage Achieved: {coverage:.2f}%")
    
    return coverage, valid_cases + invalid_cases + boundary_cases

# Sample Problem Instance 1: Basic Date Validation
def validator_instance_1(date_str: str) -> bool:
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

CATEGORIES_INSTANCE_1 = {
    "Valid 30-Day Month": lambda d, m, y: m in (4, 6, 9, 11) and d == 30 and validator_instance_1(f"{d:02d}/{m:02d}/{y:04d}"),
    "Invalid Day > 31": lambda d, m, y: d > 31 and not validator_instance_1(f"{d:02d}/{m:02d}/{y:04d}"),
    "Invalid Month > 12": lambda d, m, y: m > 12 and not validator_instance_1(f"{d:02d}/{m:02d}/{y:04d}"),
    "Invalid 30-Day Month": lambda d, m, y: m in (4, 6, 9, 11) and d > 30 and not validator_instance_1(f"{d:02d}/{m:02d}/{y:04d}"),
    "Boundary 31-Day Month": lambda d, m, y: d == 31 and m == 1 and y == 2023 and validator_instance_1(f"{d:02d}/{m:02d}/{y:04d}"),
}

# Sample Problem Instance 2: Advanced Leap Year & Boundaries
def validator_instance_2(date_str: str) -> bool:
    return is_valid_date(date_str)  # Same as original validator

CATEGORIES_INSTANCE_2 = {
    "Valid Leap Year": lambda d, m, y: m == 2 and d == 29 and validator_instance_2(f"{d:02d}/{m:02d}/{y:04d}"),
    "Valid Non-Leap Feb": lambda d, m, y: m == 2 and d == 28 and y == 1900 and validator_instance_2(f"{d:02d}/{m:02d}/{y:04d}"),
    "Invalid Feb 29 Non-Leap": lambda d, m, y: m == 2 and d == 29 and not validator_instance_2(f"{d:02d}/{m:02d}/{y:04d}"),
    "Invalid Feb 29 1900": lambda d, m, y: m == 2 and d == 29 and y == 1900 and not validator_instance_2(f"{d:02d}/{m:02d}/{y:04d}"),
    "Boundary Min Year": lambda d, m, y: y == 0 and validator_instance_2(f"{d:02d}/{m:02d}/{y:04d}"),
    "Boundary Max Year": lambda d, m, y: y == 9999 and validator_instance_2(f"{d:02d}/{m:02d}/{y:04d}"),
}

# Sample Problem Instance 3: Complex Month-Day Combinations
def validator_instance_3(date_str: str) -> bool:
    return is_valid_date(date_str)  # Same as original validator

CATEGORIES_INSTANCE_3 = {
    "Invalid Feb 30": lambda d, m, y: m == 2 and d == 30 and not validator_instance_3(f"{d:02d}/{m:02d}/{y:04d}"),
    "Invalid Apr 31": lambda d, m, y: m == 4 and d == 31 and not validator_instance_3(f"{d:02d}/{m:02d}/{y:04d}"),
    "Invalid Jun 31": lambda d, m, y: m == 6 and d == 31 and not validator_instance_3(f"{d:02d}/{m:02d}/{y:04d}"),
    "Invalid Sep 31": lambda d, m, y: m == 9 and d == 31 and not validator_instance_3(f"{d:02d}/{m:02d}/{y:04d}"),
    "Invalid Nov 31": lambda d, m, y: m == 11 and d == 31 and not validator_instance_3(f"{d:02d}/{m:02d}/{y:04d}"),
}

# Sample Problem Instance 4: Format Variations
def validator_instance_4(date_str: str, format_type: str) -> bool:
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

class TestCaseFormat:
    def __init__(self, day: int, month: int, year: int, format_type: str):
        self.day = day
        self.month = month
        self.year = year
        self.format_type = format_type
        if format_type == "DD/MM/YYYY":
            self.date_str = f"{day:02d}/{month:02d}/{year:04d}"
        elif format_type == "MM/DD/YYYY":
            self.date_str = f"{month:02d}/{day:02d}/{year:04d}"
        elif format_type == "YYYY/MM/DD":
            self.date_str = f"{year:04d}/{month:02d}/{day:02d}"
        self.is_valid = validator_instance_4(self.date_str, format_type)
        self.categories = [cat for cat, check in CATEGORIES_INSTANCE_4.items() if check(day, month, year, format_type)]

    def __str__(self):
        validity = "Valid" if self.is_valid else "Invalid"
        cats = ", ".join(self.categories) if self.categories else "General"
        return f"{self.date_str} ({self.format_type}) ({validity}: {cats})"

    def __eq__(self, other):
        return self.date_str == other.date_str and self.format_type == other.format_type

CATEGORIES_INSTANCE_4 = {
    "Valid DD/MM/YYYY": lambda d, m, y, f: f == "DD/MM/YYYY" and validator_instance_4(f"{d:02d}/{m:02d}/{y:04d}", f),
    "Valid MM/DD/YYYY": lambda d, m, y, f: f == "MM/DD/YYYY" and validator_instance_4(f"{m:02d}/{d:02d}/{y:04d}", f),
    "Valid YYYY/MM/DD": lambda d, m, y, f: f == "YYYY/MM/DD" and validator_instance_4(f"{y:04d}/{m:02d}/{d:02d}", f),
    "Invalid Ambiguous": lambda d, m, y, f: d <= 12 and m <= 12 and f in ("DD/MM/YYYY", "MM/DD/YYYY") and not validator_instance_4(f"{d:02d}/{m:02d}/{y:04d}", "DD/MM/YYYY") and not validator_instance_4(f"{m:02d}/{d:02d}/{y:04d}", "MM/DD/YYYY"),
}

def initialize_population_instance_4(size: int) -> List[TestCaseFormat]:
    population = [
        TestCaseFormat(15, 5, 2023, "DD/MM/YYYY"),
        TestCaseFormat(5, 15, 2023, "MM/DD/YYYY"),
        TestCaseFormat(15, 5, 2023, "YYYY/MM/DD"),
        TestCaseFormat(5, 6, 2023, "DD/MM/YYYY"),  # Ambiguous
    ]
    formats = ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY/MM/DD"]
    for _ in range(size - 4):
        day = random.randint(1, 40)
        month = random.randint(1, 15)
        year = random.randint(0, 9999)
        format_type = random.choice(formats)
        population.append(TestCaseFormat(day, month, year, format_type))
    return population

def calculate_fitness_instance_4(population: List[TestCaseFormat]) -> List[float]:
    covered_categories = set()
    redundant_count = 0
    for ind in population:
        new_cats = set(ind.categories) - covered_categories
        covered_categories.update(new_cats)
        redundant_count += len(set(ind.categories) & covered_categories) - len(new_cats)
    
    fitness = []
    for ind in population:
        unique_cats = set(ind.categories) - (covered_categories - set(ind.categories))
        if 1 + redundant_count > 0:
            ind_fitness = len(unique_cats) / (1 + redundant_count)
        else:
            ind_fitness = len(unique_cats)
        fitness.append(ind_fitness)
    return fitness

def local_search_instance_4(population: List[TestCaseFormat], iterations=5) -> List[TestCaseFormat]:
    refined_population = population.copy()
    # Calculate initial coverage to identify missing categories
    covered_categories = set()
    for ind in refined_population:
        covered_categories.update(ind.categories)
    all_categories = set(CATEGORIES_INSTANCE_4.keys())
    missing_categories = all_categories - covered_categories

    formats = ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY/MM/DD"]
    for i in range(len(refined_population)):
        current = refined_population[i]
        best_fitness = calculate_fitness_instance_4(refined_population)[i]
        for _ in range(iterations):
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
            
            day = max(1, min(40, day))
            month = max(1, min(15, month))
            year = max(0, min(9999, year))
            neighbor = TestCaseFormat(day, month, year, format_type)
            
            temp_population = refined_population.copy()
            temp_population[i] = neighbor
            neighbor_fitness = calculate_fitness_instance_4(temp_population)[i]
            
            # Check if the neighbor improves overall coverage
            temp_covered = set()
            for ind in temp_population:
                temp_covered.update(ind.categories)
            temp_coverage = len(temp_covered) / len(CATEGORIES_INSTANCE_4) * 100
            current_coverage = len(covered_categories) / len(CATEGORIES_INSTANCE_4) * 100
            
            if neighbor_fitness > best_fitness or temp_coverage > current_coverage:
                refined_population[i] = neighbor
                best_fitness = neighbor_fitness
                covered_categories = temp_covered
                missing_categories = all_categories - covered_categories
    
    return refined_population

def genetic_algorithm_instance_4(pop_size: int = 50, generations: int = 100, use_local_search=False, instance_name="Instance 4", force_full_generations=False) -> List[TestCaseFormat]:
    population = initialize_population_instance_4(pop_size)
    coverages = []  # List to store coverage values per generation

    for gen in range(generations):
        fitness = calculate_fitness_instance_4(population)
        parents = select_parents(population, fitness, pop_size // 2)
        offspring = []
        for _ in range(pop_size - len(parents)):
            p1, p2 = random.sample(parents, 2)
            day = random.choice([p1.day, p2.day])
            month = random.choice([p1.month, p2.month])
            year = random.choice([p1.year, p2.year])
            format_type = random.choice([p1.format_type, p2.format_type])
            child = TestCaseFormat(day, month, year, format_type)
            day = random.choice([1, 28, 29, 30, 31, random.randint(32, 40)])
            month = random.choice([1, 2, 4, 6, 9, 11, 12, random.randint(13, 15)])
            year = random.choice([0, 9999, 2020, 2021, random.randint(0, 9999)])
            child = TestCaseFormat(day, month, year, child.format_type)
            offspring.append(child)
        population = parents + offspring
        
        covered = set()
        for ind in population:
            covered.update(ind.categories)
        coverage = len(covered) / len(CATEGORIES_INSTANCE_4) * 100
        coverages.append(coverage)
        if coverage >= 95 and not force_full_generations:
            print(f"Terminated at generation {gen + 1} with {coverage:.2f}% coverage")
            break
    
    if use_local_search:
        population = local_search_instance_4(population)
        covered = set()
        for ind in population:
            covered.update(ind.categories)
        coverage = len(covered) / len(CATEGORIES_INSTANCE_4) * 100
        coverages.append(coverage)
        print(f"Coverage after local search: {coverage:.2f}%")
    
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(coverages) + 1), coverages, marker='o', linestyle='-', color='b', label="GA Evolution")
    if use_local_search and len(coverages) > 1:
        plt.plot(len(coverages), coverages[-1], marker='o', color='r', label="Post Local Search")
    plt.xlabel("Generation")
    plt.ylabel("Coverage (%)")
    plt.title(f"Coverage vs Generation ({instance_name})")
    plt.grid(True)
    plt.xticks(range(1, len(coverages) + 1))
    plt.ylim(0, 100)
    plt.legend()  # Add legend if local search is applied
    plot_filename = f"coverage_plot_{instance_name.replace(' ', '_').lower()}_{'local_search' if use_local_search else 'baseline'}.png"
    plt.savefig(plot_filename)
    plt.close()
    
    return population

def run_instance_4(use_local_search=False, instance_name="Instance 4", force_full_generations=False):
    population = genetic_algorithm_instance_4(use_local_search=use_local_search, instance_name=instance_name, force_full_generations=force_full_generations)
    fitness = calculate_fitness_instance_4(population)
    best_cases = sorted(zip(population, fitness), key=lambda x: x[1], reverse=True)
    
    valid_cases = []
    invalid_cases = []
    seen = set()
    
    for tc, _ in best_cases:
        if (tc.date_str, tc.format_type) not in seen:
            seen.add((tc.date_str, tc.format_type))
            if tc.is_valid and len(valid_cases) < 10:
                valid_cases.append(tc)
            elif not tc.is_valid and len(invalid_cases) < 10:
                invalid_cases.append(tc)
    
    while len(valid_cases) < 10:
        tc = TestCaseFormat(random.randint(1, 28), random.randint(1, 12), random.randint(1, 9998), "DD/MM/YYYY")
        if (tc.date_str, tc.format_type) not in seen:
            seen.add((tc.date_str, tc.format_type))
            valid_cases.append(tc)
    while len(invalid_cases) < 10:
        tc = TestCaseFormat(random.randint(32, 40), random.randint(1, 15), random.randint(0, 9999), "DD/MM/YYYY")
        if (tc.date_str, tc.format_type) not in seen:
            seen.add((tc.date_str, tc.format_type))
            invalid_cases.append(tc)

    print(f"\nResults for {instance_name}:")
    print("Valid Cases:")
    for tc in valid_cases:
        print(tc)
    print("\nInvalid Cases:")
    for tc in invalid_cases:
        print(tc)
    
    covered = set()
    for tc, _ in best_cases:
        covered.update(tc.categories)
    coverage = len(covered) / len(CATEGORIES_INSTANCE_4) * 100
    print(f"\nCoverage Achieved: {coverage:.2f}%")
    
    return coverage, valid_cases + invalid_cases

# Main execution across all instances
def main():
    results = {}
    
    # Original Problem (Baseline GA)
    print("\n=== Original Problem (Baseline GA) ===")
    coverage, test_cases = run_instance(instance_name="Original Baseline", force_full_generations=True)
    results["Original (Baseline)"] = coverage
    
    # Original Problem (GA + Local Search)
    print("\n=== Original Problem (GA + Local Search) ===")
    coverage, test_cases = run_instance(use_local_search=True, instance_name="Original GA + Local Search", force_full_generations=True)
    results["Original (GA + Local Search)"] = coverage
    
    # Instance 1 (Baseline GA)
    print("\n=== Instance 1: Basic Date Validation (Baseline GA) ===")
    coverage, test_cases = run_instance(category_dict=CATEGORIES_INSTANCE_1, validator=validator_instance_1, instance_name="Instance 1 Baseline", valid_min=5, invalid_min=5, boundary_min=1)
    results["Instance 1 (Baseline)"] = coverage
    
    # Instance 1 (GA + Local Search)
    print("\n=== Instance 1: Basic Date Validation (GA + Local Search) ===")
    coverage, test_cases = run_instance(category_dict=CATEGORIES_INSTANCE_1, validator=validator_instance_1, instance_name="Instance 1 GA + Local Search", valid_min=5, invalid_min=5, boundary_min=1, use_local_search=True)
    results["Instance 1 (GA + Local Search)"] = coverage
    
    # Instance 2 (Baseline GA)
    print("\n=== Instance 2: Advanced Leap Year & Boundaries (Baseline GA) ===")
    coverage, test_cases = run_instance(category_dict=CATEGORIES_INSTANCE_2, validator=validator_instance_2, instance_name="Instance 2 Baseline", valid_min=10, invalid_min=10, boundary_min=2)
    results["Instance 2 (Baseline)"] = coverage
    
    # Instance 2 (GA + Local Search)
    print("\n=== Instance 2: Advanced Leap Year & Boundaries (GA + Local Search) ===")
    coverage, test_cases = run_instance(category_dict=CATEGORIES_INSTANCE_2, validator=validator_instance_2, instance_name="Instance 2 GA + Local Search", valid_min=10, invalid_min=10, boundary_min=2, use_local_search=True)
    results["Instance 2 (GA + Local Search)"] = coverage
    
    # Instance 3 (Baseline GA)
    print("\n=== Instance 3: Complex Month-Day Combinations (Baseline GA) ===")
    coverage, test_cases = run_instance(category_dict=CATEGORIES_INSTANCE_3, validator=validator_instance_3, instance_name="Instance 3 Baseline", valid_min=0, invalid_min=10, boundary_min=0)
    results["Instance 3 (Baseline)"] = coverage
    
    # Instance 3 (GA + Local Search)
    print("\n=== Instance 3: Complex Month-Day Combinations (GA + Local Search) ===")
    coverage, test_cases = run_instance(category_dict=CATEGORIES_INSTANCE_3, validator=validator_instance_3, instance_name="Instance 3 GA + Local Search", valid_min=0, invalid_min=10, boundary_min=0, use_local_search=True)
    results["Instance 3 (GA + Local Search)"] = coverage
    
    # Instance 4 (Baseline GA)
    print("\n=== Instance 4: Format Variations (Baseline GA) ===")
    coverage, test_cases = run_instance_4(use_local_search=False, instance_name="Instance 4 Baseline", force_full_generations=True)
    results["Instance 4 (Baseline)"] = coverage
    
    # Instance 4 (GA + Local Search)
    print("\n=== Instance 4: Format Variations (GA + Local Search) ===")
    coverage, test_cases = run_instance_4(use_local_search=True, instance_name="Instance 4 GA + Local Search", force_full_generations=True)
    results["Instance 4 (GA + Local Search)"] = coverage
    
    # Print comparison
    print("\n=== Coverage Comparison ===")
    for instance, coverage in results.items():
        print(f"{instance}: {coverage:.2f}%")
    
    # Save all test cases to CSV
    with open("test_cases_all.csv", "w") as f:
        f.write("Instance,Date,Format,Validity,Categories\n")
        for instance, (coverage, test_cases) in [
            ("Original (Baseline)", run_instance(use_local_search=False, instance_name="Original Baseline", force_full_generations=True)),
            ("Original (GA + Local Search)", run_instance(use_local_search=True, instance_name="Original GA + Local Search", force_full_generations=True)),
            ("Instance 1 (Baseline)", run_instance(category_dict=CATEGORIES_INSTANCE_1, validator=validator_instance_1, instance_name="Instance 1 Baseline", valid_min=5, invalid_min=5, boundary_min=1)),
            ("Instance 1 (GA + Local Search)", run_instance(category_dict=CATEGORIES_INSTANCE_1, validator=validator_instance_1, instance_name="Instance 1 GA + Local Search", valid_min=5, invalid_min=5, boundary_min=1, use_local_search=True)),
            ("Instance 2 (Baseline)", run_instance(category_dict=CATEGORIES_INSTANCE_2, validator=validator_instance_2, instance_name="Instance 2 Baseline", valid_min=10, invalid_min=10, boundary_min=2)),
            ("Instance 2 (GA + Local Search)", run_instance(category_dict=CATEGORIES_INSTANCE_2, validator=validator_instance_2, instance_name="Instance 2 GA + Local Search", valid_min=10, invalid_min=10, boundary_min=2, use_local_search=True)),
            ("Instance 3 (Baseline)", run_instance(category_dict=CATEGORIES_INSTANCE_3, validator=validator_instance_3, instance_name="Instance 3 Baseline", valid_min=0, invalid_min=10, boundary_min=0)),
            ("Instance 3 (GA + Local Search)", run_instance(category_dict=CATEGORIES_INSTANCE_3, validator=validator_instance_3, instance_name="Instance 3 GA + Local Search", valid_min=0, invalid_min=10, boundary_min=0, use_local_search=True)),
            ("Instance 4 (Baseline)", run_instance_4(use_local_search=False, instance_name="Instance 4 Baseline", force_full_generations=True)),
            ("Instance 4 (GA + Local Search)", run_instance_4(use_local_search=True, instance_name="Instance 4 GA + Local Search", force_full_generations=True)),
        ]:
            for tc in test_cases:
                format_type = getattr(tc, "format_type", "DD/MM/YYYY")
                f.write(f"{instance},{tc.date_str},{format_type},{tc.is_valid},{';'.join(tc.categories)}\n")

if __name__ == "__main__":
    main()