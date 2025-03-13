import matplotlib
matplotlib.use('Agg')  # Use Agg backend (non-interactive)
import matplotlib.pyplot as plt
from typing import List, Dict, Any
import os

def plot_coverage(coverages: List[float], instance_name: str, use_local_search: bool = False) -> str:
    """
    Plot coverage over generations and save the plot to a file.
    
    Args:
        coverages: List of coverage values per generation
        instance_name: Name of the problem instance
        use_local_search: Whether local search was used
        
    Returns:
        The filename of the saved plot
    """
    plt.figure(figsize=(10, 6))
    
    # Plot the main GA evolution line
    plt.plot(range(1, len(coverages) + 1), coverages, marker='o', linestyle='-', color='b', label="GA Evolution")
    
    # If local search was used, highlight the last point with a different color
    if use_local_search and len(coverages) > 1:
        plt.plot(len(coverages), coverages[-1], marker='o', color='r', markersize=10, label="Post Local Search")
    
    plt.xlabel("Generation")
    plt.ylabel("Coverage (%)")
    plt.title(f"Coverage vs Generation ({instance_name})")
    plt.grid(True)
    plt.xticks(range(1, len(coverages) + 1))  # Show all generation numbers on x-axis
    plt.ylim(0, 100)  # Set y-axis range from 0 to 100
    plt.legend()  # Add a legend to distinguish between GA evolution and post local search
    
    # Ensure directory exists
    images_dir = os.path.join("src", "assets", "images")
    os.makedirs(images_dir, exist_ok=True)
    
    # Save plot with instance-specific filename
    plot_filename = f"coverage_plot_{instance_name.replace(' ', '_').lower()}_{'local_search' if use_local_search else 'baseline'}.png"
    full_path = os.path.join(images_dir, plot_filename)
    plt.savefig(full_path)
    plt.close()  # Close the plot to free memory
    
    return full_path

def print_test_cases(valid_cases: List[Any], invalid_cases: List[Any], boundary_cases: List[Any] = None, instance_name: str = ""):
    """
    Print test cases to the console.
    
    Args:
        valid_cases: List of valid test cases
        invalid_cases: List of invalid test cases
        boundary_cases: List of boundary test cases (optional)
        instance_name: Name of the problem instance
    """
    print(f"\nResults for {instance_name}:")
    
    print("Valid Cases:")
    for tc in valid_cases:
        print(tc)
    
    print("\nInvalid Cases:")
    for tc in invalid_cases:
        print(tc)
    
    if boundary_cases:
        print("\nBoundary Cases:")
        for tc in boundary_cases:
            print(tc)

def save_test_cases_to_csv(
    instance_results: Dict[str, tuple], 
    filename: str = "test_cases_all.csv"
):
    """
    Save all test cases to a CSV file.
    
    Args:
        instance_results: Dictionary mapping instance names to tuples of (coverage, test_cases)
        filename: Output CSV filename
    """
    # Ensure directory exists
    data_dir = os.path.join("src", "assets", "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Create full path for the CSV file
    full_path = os.path.join(data_dir, filename)
    
    with open(full_path, "w") as f:
        f.write("Instance,Date,Format,Validity,Categories\n")
        
        for instance_name, (coverage, test_cases) in instance_results.items():
            for tc in test_cases:
                format_type = getattr(tc, "format_type", "DD/MM/YYYY")
                validity = "Valid" if tc.is_valid else "Invalid"
                categories = ";".join(tc.categories) if tc.categories else ""
                f.write(f"{instance_name},{tc.date_str},{format_type},{validity},{categories}\n")
        
    print(f"Test cases saved to {full_path}")

def print_coverage_comparison(results: Dict[str, float]):
    """
    Print a comparison of coverage achieved by different approaches.
    
    Args:
        results: Dictionary mapping instance names to coverage values
    """
    print("\n=== Coverage Comparison ===")
    for instance, coverage in results.items():
        print(f"{instance}: {coverage:.2f}%")
