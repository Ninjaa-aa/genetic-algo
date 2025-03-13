import os
import sys

# Add the parent directory to the sys.path to allow importing from src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.validation import is_valid_date, validator_instance_1, validator_instance_2, validator_instance_3, validator_instance_4
from src.utils.visualization import save_test_cases_to_csv, print_coverage_comparison
from src.runners.run_instance import run_instance
from src.runners.run_instance4 import run_instance_4

# Import instance-specific configuration
from src.instances.original import CATEGORIES as ORIGINAL_CATEGORIES, DEFAULT_PARAMS as ORIGINAL_PARAMS
from src.instances.instance1 import CATEGORIES as CATEGORIES_INSTANCE_1, DEFAULT_PARAMS as INSTANCE1_PARAMS
from src.instances.instance2 import CATEGORIES as CATEGORIES_INSTANCE_2, DEFAULT_PARAMS as INSTANCE2_PARAMS
from src.instances.instance3 import CATEGORIES as CATEGORIES_INSTANCE_3, DEFAULT_PARAMS as INSTANCE3_PARAMS
from src.instances.instance4 import CATEGORIES as CATEGORIES_INSTANCE_4, DEFAULT_PARAMS as INSTANCE4_PARAMS

def main():
    """Execute the genetic algorithm on all problem instances."""
    results = {}
    instance_results = {}
    
    print("\n=== Original Problem (Baseline GA) ===")
    coverage, test_cases = run_instance(
        category_dict=ORIGINAL_CATEGORIES, 
        validator=is_valid_date, 
        instance_name="Original Baseline",
        force_full_generations=True,
        **{k: v for k, v in ORIGINAL_PARAMS.items() if k not in ['instance_name']}
    )
    results["Original (Baseline)"] = coverage
    instance_results["Original (Baseline)"] = (coverage, test_cases)
    
    print("\n=== Original Problem (GA + Local Search) ===")
    coverage, test_cases = run_instance(
        category_dict=ORIGINAL_CATEGORIES, 
        validator=is_valid_date, 
        use_local_search=True, 
        instance_name="Original GA + Local Search",
        force_full_generations=True,
        **{k: v for k, v in ORIGINAL_PARAMS.items() if k not in ['instance_name']}
    )
    results["Original (GA + Local Search)"] = coverage
    instance_results["Original (GA + Local Search)"] = (coverage, test_cases)
    
    print("\n=== Instance 1: Basic Date Validation (Baseline GA) ===")
    coverage, test_cases = run_instance(
        category_dict=CATEGORIES_INSTANCE_1, 
        validator=validator_instance_1, 
        instance_name="Instance 1 Baseline",
        **{k: v for k, v in INSTANCE1_PARAMS.items() if k not in ['instance_name']}
    )
    results["Instance 1 (Baseline)"] = coverage
    instance_results["Instance 1 (Baseline)"] = (coverage, test_cases)
    
    print("\n=== Instance 1: Basic Date Validation (GA + Local Search) ===")
    coverage, test_cases = run_instance(
        category_dict=CATEGORIES_INSTANCE_1, 
        validator=validator_instance_1, 
        use_local_search=True, 
        instance_name="Instance 1 GA + Local Search",
        **{k: v for k, v in INSTANCE1_PARAMS.items() if k not in ['instance_name']}
    )
    results["Instance 1 (GA + Local Search)"] = coverage
    instance_results["Instance 1 (GA + Local Search)"] = (coverage, test_cases)
    
    print("\n=== Instance 2: Advanced Leap Year & Boundaries (Baseline GA) ===")
    coverage, test_cases = run_instance(
        category_dict=CATEGORIES_INSTANCE_2, 
        validator=validator_instance_2, 
        instance_name="Instance 2 Baseline",
        **{k: v for k, v in INSTANCE2_PARAMS.items() if k not in ['instance_name']}
    )
    results["Instance 2 (Baseline)"] = coverage
    instance_results["Instance 2 (Baseline)"] = (coverage, test_cases)
    
    print("\n=== Instance 2: Advanced Leap Year & Boundaries (GA + Local Search) ===")
    coverage, test_cases = run_instance(
        category_dict=CATEGORIES_INSTANCE_2, 
        validator=validator_instance_2, 
        use_local_search=True, 
        instance_name="Instance 2 GA + Local Search",
        **{k: v for k, v in INSTANCE2_PARAMS.items() if k not in ['instance_name']}
    )
    results["Instance 2 (GA + Local Search)"] = coverage
    instance_results["Instance 2 (GA + Local Search)"] = (coverage, test_cases)
    
    print("\n=== Instance 3: Complex Month-Day Combinations (Baseline GA) ===")
    coverage, test_cases = run_instance(
        category_dict=CATEGORIES_INSTANCE_3, 
        validator=validator_instance_3, 
        instance_name="Instance 3 Baseline",
        **{k: v for k, v in INSTANCE3_PARAMS.items() if k not in ['instance_name']}
    )
    results["Instance 3 (Baseline)"] = coverage
    instance_results["Instance 3 (Baseline)"] = (coverage, test_cases)
    
    print("\n=== Instance 3: Complex Month-Day Combinations (GA + Local Search) ===")
    coverage, test_cases = run_instance(
        category_dict=CATEGORIES_INSTANCE_3, 
        validator=validator_instance_3, 
        use_local_search=True, 
        instance_name="Instance 3 GA + Local Search",
        **{k: v for k, v in INSTANCE3_PARAMS.items() if k not in ['instance_name']}
    )
    results["Instance 3 (GA + Local Search)"] = coverage
    instance_results["Instance 3 (GA + Local Search)"] = (coverage, test_cases)
    
    print("\n=== Instance 4: Format Variations (Baseline GA) ===")
    coverage, test_cases = run_instance_4(
        category_dict=CATEGORIES_INSTANCE_4, 
        validator=validator_instance_4, 
        instance_name="Instance 4 Baseline",
        force_full_generations=True,
        **{k: v for k, v in INSTANCE4_PARAMS.items() if k not in ['instance_name']}
    )
    results["Instance 4 (Baseline)"] = coverage
    instance_results["Instance 4 (Baseline)"] = (coverage, test_cases)
    
    print("\n=== Instance 4: Format Variations (GA + Local Search) ===")
    coverage, test_cases = run_instance_4(
        category_dict=CATEGORIES_INSTANCE_4, 
        validator=validator_instance_4, 
        use_local_search=True, 
        instance_name="Instance 4 GA + Local Search",
        force_full_generations=True,
        **{k: v for k, v in INSTANCE4_PARAMS.items() if k not in ['instance_name']}
    )
    results["Instance 4 (GA + Local Search)"] = coverage
    instance_results["Instance 4 (GA + Local Search)"] = (coverage, test_cases)
    
    # Print comparison of coverage across all instances
    print_coverage_comparison(results)
    
    # Save all test cases to CSV
    save_test_cases_to_csv(instance_results, "test_cases_all.csv")

if __name__ == "__main__":
    main()
