import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

def generate_random_dataframe(rows=10, cols=5):
    """
    Generates a random DataFrame with specified number of rows and columns.
    
    Args:
        rows (int): Number of rows in the DataFrame
        cols (int): Number of columns in the DataFrame
    
    Returns:
        pd.DataFrame: A DataFrame with random values
    """
    # Generate column names
    col_names = [f'Column_{i+1}' for i in range(cols)]
    
    # Generate random data
    data = {}
    for col in col_names:
        # Randomly choose data type for each column
        dtype_choice = random.choice(['int', 'float', 'str', 'bool'])
        
        if dtype_choice == 'int':
            data[col] = np.random.randint(1, 100, size=rows)
        elif dtype_choice == 'float':
            data[col] = np.random.uniform(0, 100, size=rows)
        elif dtype_choice == 'str':
            # Generate random strings
            choices = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta']
            data[col] = [random.choice(choices) for _ in range(rows)]
        else:  # bool
            data[col] = np.random.choice([True, False], size=rows)
    
    df = pd.DataFrame(data)
    return df

def visualize_dataframe(df):
    """
    Visualizes the DataFrame in multiple ways depending on the data types.
    
    Args:
        df (pd.DataFrame): The DataFrame to visualize
    """
    print("Generated DataFrame:")
    print(df.head(10))
    print(f"\nDataFrame Info:")
    print(df.info())
    
    # Select numeric columns for visualization
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols:
        # Create subplots for numeric columns
        n_numeric = len(numeric_cols)
        fig, axes = plt.subplots(2, min(3, n_numeric), figsize=(15, 8))
        if n_numeric == 1:
            axes = np.array([axes,])
        axes = axes.flatten() if n_numeric > 1 else [axes]
        
        for i, col in enumerate(numeric_cols[:min(len(axes), len(numeric_cols))]):
            axes[i].hist(df[col], bins=15, edgecolor='black')
            axes[i].set_title(f'Distribution of {col}')
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Frequency')
        
        # Hide extra subplots if any
        for j in range(i + 1, len(axes)):
            axes[j].axis('off')
        
        plt.tight_layout()
        plt.show()
        
        # Correlation heatmap for numeric columns if we have at least 2 numeric columns
        if len(numeric_cols) > 1:
            plt.figure(figsize=(8, 6))
            correlation_matrix = df[numeric_cols].corr()
            plt.imshow(correlation_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
            plt.colorbar(label='Correlation Coefficient')
            plt.title('Correlation Heatmap')
            # Add labels for columns
            plt.xticks(range(len(numeric_cols)), numeric_cols, rotation=45)
            plt.yticks(range(len(numeric_cols)), numeric_cols)
            
            # Add correlation values to the heatmap
            for i in range(len(numeric_cols)):
                for j in range(len(numeric_cols)):
                    plt.text(j, i, f'{correlation_matrix.iloc[i, j]:.2f}', 
                             ha='center', va='center', color='white' if abs(correlation_matrix.iloc[i, j]) > 0.5 else 'black')
            
            plt.tight_layout()
            plt.show()
    
    # For non-numeric columns, show value counts
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
    
    if categorical_cols:
        n_categorical = len(categorical_cols)
        fig, axes = plt.subplots(1, n_categorical, figsize=(5*n_categorical, 5))
        if n_categorical == 1:
            axes = [axes]
        
        for i, col in enumerate(categorical_cols):
            value_counts = df[col].value_counts()
            axes[i].bar(value_counts.index.astype(str), value_counts.values)
            axes[i].set_title(f'Value Counts for {col}')
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Count')
            axes[i].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()

def main():
    print("Generating a random DataFrame...")
    
    # Generate random DataFrame
    df = generate_random_dataframe(rows=15, cols=6)
    
    # Visualize the DataFrame
    visualize_dataframe(df)
    
    print("\nVisualization complete!")

if __name__ == "__main__":
    main()