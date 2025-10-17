#!/usr/bin/env python3
"""
Debug script to identify the exact cause of the "truth value of an index is ambiguous" error
"""

import pandas as pd
import traceback
import sys

def debug_combine_datasets(datasets, dataset_info):
    """Debug the combine_datasets function with detailed error reporting"""
    print("=" * 60)
    print("DEBUGGING DATASET COMBINATION")
    print("=" * 60)
    
    print(f"Number of datasets: {len(datasets)}")
    for name, df in datasets.items():
        print(f"\nDataset '{name}':")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)}")
        print(f"  Data types: {df.dtypes.to_dict()}")
        print(f"  Has info: {name in dataset_info}")
        if name in dataset_info:
            print(f"  Info: {dataset_info[name]}")
        print(f"  Sample data:")
        print(df.head(2).to_string())
    
    print("\n" + "=" * 60)
    print("ATTEMPTING COMBINATION")
    print("=" * 60)
    
    try:
        combined_dfs = []
        
        for name, df in datasets.items():
            print(f"\nProcessing dataset '{name}'...")
            
            if name not in dataset_info:
                print(f"  ERROR: No info found for dataset '{name}'")
                continue
                
            info = dataset_info[name]
            print(f"  Info: {info}")
            
            # Create a copy of the dataframe
            print(f"  Creating copy...")
            df_copy = df.copy()
            print(f"  Copy created successfully")
            
            # Add time period and service columns
            print(f"  Adding metadata columns...")
            df_copy['Time_Period'] = info['time_period']
            df_copy['Service'] = info['service']
            df_copy['Dataset_Name'] = name
            print(f"  Metadata columns added successfully")
            
            combined_dfs.append(df_copy)
            print(f"  Dataset '{name}' processed successfully")
        
        print(f"\nAll datasets processed. Total: {len(combined_dfs)}")
        
        if not combined_dfs:
            print("ERROR: No datasets to combine!")
            return None
            
        print("Attempting concatenation...")
        combined = pd.concat(combined_dfs, ignore_index=True)
        print(f"Concatenation successful! Result shape: {combined.shape}")
        
        return combined
        
    except Exception as e:
        print(f"\nERROR OCCURRED: {type(e).__name__}: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return None

def test_with_sample_data():
    """Test with sample data to ensure the function works"""
    print("Testing with sample data...")
    
    # Create sample datasets
    dataset1 = pd.DataFrame({
        'ID': [1, 2, 3],
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Value': [10, 20, 30]
    })
    
    dataset2 = pd.DataFrame({
        'ID': [4, 5, 6],
        'Name': ['David', 'Eve', 'Frank'],
        'Value': [40, 50, 60]
    })
    
    datasets = {'dataset1': dataset1, 'dataset2': dataset2}
    dataset_info = {
        'dataset1': {'time_period': 'Q1 2023', 'service': 'Service A'},
        'dataset2': {'time_period': 'Q2 2023', 'service': 'Service B'}
    }
    
    result = debug_combine_datasets(datasets, dataset_info)
    
    if result is not None:
        print("\n✅ Sample data test PASSED")
        return True
    else:
        print("\n❌ Sample data test FAILED")
        return False

def main():
    """Main debug function"""
    print("Data Joiner Debug Tool")
    print("This tool will help identify the cause of the 'truth value of an index is ambiguous' error")
    
    # First test with sample data
    if not test_with_sample_data():
        print("\n❌ Basic functionality is broken. Please check the code.")
        return
    
    print("\n" + "=" * 60)
    print("INSTRUCTIONS FOR DEBUGGING YOUR DATA")
    print("=" * 60)
    print("1. Load your datasets in the Data Joiner application")
    print("2. Add time period and service information for each dataset")
    print("3. Run this debug script with your actual data")
    print("4. The script will show exactly where the error occurs")
    print("\nTo debug your specific data, modify the 'datasets' and 'dataset_info'")
    print("variables in the main() function with your actual data.")

if __name__ == "__main__":
    main()


