# Data Joiner Application

A modern, user-friendly desktop application for combining multiple datasets with time period and service information.

## Features

- **Load Multiple Datasets**: Support for Excel (.xlsx, .xls) and CSV files
- **Smart Data Detection**: Automatically detects and skips dummy rows (titles, descriptions)
- **Time & Service Tracking**: Add time period and service information for each dataset
- **Data Preview**: Review and edit column names before joining
- **Flexible Joining**: Multiple join methods (Concatenate, Inner Join, Outer Join)
- **Export Options**: Export combined data to Excel or CSV
- **Modern GUI**: Sleek, intuitive interface built with CustomTkinter

## Installation

1. Install Python 3.7 or higher
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python data_joiner.py
   ```

2. **Load Data Tab**:
   - Click "Load Dataset" to import your files
   - Add time period and service information for each dataset
   - Remove datasets if needed

3. **Review & Edit Tab**:
   - Select a dataset to preview
   - Edit column names for proper joining
   - Review data structure

4. **Join & Export Tab**:
   - Choose join method
   - Preview combined data
   - Export to Excel or CSV

## How It Works

1. **Data Loading**: The app automatically detects and skips dummy rows at the beginning of files
2. **Data Tracking**: Each dataset gets unique time period and service identifiers
3. **Data Joining**: Datasets are combined with additional metadata columns
4. **Export**: Clean, combined data ready for analysis

## Requirements

- Python 3.7+
- pandas
- openpyxl
- customtkinter
- Pillow

## Troubleshooting

- **File Loading Issues**: Ensure files are not corrupted and have proper headers
- **Memory Issues**: For very large datasets, consider splitting them first
- **Column Name Conflicts**: Use the Review & Edit tab to rename columns before joining

## Support

This application is designed to be user-friendly for non-technical users. The interface provides clear instructions and helpful error messages.

