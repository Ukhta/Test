import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

def generate_random_dataframe(rows=None, cols=None):
    """
    Generates a random DataFrame with random data.
    
    Parameters:
    - rows: Number of rows (default: random between 5 and 20)
    - cols: Number of columns (default: random between 3 and 8)
    
    Returns:
    - A pandas DataFrame with random data
    """
    if rows is None:
        rows = random.randint(5, 20)
    if cols is None:
        cols = random.randint(3, 8)
    
    # Generate column names
    column_names = [f'Column_{i+1}' for i in range(cols)]
    
    # Create random data
    data = {}
    for col_name in column_names:
        # Randomly decide the type of data for each column
        data_type = random.choice(['int', 'float', 'str', 'bool'])
        
        if data_type == 'int':
            data[col_name] = np.random.randint(1, 100, size=rows)
        elif data_type == 'float':
            data[col_name] = np.random.uniform(1.0, 100.0, size=rows)
        elif data_type == 'str':
            # Generate random strings
            choices = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta']
            data[col_name] = [random.choice(choices) for _ in range(rows)]
        elif data_type == 'bool':
            data[col_name] = [random.choice([True, False]) for _ in range(rows)]
    
    df = pd.DataFrame(data)
    return df

def visualize_dataframe(df):
    """
    Visualizes the DataFrame content in various ways depending on data types.
    """
    print("Generated DataFrame:")
    print(df.head(10))  # Show first 10 rows
    print(f"\nDataFrame Shape: {df.shape}")
    print(f"Data Types:\n{df.dtypes}")
    
    # Identify numeric columns for plotting
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) > 0:
        # Plot histograms for numeric columns
        num_plots = len(numeric_cols)
        cols_per_row = min(3, num_plots)  # Maximum 3 plots per row
        rows_needed = (num_plots + cols_per_row - 1) // cols_per_row
        
        fig, axes = plt.subplots(rows_needed, cols_per_row, figsize=(15, 5 * rows_needed))
        if num_plots == 1:
            axes = [axes]
        elif num_plots <= 3:
            axes = axes if isinstance(axes, (list, np.ndarray)) else [axes]
        else:
            axes = axes.flatten()
        
        for i, col in enumerate(numeric_cols):
            axes[i].hist(df[col], bins=15, edgecolor='black')
            axes[i].set_title(f'Distribution of {col}')
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Frequency')
        
        # Hide unused subplots
        for j in range(i + 1, len(axes)):
            axes[j].set_visible(False)
        
        plt.tight_layout()
        plt.show()
        
        # Create a correlation heatmap if there are at least 2 numeric columns
        if len(numeric_cols) >= 2:
            plt.figure(figsize=(10, 8))
            correlation_matrix = df[numeric_cols].corr()
            plt.imshow(correlation_matrix, cmap='coolwarm', interpolation='none', aspect='auto')
            plt.colorbar(label='Correlation')
            plt.title('Correlation Heatmap')
            
            # Add labels
            plt.xticks(range(len(numeric_cols)), numeric_cols, rotation=45)
            plt.yticks(range(len(numeric_cols)), numeric_cols)
            
            # Add correlation values to the heatmap
            for i in range(len(numeric_cols)):
                for j in range(len(numeric_cols)):
                    plt.text(j, i, f'{correlation_matrix.iloc[i, j]:.2f}', 
                             ha='center', va='center', color='white', fontweight='bold')
            
            plt.tight_layout()
            plt.show()
    else:
        print("\nNo numeric columns found for visualization.")
    
    # For categorical data, show value counts
    categorical_cols = df.select_dtypes(include=['object', 'bool']).columns.tolist()
    if len(categorical_cols) > 0:
        print("\nValue Counts for Categorical Columns:")
        for col in categorical_cols:
            print(f"\n{col}:")
            print(df[col].value_counts())

def main():
    """
    Main function to generate and visualize a random DataFrame.
    """
    print("Generating a random DataFrame...")
    df = generate_random_dataframe()
    
    print("Visualizing the DataFrame...")
    visualize_dataframe(df)

if __name__ == "__main__":
    main()