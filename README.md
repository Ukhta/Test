# Random DataFrame Visualization Project

## Overview
This project generates random DataFrames with mixed data types and provides visualization capabilities. It includes functionality for creating random datasets and visualizing them with histograms, correlation heatmaps, and value count analysis.

## Features
- Generate random DataFrames with configurable rows and columns
- Support for multiple data types: integers, floats, strings, and booleans
- Automatic visualization of numeric columns with histograms
- Correlation heatmap generation for numeric columns
- Value count analysis for categorical columns
- Dynamic layout adjustment for plots

## Files
- `random_dataframe_visualization.py`: Main Python script containing the DataFrame generation and visualization functions
- `README.md`: This documentation file

## Prerequisites
- Python 3.x
- Required packages:
  - pandas
  - numpy
  - matplotlib
  - random (built-in)

Install dependencies with:
```bash
pip install pandas numpy matplotlib
```

## Usage
Run the script directly to generate and visualize a random DataFrame:
```bash
python random_dataframe_visualization.py
```

Or import the functions in your own code:
```python
from random_dataframe_visualization import generate_random_dataframe, visualize_dataframe

# Generate a custom DataFrame
df = generate_random_dataframe(rows=15, cols=5)
visualize_dataframe(df)
```

## Functions
- `generate_random_dataframe(rows=None, cols=None)`: Creates a random DataFrame with specified dimensions (defaults to random sizes)
- `visualize_dataframe(df)`: Displays the DataFrame and creates visualizations
- `main()`: Entry point function demonstrating the functionality

## Contributing
Feel free to modify the script to customize the data generation patterns, visualization styles, or add new features.

## License
No license specified - consider adding licensing information as appropriate for your project.