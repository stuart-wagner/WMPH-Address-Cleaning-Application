# Data Joiner - User Guide

## Overview
Data Joiner is a user-friendly desktop application that helps you combine multiple datasets from different time periods and services into one comprehensive dataset. The application automatically handles dummy rows and allows you to add metadata for each dataset.

## Getting Started

### Installation
1. Make sure you have Python 3.7 or higher installed
2. Install required packages by running:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
1. **Option 1**: Double-click `run_app.bat`
2. **Option 2**: Run from command line:
   ```bash
   python data_joiner.py
   ```

## Step-by-Step Usage

### Step 1: Load Your Datasets
1. Click the **"Load Dataset"** button
2. Select your Excel (.xlsx, .xls) or CSV files
3. If your Excel file has multiple sheets, choose the correct sheet
4. The application will automatically detect and skip dummy rows

### Step 2: Review and Rename Columns
1. Go to the **"Review & Rename"** tab
2. Select each dataset from the list
3. Preview the data structure
4. Use the column renaming tool:
   - Select columns that need standardization
   - Enter the desired column names
   - Click "Update" to apply changes
5. Ensure column names match across all datasets

### Step 3: Add Dataset Information
1. Select a dataset from the list
2. Enter the **Time Period** (e.g., "2023 Q1", "Jan-Mar 2023")
3. Enter the **Service** (e.g., "Customer Support", "Sales", "Marketing")
4. Click **"Add Info"**
5. Repeat for all datasets

### Step 3: Review and Edit Data
1. Go to the **"Review & Edit"** tab
2. Select a dataset to preview
3. If needed, rename columns for better joining:
   - Select a column from the dropdown
   - Enter the new name
   - Click **"Update"**

### Step 4: Join and Export
1. Go to the **"Join & Export"** tab
2. Choose your join method:
   - **Concatenate (Stack)**: Combines all rows from all datasets
   - **Inner Join**: Only rows that exist in all datasets
   - **Outer Join**: All rows from all datasets
3. Click **"Preview Combined Data"** to see the result
4. Export to Excel or CSV using the respective buttons

## Features Explained

### Automatic Dummy Row Detection
The application automatically detects and skips rows at the beginning of files that contain:
- Mostly empty values
- Non-numeric data in numeric columns
- Text that appears to be titles or descriptions

### Dataset Information Tracking
Each dataset gets three additional columns:
- **Time_Period**: The time period you specified
- **Service**: The service you specified
- **Dataset_Name**: The original filename

### Column Management
- Preview all columns before joining
- Rename columns to ensure proper alignment
- See data types and sample values

## Example Workflow

### Scenario: Combining Quarterly Reports
1. **Load Datasets**:
   - `customer_support_q1.xlsx`
   - `sales_q2.xlsx`
   - `marketing_q3.xlsx`

2. **Add Information**:
   - Customer Support: Time Period="Q1 2023", Service="Customer Support"
   - Sales: Time Period="Q2 2023", Service="Sales"
   - Marketing: Time Period="Q3 2023", Service="Marketing"

3. **Review Data**:
   - Check column names
   - Rename if needed (e.g., "Customer_ID" → "ID")

4. **Join and Export**:
   - Choose "Concatenate (Stack)"
   - Preview the combined data
   - Export to Excel

### Result
You'll get a single Excel file with all your data plus:
- Time period information for each row
- Service information for each row
- Original dataset name for each row

## Tips for Best Results

### File Preparation
- Ensure your data has clear column headers
- Place dummy rows (titles, descriptions) at the very beginning
- Use consistent data formats across files

### Column Naming
- Use descriptive column names
- Avoid special characters
- Consider renaming similar columns to match (e.g., "Customer_ID" and "Client_ID" → "ID")

### Data Quality
- Check for missing values
- Ensure consistent data types
- Remove any completely empty rows

## Troubleshooting

### Common Issues

**"Failed to load dataset"**
- Check if the file is corrupted
- Ensure the file is not password protected
- Try saving as a different format

**"No datasets loaded"**
- Make sure you've loaded at least one dataset
- Check that the file loaded successfully

**"Please add time period and service info"**
- Go back to the Load Data tab
- Select each dataset and add the required information

**"Column not found"**
- Check the column name spelling
- Make sure you've selected the correct dataset

### Performance Tips
- For very large datasets (>100,000 rows), consider splitting them first
- Close other applications to free up memory
- Use CSV format for faster loading

## File Formats Supported

### Input Formats
- **Excel**: .xlsx, .xls
- **CSV**: .csv (comma-separated)

### Output Formats
- **Excel**: .xlsx (recommended for complex data)
- **CSV**: .csv (good for simple data, smaller file size)

## Getting Help

If you encounter issues:
1. Check the error message carefully
2. Ensure all required information is provided
3. Try with smaller datasets first
4. Check the file format and structure

## Example Files

The application comes with sample data in the `demo_data` folder:
- `customer_support_q1_2023.xlsx/csv`
- `sales_q2_2023.xlsx/csv`
- `marketing_q3_2023.xlsx/csv`

These files demonstrate:
- Multiple dummy rows at the beginning
- Different column structures
- Real-world data scenarios

Use these files to practice and understand the application before working with your own data.

