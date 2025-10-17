#!/usr/bin/env python3
"""
Test script for the new Data Joiner workflow
"""

import pandas as pd
import os
import sys

def test_address_cleaning():
    """Test the address cleaning functionality"""
    print("Testing address cleaning functionality...")
    
    # Create test data with addresses
    test_data = {
        'ID': [1, 2, 3, 4, 5, 6, 7, 8],
        'Address': [
            '123 Main St Apt 4B',
            '456 Oak Ave Unit 12',
            '789 Pine St Suite 100',
            '321 Elm St #5',
            '654 Maple Dr Lot 3',
            '987 Cedar Ln PO Box 123',
            '147 Birch St 2A',
            '258 Spruce Ave'
        ],
        'Time_Period': ['Q1 2023'] * 8,
        'Service': ['Test Service'] * 8
    }
    
    df = pd.DataFrame(test_data)
    
    # Test the cleaning functions
    from data_joiner import DataJoinerApp
    app = DataJoinerApp()
    
    # Test apartment detection
    test_addresses = [
        '123 Main St Apt 4B',
        '456 Oak Ave Unit 12', 
        '789 Pine St Suite 100',
        '321 Elm St #5',
        '654 Maple Dr Lot 3',
        '987 Cedar Ln PO Box 123',
        '258 Spruce Ave'
    ]
    
    expected_results = [True, True, True, True, True, True, False]
    
    for i, address in enumerate(test_addresses):
        result = app.check_apartment_indicator(address)
        if result == expected_results[i]:
            print(f"[PASS] Apartment detection for '{address}': {result}")
        else:
            print(f"[FAIL] Apartment detection for '{address}': expected {expected_results[i]}, got {result}")
            return False
    
    # Test address cleaning
    cleaned_addresses = []
    for address in test_addresses:
        cleaned = app.remove_apartment_info(address)
        cleaned_addresses.append(cleaned)
    
    expected_cleaned = [
        '123 Main St',
        '456 Oak Ave',
        '789 Pine St',
        '321 Elm St',
        '654 Maple Dr',
        '987 Cedar Ln',
        '258 Spruce Ave'
    ]
    
    for i, (original, cleaned, expected) in enumerate(zip(test_addresses, cleaned_addresses, expected_cleaned)):
        if cleaned == expected:
            print(f"[PASS] Address cleaning for '{original}': '{cleaned}'")
        else:
            print(f"[FAIL] Address cleaning for '{original}': expected '{expected}', got '{cleaned}'")
            return False
    
    print("[PASS] Address cleaning functionality works correctly")
    return True

def test_settings():
    """Test settings functionality"""
    print("Testing settings functionality...")
    
    from data_joiner import DataJoinerApp
    app = DataJoinerApp()
    
    # Test default settings
    if 'apartment_words' in app.settings and 'po_box_words' in app.settings:
        print("[PASS] Default settings loaded correctly")
    else:
        print("[FAIL] Default settings not loaded correctly")
        return False
    
    # Test settings save/load
    original_apt_words = app.settings['apartment_words'].copy()
    app.settings['apartment_words'].append('TEST_WORD')
    app.save_settings()
    
    # Create new app instance to test loading
    app2 = DataJoinerApp()
    if 'TEST_WORD' in app2.settings['apartment_words']:
        print("[PASS] Settings save/load works correctly")
    else:
        print("[FAIL] Settings save/load failed")
        return False
    
    # Restore original settings
    app.settings['apartment_words'] = original_apt_words
    app.save_settings()
    
    return True

def test_workflow_integration():
    """Test the complete workflow integration"""
    print("Testing workflow integration...")
    
    from data_joiner import DataJoinerApp
    app = DataJoinerApp()
    
    # Create test datasets
    dataset1 = pd.DataFrame({
        'ID': [1, 2, 3],
        'Address': ['123 Main St Apt 4B', '456 Oak Ave', '789 Pine St Unit 12'],
        'Value': [10, 20, 30]
    })
    
    dataset2 = pd.DataFrame({
        'ID': [4, 5, 6],
        'Address': ['321 Elm St #5', '654 Maple Dr', '987 Cedar Ln PO Box 123'],
        'Value': [40, 50, 60]
    })
    
    # Simulate the workflow
    app.datasets = {'dataset1': dataset1, 'dataset2': dataset2}
    app.dataset_info = {
        'dataset1': {'time_period': 'Q1 2023', 'service': 'Service A'},
        'dataset2': {'time_period': 'Q2 2023', 'service': 'Service B'}
    }
    
    # Step 1: Join datasets
    app.combined_data = app.combine_datasets()
    if app.combined_data is not None and len(app.combined_data) == 6:
        print("[PASS] Dataset joining works correctly")
    else:
        print("[FAIL] Dataset joining failed")
        return False
    
    # Step 2: Clean address data
    cleaned_address, apartment_indicator = app.clean_address_column(app.combined_data['Address'])
    app.cleaned_data = app.combined_data.copy()
    app.cleaned_data['new_Address'] = cleaned_address
    app.cleaned_data['Address_apartment_indicator'] = apartment_indicator
    
    if 'new_Address' in app.cleaned_data.columns and 'Address_apartment_indicator' in app.cleaned_data.columns:
        print("[PASS] Address cleaning integration works correctly")
    else:
        print("[FAIL] Address cleaning integration failed")
        return False
    
    # Step 3: Test additional dataset join
    additional_data = pd.DataFrame({
        'Address': ['123 Main St', '456 Oak Ave', '789 Pine St', '321 Elm St', '654 Maple Dr', '987 Cedar Ln'],
        'Additional_Info': ['Info1', 'Info2', 'Info3', 'Info4', 'Info5', 'Info6']
    })
    
    app.additional_dataset = additional_data
    app.final_data = app.cleaned_data.merge(
        app.additional_dataset,
        left_on='new_Address',
        right_on='Address',
        how='left',
        suffixes=('', '_additional')
    )
    
    if app.final_data is not None and 'Additional_Info' in app.final_data.columns:
        print("[PASS] Additional dataset joining works correctly")
    else:
        print("[FAIL] Additional dataset joining failed")
        return False
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("Data Joiner New Workflow Tests")
    print("=" * 60)
    
    tests = [
        test_address_cleaning,
        test_settings,
        test_workflow_integration
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
        print("[PASS] All tests passed! The new workflow is working correctly.")
        return True
    else:
        print("[FAIL] Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


