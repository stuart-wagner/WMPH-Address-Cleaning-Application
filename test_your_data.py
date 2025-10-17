#!/usr/bin/env python3
"""
Test script using your exact datasets to reproduce and fix the error
"""

import pandas as pd
import traceback

def create_test_datasets():
    """Create test datasets based on your actual data structure"""
    
    # Dataset 1 (from first image)
    dataset1 = pd.DataFrame({
        'CustomerID': ['C0001', 'C0002', 'C0003', 'C0004', 'C0005', 'C0006', 'C0007', 'C0008', 'C0009', 'C0010', 'C0011', 'C0012', 'C0013', 'C0014', 'C0015', 'C0016', 'C0017', 'C0018', 'C0019'],
        'FirstName': ['Michael', 'Carol', 'Joseph', 'John', 'Jamie', 'Michael', 'Carol', 'Joseph', 'John', 'Jamie', 'Michael', 'Carol', 'Joseph', 'John', 'Jamie', 'Michael', 'Carol', 'Joseph', 'John'],
        'LastName': ['Davis', 'Miller', 'Hays', 'Smith', 'Salinas', 'Davis', 'Miller', 'Hays', 'Smith', 'Salinas', 'Davis', 'Miller', 'Hays', 'Smith', 'Salinas', 'Davis', 'Miller', 'Hays', 'Smith'],
        'Gender': ['M', 'F', 'M', 'M', 'M', 'M', 'F', 'M', 'M', 'M', 'M', 'F', 'M', 'M', 'M', 'M', 'F', 'M', 'M'],
        'BirthDate': ['1996-09-11 00:00:00 UTC', '1959-08-18 00:00:00 UTC', '1998-05-16 00:00:00 UTC', '1992-06-18 00:00:00 UTC', '1992-06-18 00:00:00 UTC', '1996-09-11 00:00:00 UTC', '1959-08-18 00:00:00 UTC', '1998-05-16 00:00:00 UTC', '1992-06-18 00:00:00 UTC', '1992-06-18 00:00:00 UTC', '1996-09-11 00:00:00 UTC', '1959-08-18 00:00:00 UTC', '1998-05-16 00:00:00 UTC', '1992-06-18 00:00:00 UTC', '1992-06-18 00:00:00 UTC', '1996-09-11 00:00:00 UTC', '1959-08-18 00:00:00 UTC', '1998-05-16 00:00:00 UTC', '1992-06-18 00:00:00 UTC'],
        'City': ['Osbornepo', 'New Gabri', 'Port Allen', 'Stephanied', 'Port Kimbe', 'West Jasm', 'New Micha', 'West Lisav', 'West Caro', 'Jillianhave', 'East Sama', 'Quinnville', 'Murraybor', 'Osbornepo', 'New Gabri', 'Port Allen', 'Stephanied', 'Port Kimbe', 'West Jasm'],
        'JoinDate': ['2022-09-25 00:00:00 UTC', '2020-11-03 00:00:00 UTC', '2023-05-17 00:00:00 UTC', '2022-09-25 00:00:00 UTC', '2020-11-03 00:00:00 UTC', '2023-05-17 00:00:00 UTC', '2022-09-25 00:00:00 UTC', '2020-11-03 00:00:00 UTC', '2023-05-17 00:00:00 UTC', '2022-09-25 00:00:00 UTC', '2020-11-03 00:00:00 UTC', '2023-05-17 00:00:00 UTC', '2022-09-25 00:00:00 UTC', '2020-11-03 00:00:00 UTC', '2023-05-17 00:00:00 UTC', '2022-09-25 00:00:00 UTC', '2020-11-03 00:00:00 UTC', '2023-05-17 00:00:00 UTC', '2022-09-25 00:00:00 UTC'],
        'Joined2020': [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        'Initials': ['MD', 'CM', 'JH', 'JS', 'JS', 'MD', 'CM', 'JH', 'JS', 'JS', 'MD', 'CM', 'JH', 'JS', 'JS', 'MD', 'CM', 'JH', 'JS']
    })
    
    # Dataset 2 (from second image)
    dataset2 = pd.DataFrame({
        'Customerl': ['C001', 'C002', 'C003', 'C004', 'C005', 'C006', 'C007', 'C008', 'C009', 'C010', 'C011', 'C012', 'C013', 'C014', 'C015', 'C016'],
        'FirstName': ['Michael', 'Michael', 'Carol', 'Joseph', 'Jamie', 'Michael', 'Carol', 'Joseph', 'John', 'Jamie', 'Michael', 'Carol', 'Joseph', 'John', 'Jamie', 'Michael'],
        'LastName': ['Davis', 'Miller', 'Hays', 'Ward', 'Salinas', 'Davis', 'Miller', 'Hays', 'Smith', 'Salinas', 'Davis', 'Miller', 'Hays', 'Smith', 'Salinas', 'Davis'],
        'Gender': ['M', 'M', 'F', 'M', 'M', 'M', 'F', 'M', 'M', 'M', 'M', 'F', 'M', 'M', 'M', 'M'],
        'BirthDate': ['9/11/1996', '8/18/1959', '4/19/2005', '6/16/1992', '6/18/1992', '9/11/1996', '8/18/1959', '4/19/2005', '6/16/1992', '6/18/1992', '9/11/1996', '8/18/1959', '4/19/2005', '6/16/1992', '6/18/1992', '9/11/1996'],
        'City': ['Osbornepo', 'New Gabri', 'Port Allen', 'East Edgar', 'Port Kimbe', 'West Jasm', 'New Micha', 'West Lisav', 'West Caro', 'Jillianhave', 'East Sama', 'Quinnville', 'Murraybor', 'Osbornepo', 'New Gabri', 'Port Allen'],
        'JoinDate': ['9/25/2022', '11/3/2020', '2/12/2024', '9/9/2024', '2/24/2022', '9/25/2022', '11/3/2020', '2/12/2024', '9/9/2024', '2/24/2022', '9/25/2022', '11/3/2020', '2/12/2024', '9/9/2024', '2/24/2022', '9/25/2022']
    })
    
    return dataset1, dataset2

def test_combine_datasets():
    """Test the combine_datasets function with your data"""
    print("=" * 60)
    print("TESTING WITH YOUR EXACT DATA STRUCTURE")
    print("=" * 60)
    
    # Create test datasets
    dataset1, dataset2 = create_test_datasets()
    
    print("Dataset 1 Info:")
    print(f"  Shape: {dataset1.shape}")
    print(f"  Columns: {list(dataset1.columns)}")
    print(f"  Data types: {dataset1.dtypes.to_dict()}")
    print(f"  Sample data:")
    print(dataset1.head(2).to_string())
    
    print("\nDataset 2 Info:")
    print(f"  Shape: {dataset2.shape}")
    print(f"  Columns: {list(dataset2.columns)}")
    print(f"  Data types: {dataset2.dtypes.to_dict()}")
    print(f"  Sample data:")
    print(dataset2.head(2).to_string())
    
    # Set up datasets and info as they would be in the app
    datasets = {'dataset1': dataset1, 'dataset2': dataset2}
    dataset_info = {
        'dataset1': {'time_period': 'Q1 2023', 'service': 'Customer Service'},
        'dataset2': {'time_period': 'Q2 2023', 'service': 'Sales'}
    }
    
    print("\n" + "=" * 60)
    print("ATTEMPTING COMBINATION")
    print("=" * 60)
    
    try:
        # Import the actual combine_datasets function
        from data_joiner import DataJoinerApp
        app = DataJoinerApp()
        
        # Set up the app with test data
        app.datasets = datasets
        app.dataset_info = dataset_info
        
        # Try to combine
        combined = app.combine_datasets()
        
        if combined is not None:
            print("[SUCCESS] Datasets combined successfully")
            print(f"Combined shape: {combined.shape}")
            print(f"Combined columns: {list(combined.columns)}")
            print("\nSample of combined data:")
            print(combined.head(3).to_string())
            return True
        else:
            print("[FAILED] combine_datasets returned None")
            return False
            
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("Testing Data Joiner with your exact datasets...")
    
    success = test_combine_datasets()
    
    if success:
        print("\n[SUCCESS] The error should be fixed! Try running the application again.")
    else:
        print("\n[FAILED] The error still exists. We need to investigate further.")
        print("\nPossible issues:")
        print("1. Date format differences between datasets")
        print("2. Column name differences (CustomerID vs Customerl)")
        print("3. Data type inconsistencies")
        print("4. Missing values or special characters")

if __name__ == "__main__":
    main()
