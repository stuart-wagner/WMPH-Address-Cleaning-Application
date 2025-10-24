# WMCHD Client-Services Data Cleaner

A modern, user-friendly desktop application for cleaning, joining, and enriching datasets with a focus on advanced address processing.

## Features

- **Multi-File Loading**: Load and process multiple Excel (`.xlsx`, `.xls`) and CSV (`.csv`) files in one go.
- **Smart Data Ingestion**: Automatically detects and skips "dummy rows" (like report titles or empty headers) at the top of files.
- **Structured Metadata**: Assign standardized `Month`, `Year`, and `Service` metadata to each source file for better tracking and analysis.
- **Column Standardization**: A dedicated step to preview datasets and rename columns to ensure consistency before combining.
- **Advanced Address Cleaning**:
  - **Auto-Cleaning**: Automatically cleans addresses with high-confidence indicators (e.g., `APT`, `UNIT`, `SUITE`), removing unit information.
  - **Flag for Review**: Flags addresses with ambiguous patterns (e.g., `#`, `PO BOX`, number patterns) for manual user oversight, without altering them.
  - **Configurable Rules**: All cleaning and flagging rules are fully customizable through a user-friendly settings panel.
- **Data Summarization & Enrichment**: Load a secondary dataset, summarize it by a chosen column (e.g., to get counts), and then merge this aggregated data back into your main dataset.
- **Guided 8-Step Workflow**: An intuitive, tab-based interface that guides the user logically through the entire data processing pipeline.
- **Flexible Export**: Export the final, processed dataset to either Excel (`.xlsx`) or CSV (`.csv`).
- **Modern GUI**: A sleek and professional interface built with CustomTkinter.

## Installation

1. Install Python 3.7 or higher
2. Install required packages:
   ```bash
   pip install pandas customtkinter openpyxl
   ```

## Usage

Run the application from your terminal:
   ```bash
   python data_joiner.py
   ```
## The 9-Step Workflow

The application guides users through a comprehensive 9-step process:

1.  **Load Data**: Load one or more source datasets. For each file, assign `Month`, `Year`, and `Service` metadata.
2.  **Review & Rename**: Preview each dataset and rename columns as needed to ensure consistency across all files.
3.  **Join & Preview**: All loaded datasets are stacked (concatenated) into a single large table. The metadata from Step 1 is added as new columns.
4.  **Deduplicate by Date**: Group data by a selected column and keep only the most recent record based on `Year` and `Month`.
5.  **Address Cleaning**: Select the column containing address data. The application will:
    -   Create a `new_{address_column}` with cleaned addresses (removing high-confidence unit info).
    -   Create a `{address_column}_auto_cleaned` column indicating if a high-confidence cleaning was performed.
    -   Create a `{address_column}_may_have_word` column to flag rows with ambiguous patterns (e.g., `#`, `PO BOX`, number patterns) for manual review, without altering them.
    -   All cleaning and flagging rules are fully customizable through the `⚙️ Settings` panel.
6.  **Additional Dataset**: Load a second, separate dataset that you want to use for data enrichment.
7.  **Summarize Data**: Choose a column from the additional dataset and summarize it (e.g., to get counts of unique values).
8.  **Left Join**: Merge the main cleaned dataset (from Step 5) with the summarized dataset (from Step 7) using a left join.
9.  **Export**: Save the final, merged, and cleaned dataset to an Excel or CSV file.

## Requirements

- Python 3.7+
- pandas
- openpyxl
- customtkinter

## Troubleshooting

- **File Loading Issues**: Ensure files are not corrupted and have proper headers
- **Address Cleaning Not Working**: If addresses aren't being cleaned or flagged as expected, check the `⚙️ Settings` panel to ensure the keywords and patterns match your data. The cleaning rules are loaded from `settings.json`.
- **Join Errors**: Ensure the columns you select for joining in Step 8 have matching data types and formats.

## Support

This application is designed to be user-friendly for non-technical users. The interface provides clear instructions and helpful error messages.
For a more detailed user guide, refer to `UPDATED_WORKFLOW_GUIDE.md`.
