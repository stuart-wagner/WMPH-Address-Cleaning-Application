#!/usr/bin/env python3
"""
Test script to verify the GUI fix for the "truth value of an index is ambiguous" error
"""

import pandas as pd
import sys
import os

def test_combine_datasets_fix():
    """Test that combine_datasets works without the ambiguous index error"""
    print("Testing combine_datasets fix...")
    
    from data_joiner import DataJoinerApp
    app = DataJoinerApp()
    
    # Create test datasets with different data types that might cause issues
    dataset1 = pd.DataFrame({
        'ID': [1, 2, 3],
        'Address': ['123 Main St', '456 Oak Ave', '789 Pine St'],
        'Value': [10.5, 20.3, 30.1],
        'Category': ['A', 'B', 'C']
    })
    
    dataset2 = pd.DataFrame({
        'ID': [4, 5, 6],
        'Address': ['321 Elm St', '654 Maple Dr', '987 Cedar Ln'],
        'Value': [40.7, 50.9, 60.2],
        'Category': ['D', 'E', 'F']
    })
    
    # Set up the app with test data
    app.datasets = {'dataset1': dataset1, 'dataset2': dataset2}
    app.dataset_info = {
        'dataset1': {'time_period': 'Q1 2023', 'service': 'Service A'},
        'dataset2': {'time_period': 'Q2 2023', 'service': 'Service B'}
    }
    
    try:
        # This should not raise the "truth value of an index is ambiguous" error
        combined = app.combine_datasets()
        
        # Verify the result
        if combined is not None and len(combined) == 6:
            print("[PASS] combine_datasets works without ambiguous index error")
            print(f"Combined dataset has {len(combined)} rows and {len(combined.columns)} columns")
            print(f"Columns: {list(combined.columns)}")
            return True
        else:
            print("[FAIL] combine_datasets returned unexpected result")
            return False
            
    except Exception as e:
        if "truth value of an index is ambiguous" in str(e):
            print(f"[FAIL] Still getting ambiguous index error: {e}")
            return False
        else:
            print(f"[FAIL] Unexpected error: {e}")
            return False

def test_address_cleaning_fix():
    """Test that address cleaning works without pandas errors"""
    print("Testing address cleaning fix...")
    
    from data_joiner import DataJoinerApp
    app = DataJoinerApp()
    
    # Create test data with various data types
    test_addresses = pd.Series([
        '123 Main St Apt 4B',
        '456 Oak Ave Unit 12',
        '789 Pine St Suite 100',
        '321 Elm St #5',
        '654 Maple Dr Lot 3',
        '987 Cedar Ln PO Box 123',
        '258 Spruce Ave',
        None,  # Test None handling
        '',    # Test empty string
        '   ', # Test whitespace
        123,   # Test numeric
        ['123', 'Main St']  # Test list (edge case)
    ])
    
    try:
        # This should not raise pandas errors
        cleaned_address, apartment_indicator = app.clean_address_column(test_addresses)
        
        if len(cleaned_address) == len(test_addresses) and len(apartment_indicator) == len(test_addresses):
            print("[PASS] Address cleaning works without pandas errors")
            print(f"Processed {len(cleaned_address)} addresses")
            return True
        else:
            print("[FAIL] Address cleaning returned unexpected result")
            return False
            
    except Exception as e:
        if "truth value of an index is ambiguous" in str(e):
            print(f"[FAIL] Still getting ambiguous index error in address cleaning: {e}")
            return False
        else:
            print(f"[FAIL] Unexpected error in address cleaning: {e}")
            return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Data Joiner GUI Fix Tests")
    print("=" * 60)
    
    tests = [
        test_combine_datasets_fix,
        test_address_cleaning_fix
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"Tests completed: {passed}/{total} passed")
    print("=" * 60)
    
    if passed == total:
        print("[PASS] All GUI fix tests passed! The ambiguous index error is resolved.")
        return True
    else:
        print("[FAIL] Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


