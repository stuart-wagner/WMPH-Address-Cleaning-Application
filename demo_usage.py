#!/usr/bin/env python3
"""
Demo script showing how to use the Data Joiner application programmatically
"""

import pandas as pd
import os

def create_demo_datasets():
    """Create demo datasets to test the application"""
    
    # Create demo directory
    demo_dir = "demo_data"
    os.makedirs(demo_dir, exist_ok=True)
    
    print("Creating demo datasets...")
    
    # Dataset 1: Customer Support Data
    support_data = {
        'Customer_ID': [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
        'Issue_Type': ['Login Problem', 'Payment Issue', 'Feature Request', 'Bug Report', 
                      'Account Access', 'Billing Question', 'Technical Support', 'Feature Request'],
        'Priority': ['High', 'Medium', 'Low', 'High', 'Medium', 'Low', 'High', 'Medium'],
        'Resolution_Time_Hours': [2, 4, 8, 1, 6, 3, 2, 5],
        'Satisfaction_Rating': [4, 3, 5, 2, 4, 5, 3, 4],
        'Agent_Name': ['Alice', 'Bob', 'Charlie', 'Alice', 'David', 'Eve', 'Bob', 'Charlie']
    }
    
    # Add dummy rows
    dummy_rows = pd.DataFrame({
        'Customer_ID': ['CUSTOMER SUPPORT REPORT', 'Q1 2023', 'Generated on: 2023-03-31', ''],
        'Issue_Type': ['', '', '', ''],
        'Priority': ['', '', '', ''],
        'Resolution_Time_Hours': ['', '', '', ''],
        'Satisfaction_Rating': ['', '', '', ''],
        'Agent_Name': ['', '', '', '']
    })
    
    support_df = pd.concat([dummy_rows, pd.DataFrame(support_data)], ignore_index=True)
    support_df.to_excel(f"{demo_dir}/customer_support_q1_2023.xlsx", index=False)
    support_df.to_csv(f"{demo_dir}/customer_support_q1_2023.csv", index=False)
    
    # Dataset 2: Sales Data
    sales_data = {
        'Client_ID': [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009],
        'Product_Name': ['Software A', 'Software B', 'Software A', 'Software C', 'Software B',
                        'Software A', 'Software C', 'Software B', 'Software A'],
        'Sale_Amount': [5000, 7500, 3000, 12000, 6000, 4500, 9000, 5500, 3500],
        'Sales_Rep': ['John', 'Jane', 'John', 'Bob', 'Jane', 'Alice', 'Bob', 'John', 'Alice'],
        'Region': ['North', 'South', 'East', 'West', 'North', 'South', 'East', 'West', 'North'],
        'Deal_Status': ['Closed', 'Closed', 'Closed', 'Closed', 'Closed', 'Closed', 'Closed', 'Closed', 'Closed']
    }
    
    # Add dummy rows
    dummy_rows2 = pd.DataFrame({
        'Client_ID': ['SALES REPORT', 'Q2 2023', 'Generated on: 2023-06-30', ''],
        'Product_Name': ['', '', '', ''],
        'Sale_Amount': ['', '', '', ''],
        'Sales_Rep': ['', '', '', ''],
        'Region': ['', '', '', ''],
        'Deal_Status': ['', '', '', '']
    })
    
    sales_df = pd.concat([dummy_rows2, pd.DataFrame(sales_data)], ignore_index=True)
    sales_df.to_excel(f"{demo_dir}/sales_q2_2023.xlsx", index=False)
    sales_df.to_csv(f"{demo_dir}/sales_q2_2023.csv", index=False)
    
    # Dataset 3: Marketing Data
    marketing_data = {
        'Campaign_ID': [3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008],
        'Campaign_Name': ['Summer Sale', 'Back to School', 'Holiday Prep', 'New Year Special',
                         'Valentine\'s Day', 'Spring Launch', 'Summer Campaign', 'Fall Promotion'],
        'Budget': [10000, 15000, 20000, 12000, 8000, 18000, 22000, 16000],
        'Impressions': [50000, 75000, 100000, 60000, 40000, 90000, 110000, 80000],
        'Clicks': [2500, 3750, 5000, 3000, 2000, 4500, 5500, 4000],
        'Conversions': [250, 375, 500, 300, 200, 450, 550, 400],
        'Channel': ['Email', 'Social Media', 'Google Ads', 'Email', 'Social Media', 
                   'Google Ads', 'Email', 'Social Media']
    }
    
    # Add dummy rows
    dummy_rows3 = pd.DataFrame({
        'Campaign_ID': ['MARKETING REPORT', 'Q3 2023', 'Generated on: 2023-09-30', ''],
        'Campaign_Name': ['', '', '', ''],
        'Budget': ['', '', '', ''],
        'Impressions': ['', '', '', ''],
        'Clicks': ['', '', '', ''],
        'Conversions': ['', '', '', ''],
        'Channel': ['', '', '', '']
    })
    
    marketing_df = pd.concat([dummy_rows3, pd.DataFrame(marketing_data)], ignore_index=True)
    marketing_df.to_excel(f"{demo_dir}/marketing_q3_2023.xlsx", index=False)
    marketing_df.to_csv(f"{demo_dir}/marketing_q3_2023.csv", index=False)
    
    print(f"Demo datasets created in '{demo_dir}' directory:")
    print("1. customer_support_q1_2023.xlsx/csv - Customer support data with dummy rows")
    print("2. sales_q2_2023.xlsx/csv - Sales data with dummy rows")
    print("3. marketing_q3_2023.xlsx/csv - Marketing data with dummy rows")
    print("\nThese files demonstrate:")
    print("- Multiple dummy rows at the beginning")
    print("- Different column structures")
    print("- Real-world data scenarios")
    print("\nYou can now test the Data Joiner application with these files!")

if __name__ == "__main__":
    create_demo_datasets()

