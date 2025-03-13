# Genetic Algorithm for Test Case Generation

This project implements a genetic algorithm approach to automatically generate test cases for date validation functions. The algorithm evolves a population of test cases to achieve maximum coverage of predefined categories of date inputs, combining global exploration with local search techniques.

## Project Structure

```
genetic_algo_project/
├── src/
│   ├── core/                 # Core genetic algorithm functionality
│   │   ├── test_case.py      # Test case representation classes
│   │   ├── genetic_algorithm.py  # GA and local search implementation
│   │   └── fitness.py        # Fitness calculation and operators
│   ├── instances/            # Problem instances
│   │   ├── original.py       # Original test problem
│   │   ├── instance1.py      # Basic date validation
│   │   ├── instance2.py      # Advanced leap year & boundaries
│   │   ├── instance3.py      # Complex month-day combinations
│   │   └── instance4.py      # Format variations
│   ├── utils/                # Utility functions
│   │   ├── validation.py     # Date validation functions
│   │   └── visualization.py  # Plotting and reporting
│   ├── runners/              # Execution functions
│   │   ├── run_instance.py   # Runner for standard problem instances
│   │   └── run_instance4.py  # Runner for format-specific instance
│   └── assets/               # Generated assets
│       ├── images/           # Coverage plots and visualizations
│       └── data/             # Generated test case data
├── main.py                   # Main execution script
├── genetic_algo.py           # Original monolithic implementation
├── generate_report_pdf.py    # PDF report generation script
├── GA_Test_Case_Generation_Report.pdf # Generated PDF report
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## Problem Instances

The project includes several test problem instances:

1. **Original Problem**: Full date validation with multiple categories including leap years and boundary cases
2. **Instance 1**: Basic date validation focused on day/month constraints
3. **Instance 2**: Advanced leap year validation and boundary testing
4. **Instance 3**: Complex month-day combinations testing invalid day-month pairs
5. **Instance 4**: Format variations testing different date formats (DD/MM/YYYY, MM/DD/YYYY, YYYY/MM/DD)

## Features

- Genetic algorithm with specialized crossover and mutation operators
- Local search optimization to refine solutions after GA convergence
- Test case categorization for better coverage analysis
- Enhanced fitness function that balances coverage and diversity
- Visualization of coverage improvement over generations
- Comprehensive PDF report generation
- Configurable parameters for each problem instance
- Early termination or full generations run options

## Requirements

- Python 3.6+
- matplotlib
- numpy
- fpdf (for PDF report generation)
- reportlab (alternative PDF generation)

## Installation

1. Clone this repository
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Genetic Algorithm

Run the main script to execute the genetic algorithm on all problem instances:

```bash
python main.py
```

### Generating the PDF Report

Generate a comprehensive PDF report of the genetic algorithm test case generation approach:

```bash
python generate_report_pdf.py
```

## Output

The system produces:

- Test case reports for each problem instance
- Coverage plots showing the evolution of coverage over generations (stored in `src/assets/images/`)
- A CSV file with all generated test cases (stored in `src/assets/data/`)
- A coverage comparison between baseline GA and GA with local search
- A comprehensive PDF report documenting the approach and results

## Visualizations

The project includes enhanced visualizations:

- **Coverage Evolution Plots**: Line graphs showing how coverage improves over generations
- **Local Search Impact**: Highlights the improvement from local search optimization
- **Comparison Visualizations**: Comparing baseline GA vs. GA with local search

## Genetic Algorithm Details

### Chromosome Representation
Each test case (chromosome) consists of:
- day (1-31 or higher for invalid cases)
- month (1-12 or higher for invalid cases)
- year (0-9999)
- date_str (formatted representation)
- categories (what test categories it belongs to)

### Genetic Operators
- **Selection**: Rank-based selection of the fittest individuals
- **Crossover**: Component-wise recombination of date elements
- **Mutation**: Targeted mutation with biases toward boundary values
- **Local Search**: Hill-climbing refinement after GA convergence

### Fitness Function
The fitness function prioritizes individuals that cover previously uncovered categories while penalizing redundancy in the population.

## Customization

To customize the genetic algorithm or add new problem instances:

1. Define your categories in a new file in the `instances/` directory
2. Create a validation function in `utils/validation.py`
3. Update the `main.py` to include your new problem instance
4. Adjust parameters like:
   - Population size
   - Number of generations
   - Mutation rate
   - Local search iterations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributors

- Developed by the AI Testing Team
"# genetic-algo" 
