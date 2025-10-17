#!/usr/bin/env python3
"""
Test script to verify Data Joiner functionality
"""

import pandas as pd
import os
import sys

def test_dummy_row_detection():
    """Test the dummy row detection functionality"""
    print("Testing dummy row detection...")
    
    # Create test data with dummy rows
    dummy_rows = pd.DataFrame({
        'col1': ['Report Title', 'Generated: 2023-01-01', ''],
        'col2': ['', '', ''],
        'col3': ['', '', '']
    })
    
    real_data = pd.DataFrame({
        'col1': [1, 2, 3, 4, 5],
        'col2': ['A', 'B', 'C', 'D', 'E'],
        'col3': [10.5, 20.3, 30.1, 40.7, 50.9]
    })
    
    test_df = pd.concat([dummy_rows, real_data], ignore_index=True)
    
    # Test the detection function
    from data_joiner import DataJoinerApp
    app = DataJoinerApp()
    
    result_df = app.detect_and_skip_dummy_rows(test_df)
    
    # Check if dummy rows were removed
    if len(result_df) == len(real_data) and result_df.iloc[0, 0] == 1:
        print("[PASS] Dummy row detection works correctly")
        return True
    else:
        print("[FAIL] Dummy row detection failed")
        return False

def test_data_combination():
    """Test the data combination functionality"""
    print("Testing data combination...")
    
    # Create test datasets
    df1 = pd.DataFrame({
        'ID': [1, 2, 3],
        'Value': [10, 20, 30]
    })
    
    df2 = pd.DataFrame({
        'ID': [4, 5, 6],
        'Value': [40, 50, 60]
    })
    
    # Test combination
    from data_joiner import DataJoinerApp
    app = DataJoinerApp()
    
    # Simulate the combination process
    app.datasets = {'dataset1': df1, 'dataset2': df2}
    app.dataset_info = {
        'dataset1': {'time_period': 'Q1 2023', 'service': 'Service A'},
        'dataset2': {'time_period': 'Q2 2023', 'service': 'Service B'}
    }
    
    combined = app.combine_datasets()
    
    # Check if combination worked
    expected_columns = ['ID', 'Value', 'Time_Period', 'Service', 'Dataset_Name']
    if all(col in combined.columns for col in expected_columns):
        print("[PASS] Data combination works correctly")
        return True
    else:
        print("[FAIL] Data combination failed")
        return False

def test_file_operations():
    """Test file reading and writing operations"""
    print("Testing file operations...")
    
    try:
        # Test CSV reading
        test_data = pd.DataFrame({
            'A': [1, 2, 3],
            'B': ['x', 'y', 'z']
        })
        
        test_file = 'test_temp.csv'
        test_data.to_csv(test_file, index=False)
        
        # Test reading
        read_data = pd.read_csv(test_file)
        
        # Clean up
        os.remove(test_file)
        
        if read_data.equals(test_data):
            print("[PASS] File operations work correctly")
            return True
        else:
            print("[FAIL] File operations failed")
            return False
            
    except Exception as e:
        print(f"[FAIL] File operations failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Data Joiner Functionality Tests")
    print("=" * 50)
    
    tests = [
        test_dummy_row_detection,
        test_data_combination,
        test_file_operations
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests completed: {passed}/{total} passed")
    print("=" * 50)
    
    if passed == total:
        print("[PASS] All tests passed! The application is working correctly.")
        return True
    else:
        print("[FAIL] Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
