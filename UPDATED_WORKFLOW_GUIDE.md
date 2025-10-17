# Data Joiner - Updated Workflow Guide

## 🎯 New 7-Step Workflow

The Data Joiner application has been completely updated to follow a specific 7-step workflow for advanced dataset processing with address cleaning capabilities.

## 📋 Step-by-Step Process

### Step 1: Load Data
- **Purpose**: Load multiple datasets and assign time period/service information
- **Features**:
  - Load Excel (.xlsx, .xls) or CSV files
  - Add time period and service information for each dataset
  - Review and adjust column names if needed
  - Remove datasets if necessary

### Step 2: Join & Preview
- **Purpose**: Join all datasets and preview the combined result
- **Features**:
  - All datasets are stacked together (concatenated)
  - Time period and service information is added to each row
  - Preview the combined dataset before proceeding
  - Verify data structure and completeness

### Step 3: Address Cleaning
- **Purpose**: Clean address data and create apartment indicators
- **Features**:
  - Select the address column to clean
  - Automatically detect apartment/unit information
  - Remove apartment information from addresses
  - Create indicator variable for potential apartment entries
  - Configurable apartment detection rules

### Step 4: Review Cleaned Data
- **Purpose**: Review the results of address cleaning
- **Features**:
  - Check the cleaned address column
  - Verify the apartment indicator column
  - Ensure cleaning was performed correctly
  - Make adjustments if needed

### Step 5: Additional Dataset
- **Purpose**: Load and join an additional dataset
- **Features**:
  - Load a new dataset to join with cleaned data
  - Select join variables from both datasets
  - Perform left join (keeps all cleaned data, adds matching additional data)
  - Preview the merged result

### Step 6: Final Review
- **Purpose**: Review the complete merged dataset
- **Features**:
  - Check the final dataset with all joins
  - Verify data quality and completeness
  - Ensure all processing steps were successful
  - Prepare for export

### Step 7: Export
- **Purpose**: Export the final processed dataset
- **Features**:
  - Export to Excel (.xlsx) format
  - Export to CSV format
  - Save the complete processed data
  - Maintain all original and processed columns

## 🔧 Advanced Address Cleaning Features

### Apartment Detection
The application automatically detects apartment-like information in addresses:

**Apartment Words** (configurable):
- APT, APARTMENT, UNIT, U, LOT, SUITE, STE
- BLDG, BUILDING, FLOOR, FL, ROOM, RM

**PO Box Detection**:
- PO BOX, P.O. BOX, POBOX, P.O.BOX

**Number Pattern Detection**:
- Addresses ending with numbers (when preceded by apartment words)
- Addresses with # symbols
- Complex number patterns

### Address Cleaning Process
1. **Detection**: Identifies apartment indicators in addresses
2. **Cleaning**: Removes apartment information from addresses
3. **New Column**: Creates `new_[original_column_name]` with cleaned addresses
4. **Indicator**: Creates `[original_column_name]_apartment_indicator` (Yes/No)

### Example Address Cleaning
```
Original: "123 Main St Apt 4B"
Cleaned:  "123 Main St"
Indicator: "Yes"

Original: "456 Oak Ave Unit 12"
Cleaned:  "456 Oak Ave"
Indicator: "Yes"

Original: "789 Pine St Suite 100"
Cleaned:  "789 Pine St"
Indicator: "Yes"

Original: "321 Elm St #5"
Cleaned:  "321 Elm St"
Indicator: "Yes"

Original: "258 Spruce Ave"
Cleaned:  "258 Spruce Ave"
Indicator: "No"
```

## ⚙️ Settings Configuration

### Hidden Settings Window
Access the settings window by clicking the "⚙️ Settings" button in the main interface.

### Configurable Options
1. **Apartment Words**: Customize which words indicate apartment information
2. **PO Box Words**: Customize PO Box detection patterns
3. **Number Patterns**: Customize regex patterns for number detection
4. **Case Sensitivity**: Control case sensitivity (currently disabled)

### Settings Persistence
- Settings are automatically saved to `settings.json`
- Settings persist between application sessions
- Default settings can be restored at any time

## 🚀 Getting Started

### Quick Start
1. **Run Application**: `python data_joiner.py` or double-click `run_app.bat`
2. **Load Datasets**: Use Step 1 to load your data files
3. **Join Data**: Use Step 2 to combine all datasets
4. **Clean Addresses**: Use Step 3 to clean address data
5. **Review Results**: Use Step 4 to check cleaning results
6. **Add More Data**: Use Step 5 to join additional datasets
7. **Final Review**: Use Step 6 to review complete dataset
8. **Export**: Use Step 7 to save your processed data

### Sample Data
The application includes sample data in the `demo_data/` folder:
- `customer_support_q1_2023.xlsx/csv`
- `sales_q2_2023.xlsx/csv`
- `marketing_q3_2023.xlsx/csv`

## 🧪 Testing

### Automated Tests
Run `python test_new_workflow.py` to test all functionality:
- Address cleaning accuracy
- Settings management
- Complete workflow integration
- Data joining and merging

### Manual Testing
1. Use the sample data files
2. Follow the 7-step workflow
3. Test different address formats
4. Verify export functionality

## 📊 Data Flow

```
Original Datasets
       ↓
   [Step 1] Load & Assign Info
       ↓
   [Step 2] Join & Preview
       ↓
   [Step 3] Address Cleaning
       ↓
   [Step 4] Review Cleaned Data
       ↓
   [Step 5] Additional Dataset Join
       ↓
   [Step 6] Final Review
       ↓
   [Step 7] Export
```

## 🎨 User Interface

### Modern Design
- Clean, professional interface
- Intuitive tabbed workflow
- Clear step-by-step instructions
- Helpful error messages and feedback

### Key Features
- **Tabbed Interface**: Easy navigation between steps
- **Data Previews**: Interactive tables for data review
- **Settings Panel**: Hidden but accessible configuration
- **Progress Tracking**: Clear indication of current step
- **Error Handling**: Comprehensive error messages

## 🔍 Troubleshooting

### Common Issues
1. **"No datasets loaded"**: Complete Step 1 first
2. **"Please join datasets first"**: Complete Step 2 before Step 3
3. **"Please clean address data first"**: Complete Step 3 before Step 5
4. **"Please complete the data processing workflow first"**: Complete all steps before Step 7

### Address Cleaning Issues
- Check settings if apartment detection is not working correctly
- Verify address column selection
- Review apartment indicator results
- Adjust settings if needed

### Performance Tips
- Use CSV format for faster loading
- Limit preview to first 100 rows for large datasets
- Close other applications for better performance

## 📈 Use Cases

### Primary Use Cases
1. **Customer Data Processing**: Clean customer addresses for analysis
2. **Property Management**: Process property addresses and units
3. **Marketing Campaigns**: Clean mailing addresses for campaigns
4. **Data Integration**: Combine multiple datasets with address cleaning

### Business Scenarios
- **Real Estate**: Clean property addresses and unit information
- **E-commerce**: Process customer shipping addresses
- **Healthcare**: Clean patient addresses for analysis
- **Government**: Process citizen address data

## 🎯 Success Metrics

### Functionality
- ✅ All 7 workflow steps implemented
- ✅ Advanced address cleaning with apartment detection
- ✅ Configurable settings with persistence
- ✅ Left join functionality for additional datasets
- ✅ Complete data preview and export capabilities

### User Experience
- ✅ Intuitive step-by-step workflow
- ✅ Clear instructions and feedback
- ✅ Modern, professional interface
- ✅ Comprehensive error handling

### Technical Quality
- ✅ Robust address cleaning algorithms
- ✅ Configurable and extensible settings
- ✅ Memory-efficient data processing
- ✅ Comprehensive testing and validation

## 🔮 Future Enhancements

### Potential Improvements
- **Advanced Address Parsing**: More sophisticated address components
- **Geocoding Integration**: Add latitude/longitude coordinates
- **Data Validation**: Enhanced data quality checks
- **Batch Processing**: Process multiple files simultaneously
- **Cloud Integration**: Support for cloud storage services

### Technical Upgrades
- **Performance Optimization**: Handle larger datasets
- **Memory Management**: Better memory usage for large files
- **UI Improvements**: More advanced data visualization
- **Plugin System**: Extensible architecture for custom features

## 📝 Conclusion

The updated Data Joiner application provides a comprehensive solution for advanced dataset processing with specialized address cleaning capabilities. The 7-step workflow ensures a systematic approach to data processing, while the configurable settings allow for customization to specific needs.

The application is production-ready and provides a solid foundation for future enhancements while meeting all current requirements for data joining, address cleaning, and dataset merging.


