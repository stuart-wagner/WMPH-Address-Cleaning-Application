#!/usr/bin/env python3
"""
Test script for the Data Joiner application
"""

import pandas as pd
import os
import tempfile

def create_test_data():
    """Create sample test datasets"""
    
    # Create test directory
    test_dir = "test_data"
    os.makedirs(test_dir, exist_ok=True)
    
    # Test Dataset 1 - Customer Support Q1 2023
    data1 = {
        'Customer_ID': [1, 2, 3, 4, 5],
        'Issue_Type': ['Login', 'Payment', 'Feature', 'Bug', 'Account'],
        'Resolution_Time': [15, 30, 45, 20, 60],
        'Satisfaction': [5, 4, 3, 5, 2]
    }
    df1 = pd.DataFrame(data1)
    
    # Add dummy rows at the beginning
    dummy_rows = pd.DataFrame({
        'Customer_ID': ['Customer Support Report', 'Q1 2023', ''],
        'Issue_Type': ['', '', ''],
        'Resolution_Time': ['', '', ''],
        'Satisfaction': ['', '', '']
    })
    
    df1_with_dummy = pd.concat([dummy_rows, df1], ignore_index=True)
    df1_with_dummy.to_excel(f"{test_dir}/customer_support_q1.xlsx", index=False)
    df1_with_dummy.to_csv(f"{test_dir}/customer_support_q1.csv", index=False)
    
    # Test Dataset 2 - Sales Q2 2023
    data2 = {
        'Client_ID': [101, 102, 103, 104, 105],
        'Product': ['Software A', 'Software B', 'Software A', 'Software C', 'Software B'],
        'Revenue': [5000, 7500, 3000, 12000, 6000],
        'Sales_Rep': ['John', 'Jane', 'Bob', 'Alice', 'John']
    }
    df2 = pd.DataFrame(data2)
    
    # Add dummy rows
    dummy_rows2 = pd.DataFrame({
        'Client_ID': ['Sales Report', 'Q2 2023', ''],
        'Product': ['', '', ''],
        'Revenue': ['', '', ''],
        'Sales_Rep': ['', '', '']
    })
    
    df2_with_dummy = pd.concat([dummy_rows2, df2], ignore_index=True)
    df2_with_dummy.to_excel(f"{test_dir}/sales_q2.xlsx", index=False)
    df2_with_dummy.to_csv(f"{test_dir}/sales_q2.csv", index=False)
    
    # Test Dataset 3 - Marketing Q3 2023
    data3 = {
        'Campaign_ID': [201, 202, 203, 204, 205],
        'Campaign_Name': ['Summer Sale', 'Back to School', 'Holiday Prep', 'New Year', 'Valentine'],
        'Cost': [1000, 1500, 2000, 1200, 800],
        'Conversions': [50, 75, 100, 60, 40]
    }
    df3 = pd.DataFrame(data3)
    
    # Add dummy rows
    dummy_rows3 = pd.DataFrame({
        'Campaign_ID': ['Marketing Report', 'Q3 2023', ''],
        'Campaign_Name': ['', '', ''],
        'Cost': ['', '', ''],
        'Conversions': ['', '', '']
    })
    
    df3_with_dummy = pd.concat([dummy_rows3, df3], ignore_index=True)
    df3_with_dummy.to_excel(f"{test_dir}/marketing_q3.xlsx", index=False)
    df3_with_dummy.to_csv(f"{test_dir}/marketing_q3.csv", index=False)
    
    print(f"Test data created in '{test_dir}' directory:")
    print("- customer_support_q1.xlsx/csv")
    print("- sales_q2.xlsx/csv") 
    print("- marketing_q3.xlsx/csv")
    print("\nYou can now test the Data Joiner application with these files!")

if __name__ == "__main__":
    create_test_data()

