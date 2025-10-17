import customtkinter as ctk
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from datetime import datetime
import json
import re

class DataJoinerApp:
    def __init__(self):
        # Set appearance mode and color theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("WMCHD Client-Services Data Cleaner - Joining and Address Cleaning")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Initialize review tab variables
        self.current_preview_dataset = None
        self.column_rename_history = {}
        
        # Initialize data storage
        self.datasets = {}  # Store loaded datasets
        self.dataset_info = {}  # Store time period and service info for each dataset
        self.combined_data = None
        self.cleaned_data = None
        self.final_data = None
        self.additional_dataset = None
        
        # Status tracking
        self.datasets_joined = False
        self.address_cleaning_done = False
        self.additional_join_done = False
        
        # Backup storage for reverting changes
        self.pre_cleaned_data = None
        self.pre_additional_join_data = None
        
        # Settings for address cleaning
        self.settings_file = "settings.json"
        self.load_settings()
        
        # Create the GUI
        self.create_widgets()
    
    def load_settings(self):
        """Load settings from file or create default settings"""
        default_settings = {
            "apartment_words": ["APT", "APARTMENT", "UNIT", "U", "LOT", "SUITE", "STE", "BLDG", "BUILDING", "FLOOR", "FL", "ROOM", "RM"],
            "po_box_words": ["PO BOX", "P.O. BOX", "POBOX", "P.O.BOX"],
            "number_patterns": [r'\d+$', r'#\d+', r'\d+[A-Z]?$'],
            "case_sensitive": False
        }
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    self.settings = json.load(f)
            else:
                self.settings = default_settings
                self.save_settings()
        except Exception as e:
            print(f"Error loading settings: {e}")
            self.settings = default_settings
    
    def save_settings(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
        
    def create_widgets(self):
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="WMCHD Client-Services Data Cleaner", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        subtitle_label = ctk.CTkLabel(
            main_frame, 
            text="Load, clean, and merge datasets with advanced address processing", 
            font=ctk.CTkFont(size=14)
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Create notebook for tabs
        self.notebook = ctk.CTkTabview(main_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Step 1: Load Data Tab
        self.load_tab = self.notebook.add("1. Load Data")
        self.create_load_tab()
        
        # Step 2: Review & Rename Tab
        self.review_tab = self.notebook.add("2. Review & Rename")
        self.create_review_tab()
        
        # Step 3: Join & Preview Tab
        self.join_tab = self.notebook.add("3. Join & Preview")
        self.create_join_tab()
        
        # Step 4: Address Cleaning Tab
        self.clean_tab = self.notebook.add("4. Address Cleaning")
        self.create_clean_tab()
        
        
        # Step 5: Additional Dataset Tab
        self.additional_tab = self.notebook.add("5. Additional Dataset")
        self.create_additional_tab()
        
        # Step 6: Final Review Tab
        self.final_tab = self.notebook.add("6. Final Review")
        self.create_final_tab()
        
        # Step 7: Export Tab
        self.export_tab = self.notebook.add("7. Export")
        self.create_export_tab()
        
        # Settings button
        settings_btn = ctk.CTkButton(
            main_frame,
            text="⚙️ Settings",
            command=self.open_settings,
            width=100,
            height=30
        )
        settings_btn.pack(side="right", padx=10, pady=10)
        
    def create_load_tab(self):
        # Load datasets section
        load_frame = ctk.CTkFrame(self.load_tab)
        load_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Instructions
        instructions = ctk.CTkLabel(
            load_frame,
            text="Step 1: Load your datasets and assign time period/service information\n• Load Excel or CSV files\n• Add time period and service for each dataset\n• Review and adjust column names if needed",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        instructions.pack(pady=(20, 30))
        
        # Load button
        load_btn = ctk.CTkButton(
            load_frame,
            text="Load Dataset",
            command=self.load_dataset,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        load_btn.pack(pady=10)
        
        # Dataset list
        self.dataset_list_frame = ctk.CTkFrame(load_frame)
        self.dataset_list_frame.pack(fill="both", expand=True, pady=20)
        
        self.dataset_list_label = ctk.CTkLabel(
            self.dataset_list_frame,
            text="Loaded Datasets:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.dataset_list_label.pack(pady=(20, 10))
        
        self.dataset_listbox = tk.Listbox(
            self.dataset_list_frame,
            height=15,
            font=("Arial", 11),
            selectmode=tk.SINGLE
        )
        self.dataset_listbox.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Dataset info frame
        self.info_frame = ctk.CTkFrame(load_frame)
        self.info_frame.pack(fill="x", pady=10)
        
        # Time period input
        time_label = ctk.CTkLabel(self.info_frame, text="Time Period:", font=ctk.CTkFont(size=12, weight="bold"))
        time_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.time_entry = ctk.CTkEntry(self.info_frame, placeholder_text="e.g., 2023 Q1, Jan-Mar 2023", width=200)
        self.time_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Service input
        service_label = ctk.CTkLabel(self.info_frame, text="Service:", font=ctk.CTkFont(size=12, weight="bold"))
        service_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        
        self.service_entry = ctk.CTkEntry(self.info_frame, placeholder_text="e.g., Customer Support, Sales", width=200)
        self.service_entry.grid(row=0, column=3, padx=10, pady=10)
        
        # Add info button
        add_info_btn = ctk.CTkButton(
            self.info_frame,
            text="Add Info",
            command=self.add_dataset_info,
            width=100
        )
        add_info_btn.grid(row=0, column=4, padx=10, pady=10)
        
        # Remove dataset button
        remove_btn = ctk.CTkButton(
            load_frame,
            text="Remove Selected Dataset",
            command=self.remove_dataset,
            fg_color="red",
            hover_color="darkred"
        )
        remove_btn.pack(pady=10)
    
    def create_join_tab(self):
        """Create the join and preview tab"""
        join_frame = ctk.CTkFrame(self.join_tab)
        join_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Instructions
        instructions = ctk.CTkLabel(
            join_frame,
            text="Step 2: Join datasets and preview the combined result\n• All datasets will be stacked together\n• Time period and service information will be added\n• Review the combined dataset before proceeding",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        instructions.pack(pady=(20, 10))
        
        # Join button
        join_btn = ctk.CTkButton(
            join_frame,
            text="Join Datasets",
            command=self.join_datasets,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        join_btn.pack(pady=10)
        
        # Debug / summary label to show per-dataset counts and combined shape
        self.join_summary_label = ctk.CTkLabel(join_frame, text="", font=ctk.CTkFont(size=12), justify="left")
        self.join_summary_label.pack(fill="x", padx=10, pady=(0,10))

        # Save Combined CSV button
        self.save_csv_btn = ctk.CTkButton(join_frame, text="Save Combined CSV", command=self.save_combined_debug)
        self.save_csv_btn.pack(pady=(0,5))

        # Save Combined XLSX button
        self.save_xlsx_btn = ctk.CTkButton(join_frame, text="Save Combined XLSX", command=self.save_combined_xlsx)
        self.save_xlsx_btn.pack(pady=(0,10))

        # Data preview
        self.join_preview_frame = ctk.CTkFrame(join_frame)
        self.join_preview_frame.pack(fill="both", expand=True, pady=10)
        
        # Create treeview for data preview
        self.join_tree_frame = ctk.CTkFrame(self.join_preview_frame)
        self.join_tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbars
        self.join_tree_scroll_y = tk.Scrollbar(self.join_tree_frame)
        self.join_tree_scroll_y.pack(side="right", fill="y")
        
        self.join_tree_scroll_x = tk.Scrollbar(self.join_tree_frame, orient="horizontal")
        self.join_tree_scroll_x.pack(side="bottom", fill="x")
        
        # Treeview
        self.join_tree = ttk.Treeview(self.join_tree_frame, yscrollcommand=self.join_tree_scroll_y.set, xscrollcommand=self.join_tree_scroll_x.set)
        self.join_tree.pack(side="left", fill="both", expand=True)
        
        self.join_tree_scroll_y.config(command=self.join_tree.yview)
        self.join_tree_scroll_x.config(command=self.join_tree.xview)
    
    def create_clean_tab(self):
        """Create the address cleaning tab"""
        clean_frame = ctk.CTkFrame(self.clean_tab)
        clean_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Instructions
        instructions = ctk.CTkLabel(
            clean_frame,
            text="Step 3: Clean address data\n• Select the address column to clean\n• Remove apartment/unit information\n• Create indicator for potential apartment entries",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        instructions.pack(pady=(20, 10))
        
        # Address column selection
        column_frame = ctk.CTkFrame(clean_frame)
        column_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(column_frame, text="Select Address Column:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=10, pady=10)
        
        self.address_column_selector = ctk.CTkComboBox(column_frame, values=[], command=self.on_address_column_select)
        self.address_column_selector.pack(side="left", padx=10, pady=10)
        
        # Clean button
        clean_btn = ctk.CTkButton(
            clean_frame,
            text="Clean Address Data",
            command=self.clean_address_data,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        clean_btn.pack(pady=10)
        
        # Results preview
        self.clean_preview_frame = ctk.CTkFrame(clean_frame)
        self.clean_preview_frame.pack(fill="both", expand=True, pady=10)
        
        # Create treeview for cleaned data preview
        self.clean_tree_frame = ctk.CTkFrame(self.clean_preview_frame)
        self.clean_tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbars
        self.clean_tree_scroll_y = tk.Scrollbar(self.clean_tree_frame)
        self.clean_tree_scroll_y.pack(side="right", fill="y")
        
        self.clean_tree_scroll_x = tk.Scrollbar(self.clean_tree_frame, orient="horizontal")
        self.clean_tree_scroll_x.pack(side="bottom", fill="x")
        
        # Treeview
        self.clean_tree = ttk.Treeview(self.clean_tree_frame, yscrollcommand=self.clean_tree_scroll_y.set, xscrollcommand=self.clean_tree_scroll_x.set)
        self.clean_tree.pack(side="left", fill="both", expand=True)
        
        self.clean_tree_scroll_y.config(command=self.clean_tree.yview)
        self.clean_tree_scroll_x.config(command=self.clean_tree.xview)
    
    def create_additional_tab(self):
        """Create the additional dataset tab"""
        additional_frame = ctk.CTkFrame(self.additional_tab)
        additional_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Instructions
        instructions = ctk.CTkLabel(
            additional_frame,
            text="Step 5: Load additional dataset for left join\n• Load a new dataset to join with cleaned data\n• Select join variables\n• Preview the merged result",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        instructions.pack(pady=(20, 10))
        
        # Load additional dataset
        load_additional_btn = ctk.CTkButton(
            additional_frame,
            text="Load Additional Dataset",
            command=self.load_additional_dataset,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        load_additional_btn.pack(pady=10)
        
        # Join variables selection
        join_vars_frame = ctk.CTkFrame(additional_frame)
        join_vars_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(join_vars_frame, text="Cleaned Data Column:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=10, pady=10)
        self.cleaned_join_column = ctk.CTkComboBox(join_vars_frame, values=[])
        self.cleaned_join_column.pack(side="left", padx=10, pady=10)
        
        ctk.CTkLabel(join_vars_frame, text="Additional Data Column:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=10, pady=10)
        self.additional_join_column = ctk.CTkComboBox(join_vars_frame, values=[])
        self.additional_join_column.pack(side="left", padx=10, pady=10)
        
        # Join button
        join_additional_btn = ctk.CTkButton(
            additional_frame,
            text="Join Datasets",
            command=self.join_additional_dataset,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        join_additional_btn.pack(pady=10)
        
        # Results preview
        self.additional_preview_frame = ctk.CTkFrame(additional_frame)
        self.additional_preview_frame.pack(fill="both", expand=True, pady=10)
        
        # Create treeview for merged data preview
        self.additional_tree_frame = ctk.CTkFrame(self.additional_preview_frame)
        self.additional_tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbars
        self.additional_tree_scroll_y = tk.Scrollbar(self.additional_tree_frame)
        self.additional_tree_scroll_y.pack(side="right", fill="y")
        
        self.additional_tree_scroll_x = tk.Scrollbar(self.additional_tree_frame, orient="horizontal")
        self.additional_tree_scroll_x.pack(side="bottom", fill="x")
        
        # Treeview
        self.additional_tree = ttk.Treeview(self.additional_tree_frame, yscrollcommand=self.additional_tree_scroll_y.set, xscrollcommand=self.additional_tree_scroll_x.set)
        self.additional_tree.pack(side="left", fill="both", expand=True)
        
        self.additional_tree_scroll_y.config(command=self.additional_tree.yview)
        self.additional_tree_scroll_x.config(command=self.additional_tree.xview)
    
    def create_final_tab(self):
        """Create the final review tab"""
        final_frame = ctk.CTkFrame(self.final_tab)
        final_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Instructions
        instructions = ctk.CTkLabel(
            final_frame,
            text="Step 6: Review final merged dataset\n• Check the complete dataset with all joins\n• Verify data quality and completeness\n• Proceed to export when ready",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        instructions.pack(pady=(20, 10))
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            final_frame,
            text="Refresh Preview",
            command=self.refresh_final_preview,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        refresh_btn.pack(pady=10)
        
        # Final data preview
        self.final_preview_frame = ctk.CTkFrame(final_frame)
        self.final_preview_frame.pack(fill="both", expand=True, pady=10)
        
        # Create treeview for final data preview
        self.final_tree_frame = ctk.CTkFrame(self.final_preview_frame)
        self.final_tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbars
        self.final_tree_scroll_y = tk.Scrollbar(self.final_tree_frame)
        self.final_tree_scroll_y.pack(side="right", fill="y")
        
        self.final_tree_scroll_x = tk.Scrollbar(self.final_tree_frame, orient="horizontal")
        self.final_tree_scroll_x.pack(side="bottom", fill="x")
        
        # Treeview
        self.final_tree = ttk.Treeview(self.final_tree_frame, yscrollcommand=self.final_tree_scroll_y.set, xscrollcommand=self.final_tree_scroll_x.set)
        self.final_tree.pack(side="left", fill="both", expand=True)
        
        self.final_tree_scroll_y.config(command=self.final_tree.yview)
        self.final_tree_scroll_x.config(command=self.final_tree.xview)
        
    def create_review_tab(self):
        """Create the review and rename columns tab"""
        review_frame = ctk.CTkFrame(self.review_tab)
        review_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Instructions
        instructions = ctk.CTkLabel(
            review_frame,
            text="Step 2: Review and Rename Columns\n• Select datasets to preview\n• Review column names and data\n• Standardize column names across datasets\n• Ensure consistency before joining",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        instructions.pack(pady=(20, 10))
        
        # Dataset selector
        selector_frame = ctk.CTkFrame(review_frame)
        selector_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(selector_frame, text="Select Dataset:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=10, pady=10)
        
        self.dataset_selector = ctk.CTkComboBox(selector_frame, values=[], command=self.on_dataset_select)
        self.dataset_selector.pack(side="left", padx=10, pady=10)
        
        # Data preview
        self.preview_frame = ctk.CTkFrame(review_frame)
        self.preview_frame.pack(fill="both", expand=True, pady=10)
        
        # Create treeview for data preview
        self.tree_frame = ctk.CTkFrame(self.preview_frame)
        self.tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbars
        self.tree_scroll_y = tk.Scrollbar(self.tree_frame)
        self.tree_scroll_y.pack(side="right", fill="y")
        
        self.tree_scroll_x = tk.Scrollbar(self.tree_frame, orient="horizontal")
        self.tree_scroll_x.pack(side="bottom", fill="x")
        
        # Treeview
        self.tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll_y.set, xscrollcommand=self.tree_scroll_x.set)
        self.tree.pack(side="left", fill="both", expand=True)
        
        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)
        
        # Column editing frame
        self.column_edit_frame = ctk.CTkFrame(review_frame)
        self.column_edit_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(self.column_edit_frame, text="Edit Column Names:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=10, pady=10)
        
        # Column selector
        self.column_selector = ctk.CTkComboBox(self.column_edit_frame, values=[], command=self.on_column_select)
        self.column_selector.pack(side="left", padx=10, pady=10)

        # New name entry
        self.new_name_entry = ctk.CTkEntry(self.column_edit_frame, placeholder_text="New column name")
        self.new_name_entry.pack(side="left", padx=10, pady=10)

        # Update button
        self.update_column_btn = ctk.CTkButton(self.column_edit_frame, text="Update Column Name", command=self.update_column_name)
        self.update_column_btn.pack(side="left", padx=10, pady=10)

        # Add button to update dataset selector
        self.refresh_btn = ctk.CTkButton(selector_frame, text="Refresh Dataset List", command=self.update_dataset_selector)
        self.refresh_btn.pack(side="left", padx=10, pady=10)
        
    def create_export_tab(self):
        """Create the export tab"""
        export_frame = ctk.CTkFrame(self.export_tab)
        export_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Instructions
        instructions = ctk.CTkLabel(
            export_frame,
            text="Step 7: Export final dataset\n• Export the complete merged dataset\n• Choose between Excel or CSV format\n• Save your processed data",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        instructions.pack(pady=(20, 10))
        
        # Export settings
        settings_frame = ctk.CTkFrame(export_frame)
        settings_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(settings_frame, text="Export Settings:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        # Note about data processing
        note_label = ctk.CTkLabel(
            settings_frame,
            text="Note: Make sure you have completed all previous steps (1-6) before exporting.",
            font=ctk.CTkFont(size=12),
            text_color="orange"
        )
        note_label.pack(pady=10)
        
        # Combined data preview
        self.combined_preview_frame = ctk.CTkFrame(export_frame)
        self.combined_preview_frame.pack(fill="both", expand=True, pady=10)
        
        # Export buttons
        export_buttons_frame = ctk.CTkFrame(export_frame)
        export_buttons_frame.pack(fill="x", pady=10)
        
        export_excel_btn = ctk.CTkButton(
            export_buttons_frame,
            text="Export to Excel",
            command=self.export_excel,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="green",
            hover_color="darkgreen"
        )
        export_excel_btn.pack(side="left", padx=10, pady=10)
        
        export_csv_btn = ctk.CTkButton(
            export_buttons_frame,
            text="Export to CSV",
            command=self.export_csv,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="blue",
            hover_color="darkblue"
        )
        export_csv_btn.pack(side="left", padx=10, pady=10)
        
    def load_dataset(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Dataset(s)",
            filetypes=[
                ("All Supported Files", "*.xlsx *.xls *.csv"),
                ("Excel files", "*.xlsx *.xls"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        
        if file_paths:
            loaded_count = 0
            error_count = 0
            error_messages = []
            
            for file_path in file_paths:
                try:
                    # Read the file
                    if file_path.endswith(('.xlsx', '.xls')):
                        # Try to read Excel file, handling multiple sheets
                        excel_file = pd.ExcelFile(file_path)
                        if len(excel_file.sheet_names) > 1:
                            # Show sheet selection dialog
                            sheet_name = self.select_sheet(excel_file.sheet_names)
                            if sheet_name is None:
                                continue  # Skip this file if no sheet selected
                        else:
                            sheet_name = excel_file.sheet_names[0]
                        
                        df = pd.read_excel(file_path, sheet_name=sheet_name)
                    else:
                        df = pd.read_csv(file_path)
                    
                    # Try to detect and skip dummy rows
                    df = self.detect_and_skip_dummy_rows(df)
                    
                    # Generate unique dataset name
                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    counter = 1
                    dataset_name = base_name
                    while dataset_name in self.datasets:
                        dataset_name = f"{base_name}_{counter}"
                        counter += 1
                    
                    # Store dataset
                    self.datasets[dataset_name] = df
                    loaded_count += 1
                    
                except Exception as e:
                    error_count += 1
                    error_messages.append(f"Failed to load {os.path.basename(file_path)}: {str(e)}")
            
            # Update UI after all files are processed
            self.update_dataset_list()
            self.update_dataset_selector()
            
            # Show summary message
            if loaded_count > 0:
                success_msg = f"Successfully loaded {loaded_count} dataset{'s' if loaded_count != 1 else ''}"
                if error_count > 0:
                    success_msg += f"\n\nWarning: {error_count} file{'s' if error_count != 1 else ''} failed to load:"
                    success_msg += "\n" + "\n".join(error_messages)
                messagebox.showinfo("Import Complete", success_msg)
            elif error_count > 0:
                error_msg = f"Failed to load {error_count} file{'s' if error_count != 1 else ''}:\n\n"
                error_msg += "\n".join(error_messages)
                messagebox.showerror("Import Failed", error_msg)
    
    def select_sheet(self, sheet_names):
        # Create a simple dialog to select sheet
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Select Sheet")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        result = [None]
        
        ctk.CTkLabel(dialog, text="Select a sheet:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=20)
        
        sheet_var = tk.StringVar(value=sheet_names[0])
        sheet_combo = ctk.CTkComboBox(dialog, values=sheet_names, variable=sheet_var, width=250)
        sheet_combo.pack(pady=10)
        
        def ok_clicked():
            result[0] = sheet_var.get()
            dialog.destroy()
        
        def cancel_clicked():
            dialog.destroy()
        
        ctk.CTkButton(dialog, text="OK", command=ok_clicked).pack(side="left", padx=20, pady=20)
        ctk.CTkButton(dialog, text="Cancel", command=cancel_clicked).pack(side="right", padx=20, pady=20)
        
        dialog.wait_window()
        return result[0]
    
    def detect_and_skip_dummy_rows(self, df):
        # Simple heuristic to detect dummy rows
        # Look for rows where most values are NaN or non-numeric
        for i in range(min(10, len(df))):  # Check first 10 rows
            row = df.iloc[i]
            nan_count = row.isna().sum()
            non_numeric_count = 0
            
            for val in row:
                try:
                    if pd.notna(val):
                        try:
                            float(str(val))
                        except (ValueError, TypeError):
                            non_numeric_count += 1
                except (TypeError, ValueError):
                    non_numeric_count += 1
            
            # If more than 70% of values are NaN or non-numeric, consider it a dummy row
            if (nan_count + non_numeric_count) / len(row) > 0.7:
                continue
            else:
                # Found the header row, return data starting from here
                return df.iloc[i:].reset_index(drop=True)
        
        return df
    
    def update_dataset_list(self):
        self.dataset_listbox.delete(0, tk.END)
        for name, df in self.datasets.items():
            info = self.dataset_info.get(name, {})
            time_period = info.get('time_period', 'Not set')
            service = info.get('service', 'Not set')
            rows = len(df)
            cols = len(df.columns)
            display_text = f"{name} ({rows} rows, {cols} cols) - {time_period} - {service}"
            self.dataset_listbox.insert(tk.END, display_text)
    
    def update_dataset_selector(self):
        values = list(self.datasets.keys())
        self.dataset_selector.configure(values=values)
        if values:
            # Only set if not already set to a valid value
            current = self.dataset_selector.get()
            if current not in values:
                self.dataset_selector.set(values[0])
                self.on_dataset_select(values[0])
            else:
                self.on_dataset_select(current)
    
    def add_dataset_info(self):
        selected_indices = self.dataset_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select a dataset first!")
            return
        
        selected_name = list(self.datasets.keys())[selected_indices[0]]
        time_period = self.time_entry.get().strip()
        service = self.service_entry.get().strip()
        
        if not time_period or not service:
            messagebox.showwarning("Warning", "Please enter both time period and service!")
            return
        
        self.dataset_info[selected_name] = {
            'time_period': time_period,
            'service': service
        }
        
        self.update_dataset_list()
        self.time_entry.delete(0, tk.END)
        self.service_entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", f"Info added for dataset '{selected_name}'!")
    
    def remove_dataset(self):
        selected_indices = self.dataset_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select a dataset to remove!")
            return
        
        selected_name = list(self.datasets.keys())[selected_indices[0]]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to remove dataset '{selected_name}'?"):
            del self.datasets[selected_name]
            if selected_name in self.dataset_info:
                del self.dataset_info[selected_name]
            
            self.update_dataset_list()
            self.update_dataset_selector()
            messagebox.showinfo("Success", f"Dataset '{selected_name}' removed!")
    
    def on_dataset_select(self, dataset_name):
        if dataset_name in self.datasets:
            df = self.datasets[dataset_name]
            self.display_dataframe(df)
            self.update_column_selector(df)
    
    def display_dataframe(self, df):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Set up columns
        columns = list(df.columns)
        self.tree["columns"] = columns
        self.tree["show"] = "headings"
        
        # Configure column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, minwidth=50)
        
        # Insert data (limit to first 100 rows for performance)
        for i, row in df.head(100).iterrows():
            values = []
            for val in row:
                try:
                    if pd.notna(val):
                        values.append(str(val))
                    else:
                        values.append("")
                except (TypeError, ValueError):
                    values.append("")
            self.tree.insert("", "end", values=values)
    
    def update_column_selector(self, df):
        columns = list(df.columns)
        self.column_selector.configure(values=columns)
        if len(columns) > 0:
            self.column_selector.set(columns[0])
    

    def on_column_select(self, column_name):
        self.new_name_entry.delete(0, tk.END)
        self.new_name_entry.insert(0, column_name)

    def update_column_name(self):
        dataset_name = self.dataset_selector.get()
        old_name = self.column_selector.get()
        new_name = self.new_name_entry.get().strip()

        if not dataset_name or not old_name or not new_name:
            messagebox.showwarning("Warning", "Please select dataset and column, and enter new name!")
            return

        if dataset_name in self.datasets:
            self.datasets[dataset_name] = self.datasets[dataset_name].rename(columns={old_name: new_name})
            self.display_dataframe(self.datasets[dataset_name])
            self.update_column_selector(self.datasets[dataset_name])
            messagebox.showinfo("Success", f"Column '{old_name}' renamed to '{new_name}'!")
    
    
    def combine_datasets(self):
        """Combine datasets with robust error handling"""
        try:
            combined_dfs = []
            
            for name, df in self.datasets.items():
                # If dataset_info missing, supply default metadata but record a warning
                if name not in self.dataset_info:
                    print(f"Warning: No info found for dataset '{name}', using default metadata")
                    info = {'time_period': 'Unknown', 'service': 'Unknown'}
                else:
                    info = self.dataset_info[name]
                
                # Create a copy of the dataframe
                df_copy = df.copy()
                
                # Ensure all columns are string type to avoid comparison issues
                for col in df_copy.columns:
                    if df_copy[col].dtype == 'object':
                        df_copy[col] = df_copy[col].astype(str)
                
                # Add time period and service columns
                df_copy['Time_Period'] = str(info['time_period'])
                df_copy['Service'] = str(info['service'])
                df_copy['Dataset_Name'] = str(name)
                
                combined_dfs.append(df_copy)
            
            if not combined_dfs:
                print("Error: No valid datasets to combine")
                return None
            
            # Combine all dataframes using concatenation (stacking)
            # This is the default behavior for the new workflow
            combined = pd.concat(combined_dfs, ignore_index=True, sort=False)
            
            # Ensure all columns are properly typed
            for col in combined.columns:
                if combined[col].dtype == 'object':
                    # Replace 'nan' strings with actual NaN values
                    combined[col] = combined[col].replace('nan', pd.NA)
            
            return combined
            
        except Exception as e:
            print(f"Error in combine_datasets: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def display_combined_data(self):
        if self.combined_data is None:
            return
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Set up columns
        columns = list(self.combined_data.columns)
        self.tree["columns"] = columns
        self.tree["show"] = "headings"
        
        # Configure column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, minwidth=50)
        
        # Insert data (limit to first 100 rows for performance)
        for i, row in self.combined_data.head(100).iterrows():
            values = []
            for val in row:
                try:
                    if pd.notna(val):
                        values.append(str(val))
                    else:
                        values.append("")
                except (TypeError, ValueError):
                    values.append("")
            self.tree.insert("", "end", values=values)
    
    def export_excel(self):
        if self.final_data is None:
            messagebox.showwarning("Warning", "Please complete the data processing workflow first!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Excel File",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.final_data.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Data exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def export_csv(self):
        if self.final_data is None:
            messagebox.showwarning("Warning", "Please complete the data processing workflow first!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save CSV File",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.final_data.to_csv(file_path, index=False)
                messagebox.showinfo("Success", f"Data exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def join_datasets(self):
        """Join all datasets and show preview"""
        if not self.datasets:
            messagebox.showwarning("Warning", "No datasets loaded!")
            return
        
        try:
            # Check if all datasets have required info
            missing_info = [name for name in self.datasets.keys() if name not in self.dataset_info]
            if missing_info:
                # Warn the user but proceed using default metadata for missing datasets
                messagebox.showwarning("Warning", f"Using default metadata for: {', '.join(missing_info)}")
            
            # Combine datasets
            self.combined_data = self.combine_datasets()
            
            if self.combined_data is None:
                messagebox.showerror("Error", "Failed to combine datasets. Check the console for details.")
                return
            
            # Display preview with complete dataset
            if self.combined_data is not None:
                self.display_dataframe_in_tree(self.join_tree, self.combined_data)
                
                # Debug info: rows per dataset and combined shape
                try:
                    per_ds = {name: len(df) for name, df in self.datasets.items()}
                    combined_shape = self.combined_data.shape
                    summary_lines = [f"Datasets included: {len(self.datasets)}"]
                    total_input_rows = 0
                    for k,v in per_ds.items():
                        total_input_rows += v
                        summary_lines.append(f" - {k}: {v} rows")
                    summary_lines.append(f"Combined shape: {combined_shape[0]} rows x {combined_shape[1]} cols")
                    if total_input_rows != combined_shape[0]:
                        summary_lines.append(f"WARNING: Input rows ({total_input_rows}) != Combined rows ({combined_shape[0]})")
                    summary_text = "\n".join(summary_lines)
                    print(summary_text)  # Debug output
                    self.join_summary_label.configure(text=summary_text)
                except Exception as e:
                    print(f"Error updating join summary: {e}")
                    pass
            #except Exception as e:
            #    print(f"Error building join summary: {e}")
            # Mark datasets joined
            self.datasets_joined = True
            # Ensure address selector updated
            column_list = list(self.combined_data.columns)
            try:
                self.address_column_selector.configure(values=column_list)
                if len(column_list) > 0:
                    self.address_column_selector.set(column_list[0])
            except Exception:
                pass
            
            # Update address column selector
            column_list = list(self.combined_data.columns)
            self.address_column_selector.configure(values=column_list)
            if len(column_list) > 0:
                self.address_column_selector.set(column_list[0])
            
            total_rows = len(self.combined_data)
            preview_rows = min(200, total_rows)
            messagebox.showinfo("Success", f"Datasets joined successfully!\n\nTotal rows: {total_rows}\nPreview showing: {preview_rows} rows\n\nYou can now proceed to address cleaning.")
            
        except Exception as e:
            error_msg = f"Failed to join datasets: {str(e)}"
            print(f"Join error: {error_msg}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", error_msg)
    
    def on_address_column_select(self, column_name):
        """Handle address column selection"""
        if self.combined_data is not None and not self.combined_data.columns.empty and column_name in self.combined_data.columns:
            # Update the address column selector with available columns
            self.address_column_selector.set(column_name)

    def save_combined_debug(self):
        """Save the combined dataframe to CSV for debugging purposes"""
        if self.combined_data is None:
            messagebox.showwarning("Warning", "No combined data to save. Please run 'Join Datasets' first.")
            return
        try:
            default_name = f"combined_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            save_path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=default_name, filetypes=[("CSV files","*.csv"), ("All files","*.*")])
            if not save_path:
                return
            # Ensure it's a DataFrame
            if hasattr(self.combined_data, 'to_csv'):
                self.combined_data.to_csv(save_path, index=False)
                messagebox.showinfo("Saved", f"Combined CSV saved to:\n{save_path}")
            else:
                messagebox.showerror("Error", "Combined data is not a valid DataFrame.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save combined CSV: {e}")

    def save_combined_xlsx(self):
        """Save the combined dataframe to XLSX for debugging purposes"""
        if self.combined_data is None:
            messagebox.showwarning("Warning", "No combined data to save. Please run 'Join Datasets' first.")
            return
        try:
            default_name = f"combined_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=default_name, filetypes=[("Excel files","*.xlsx"), ("All files","*.*")])
            if not save_path:
                return
            # Ensure it's a DataFrame
            if hasattr(self.combined_data, 'to_excel'):
                self.combined_data.to_excel(save_path, index=False)
                messagebox.showinfo("Saved", f"Combined XLSX saved to:\n{save_path}")
            else:
                messagebox.showerror("Error", "Combined data is not a valid DataFrame.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save combined XLSX: {e}")
    
    def clean_address_data(self):
        """Clean address data and create apartment indicator"""
        if not self.datasets_joined or self.combined_data is None:
            messagebox.showwarning("Warning", "Please join datasets first!")
            return
        
        address_column = self.address_column_selector.get()
        if not address_column:
            messagebox.showwarning("Warning", "Please select an address column!")
            return
            
        if not address_column in self.combined_data.columns:
            messagebox.showerror("Error", f"Column '{address_column}' not found in combined data!")
            return
        
        if self.combined_data.columns.empty or address_column not in self.combined_data.columns:
            messagebox.showerror("Error", f"Column '{address_column}' not found in data!")
            return
            
        try:
            # Store original data before cleaning
            self.pre_cleaned_data = self.combined_data.copy()
            
            # Create a copy of the combined data
            self.cleaned_data = self.combined_data.copy()
            
            print(f"Processing {len(self.cleaned_data)} rows from combined data...")  # Debug print
            
            # Clean the address column and get results
            results = self.clean_address_column(self.cleaned_data[address_column])
            cleaned_addresses = results[0]
            apartment_indicators = results[1]
            
            # Verify the lengths match
            if len(cleaned_addresses) != len(self.cleaned_data) or len(apartment_indicators) != len(self.cleaned_data):
                raise ValueError(f"Mismatch in processed data lengths: {len(cleaned_addresses)} addresses, {len(apartment_indicators)} indicators, {len(self.cleaned_data)} original rows")
            
            # Add new columns
            new_address_name = f"new_{address_column}"
            self.cleaned_data[new_address_name] = cleaned_addresses
            self.cleaned_data[f"{address_column}_apartment_indicator"] = apartment_indicators
            
            print(f"Processed {len(self.cleaned_data)} rows successfully")  # Debug print
            
            # Set cleaning status
            self.address_cleaning_done = True
            
            # Update the preview
            self.display_dataframe_in_tree(self.clean_tree, self.cleaned_data)
            
            messagebox.showinfo("Success", f"Address cleaning completed successfully!\nProcessed {len(self.cleaned_data)} rows.")
            
        except Exception as e:
            self.address_cleaning_done = False
            error_msg = f"Failed to clean address data: {str(e)}"
            print(f"Cleaning error: {error_msg}")
            messagebox.showerror("Error", error_msg)
            return
        
        try:
            # Create a copy of the combined data
            self.cleaned_data = self.combined_data.copy()
            
            # Clean the address column and get results
            results = self.clean_address_column(self.cleaned_data[address_column])
            cleaned_addresses = results[0]
            apartment_indicators = results[1]
            
            # Add new columns
            new_address_name = f"new_{address_column}"
            self.cleaned_data[new_address_name] = cleaned_addresses
            self.cleaned_data[f"{address_column}_apartment_indicator"] = apartment_indicators
            
            # Display preview
            self.display_dataframe_in_tree(self.clean_tree, self.cleaned_data)
            
            # Update column selectors for additional dataset join
            self.update_join_column_selectors()
            
            messagebox.showinfo("Success", f"Address cleaning completed! Created columns:\n- {new_address_name}\n- {address_column}_apartment_indicator")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clean address data: {str(e)}")
    
    def clean_address_column(self, address_series):
        """Clean address column and create apartment indicator"""
        cleaned_addresses = []
        apartment_indicators = []
        
        for address in address_series:
            try:
                if pd.isna(address) or str(address).strip() == "":
                    cleaned_addresses.append("")
                    apartment_indicators.append("No")
                    continue
            except (TypeError, ValueError):
                # Handle any type conversion issues
                cleaned_addresses.append("")
                apartment_indicators.append("No")
                continue
            
            address_str = str(address).strip()
            original_address = address_str
            
            # Check for apartment indicators
            has_apartment = self.check_apartment_indicator(address_str)
            
            # Clean the address
            cleaned_address = self.remove_apartment_info(address_str)
            
            cleaned_addresses.append(cleaned_address)
            apartment_indicators.append("Yes" if has_apartment else "No")
        
        return pd.Series(cleaned_addresses), pd.Series(apartment_indicators)
    
    def check_apartment_indicator(self, address):
        """Check if address contains apartment-like information"""
        address_upper = address.upper()
        
        # Check for apartment words (as whole words)
        for word in self.settings["apartment_words"]:
            # Use word boundaries to match whole words only
            pattern = r'\b' + re.escape(word.upper()) + r'\b'
            if re.search(pattern, address_upper):
                return True
        
        # Check for PO Box
        for po_box in self.settings["po_box_words"]:
            if po_box.upper() in address_upper:
                return True
        
        # Check for number patterns (but not just ending with a number)
        for pattern in self.settings["number_patterns"]:
            if re.search(pattern, address_upper):
                # Additional check: make sure it's not just a street number
                # Look for apartment-like words before the number
                match = re.search(pattern, address_upper)
                if match:
                    # Check if there's an apartment word before this number
                    before_number = address_upper[:match.start()].strip()
                    # Only consider it an apartment if there's an apartment word or # before the number
                    has_apt_word = False
                    for apt_word in self.settings["apartment_words"]:
                        if apt_word.upper() in before_number:
                            has_apt_word = True
                            break
                    
                    if has_apt_word or '#' in before_number:
                        return True
                    # If it's just a number at the end without apartment words, don't consider it an apartment
        
        return False
    
    def remove_apartment_info(self, address):
        """Remove apartment information from address"""
        address_upper = address.upper()
        
        # Find the earliest occurrence of any apartment word
        earliest_pos = len(address)
        for word in self.settings["apartment_words"]:
            # Use word boundaries to match whole words only
            pattern = r'\b' + re.escape(word.upper()) + r'\b'
            match = re.search(pattern, address_upper)
            if match and match.start() < earliest_pos:
                earliest_pos = match.start()
        
        # Also check for # symbol
        hash_pos = address_upper.find('#')
        if hash_pos != -1 and hash_pos < earliest_pos:
            earliest_pos = hash_pos
        
        # Also check for PO Box
        for po_box in self.settings["po_box_words"]:
            po_pos = address_upper.find(po_box.upper())
            if po_pos != -1 and po_pos < earliest_pos:
                earliest_pos = po_pos
        
        # If no apartment word or # found, return original
        if earliest_pos == len(address):
            return address
        
        # Return address up to the apartment word or #
        return address[:earliest_pos].strip()
    
    def load_additional_dataset(self):
        """Load additional dataset for left join"""
        file_path = filedialog.askopenfilename(
            title="Select Additional Dataset",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Read the file
                if file_path.endswith(('.xlsx', '.xls')):
                    excel_file = pd.ExcelFile(file_path)
                    if len(excel_file.sheet_names) > 1:
                        sheet_name = self.select_sheet(excel_file.sheet_names)
                        if sheet_name is None:
                            return
                    else:
                        sheet_name = excel_file.sheet_names[0]
                    
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                else:
                    df = pd.read_csv(file_path)
                
                # Try to detect and skip dummy rows
                df = self.detect_and_skip_dummy_rows(df)
                
                # Store additional dataset
                self.additional_dataset = df
                
                # Update column selector
                self.additional_join_column.configure(values=list(df.columns))
                if not df.columns.empty:
                    self.additional_join_column.set(df.columns[0])
                
                messagebox.showinfo("Success", "Additional dataset loaded successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load additional dataset: {str(e)}")
    
    def join_additional_dataset(self):
        """Join additional dataset with cleaned data"""
        if self.cleaned_data is None:
            messagebox.showwarning("Warning", "Please clean address data first!")
            return
        
        if self.additional_dataset is None:
            messagebox.showwarning("Warning", "Please load additional dataset first!")
            return
        
        cleaned_column = self.cleaned_join_column.get()
        additional_column = self.additional_join_column.get()
        
        if not cleaned_column or not additional_column:
            messagebox.showwarning("Warning", "Please select join columns!")
            return
        
        try:
            # Perform left join
            self.final_data = self.cleaned_data.merge(
                self.additional_dataset,
                left_on=cleaned_column,
                right_on=additional_column,
                how='left',
                suffixes=('', '_additional')
            )
            
            # Display preview
            self.display_dataframe_in_tree(self.additional_tree, self.final_data)
            
            messagebox.showinfo("Success", "Additional dataset joined successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to join additional dataset: {str(e)}")
    
    def refresh_final_preview(self):
        """Refresh the final preview"""
        if self.final_data is not None:
            self.display_dataframe_in_tree(self.final_tree, self.final_data)
        else:
            messagebox.showwarning("Warning", "No final data to preview!")
    
    def update_join_column_selectors(self):
        """Update join column selectors with cleaned data columns"""
        if self.cleaned_data is not None:
            self.cleaned_join_column.configure(values=list(self.cleaned_data.columns))
            if not self.cleaned_data.columns.empty:
                self.cleaned_join_column.set(self.cleaned_data.columns[0])
    
    def display_dataframe_in_tree(self, tree_widget, dataframe):
        """Display dataframe in tree widget"""
        # Clear existing items
        for item in tree_widget.get_children():
            tree_widget.delete(item)
        
        if dataframe is None or dataframe.empty:
            return
        
        # Set up columns
        columns = list(dataframe.columns)
        tree_widget["columns"] = columns
        tree_widget["show"] = "headings"
        
        # Configure column headings
        for col in columns:
            tree_widget.heading(col, text=col)
            tree_widget.column(col, width=100, minwidth=50)
        
        # Insert data (limit to first 200 rows for performance)
        preview_rows = min(200, len(dataframe))
        for i, row in dataframe.head(preview_rows).iterrows():
            values = []
            for val in row:
                try:
                    if pd.notna(val):
                        values.append(str(val))
                    else:
                        values.append("")
                except (TypeError, ValueError):
                    values.append("")
            tree_widget.insert("", "end", values=values)
    
    def open_settings(self):
        """Open settings window"""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("600x500")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Main frame
        main_frame = ctk.CTkFrame(settings_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="Address Cleaning Settings", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(0, 20))
        
        # Apartment words
        apt_frame = ctk.CTkFrame(main_frame)
        apt_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(apt_frame, text="Apartment Words (one per line):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.apt_words_text = ctk.CTkTextbox(apt_frame, height=100)
        self.apt_words_text.pack(fill="x", padx=10, pady=(0, 10))
        self.apt_words_text.insert("1.0", "\n".join(self.settings["apartment_words"]))
        
        # PO Box words
        po_frame = ctk.CTkFrame(main_frame)
        po_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(po_frame, text="PO Box Words (one per line):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.po_words_text = ctk.CTkTextbox(po_frame, height=80)
        self.po_words_text.pack(fill="x", padx=10, pady=(0, 10))
        self.po_words_text.insert("1.0", "\n".join(self.settings["po_box_words"]))
        
        # Number patterns
        num_frame = ctk.CTkFrame(main_frame)
        num_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(num_frame, text="Number Patterns (regex, one per line):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.num_patterns_text = ctk.CTkTextbox(num_frame, height=80)
        self.num_patterns_text.pack(fill="x", padx=10, pady=(0, 10))
        self.num_patterns_text.insert("1.0", "\n".join(self.settings["number_patterns"]))
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=20)
        
        save_btn = ctk.CTkButton(button_frame, text="Save", command=lambda: self.save_settings_from_window(settings_window))
        save_btn.pack(side="left", padx=10, pady=10)
        
        reset_btn = ctk.CTkButton(button_frame, text="Reset to Default", command=self.reset_settings)
        reset_btn.pack(side="left", padx=10, pady=10)
        
        cancel_btn = ctk.CTkButton(button_frame, text="Cancel", command=settings_window.destroy)
        cancel_btn.pack(side="right", padx=10, pady=10)
    
    def save_settings_from_window(self, window):
        """Save settings from settings window"""
        try:
            # Get apartment words
            apt_words = [word.strip() for word in self.apt_words_text.get("1.0", "end-1c").split("\n") if word.strip()]
            
            # Get PO box words
            po_words = [word.strip() for word in self.po_words_text.get("1.0", "end-1c").split("\n") if word.strip()]
            
            # Get number patterns
            num_patterns = [pattern.strip() for pattern in self.num_patterns_text.get("1.0", "end-1c").split("\n") if pattern.strip()]
            
            # Update settings
            self.settings["apartment_words"] = apt_words
            self.settings["po_box_words"] = po_words
            self.settings["number_patterns"] = num_patterns
            
            # Save to file
            self.save_settings()
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def reset_settings(self):
        """Reset settings to default"""
        default_settings = {
            "apartment_words": ["APT", "APARTMENT", "UNIT", "U", "LOT", "SUITE", "STE", "BLDG", "BUILDING", "FLOOR", "FL", "ROOM", "RM"],
            "po_box_words": ["PO BOX", "P.O. BOX", "POBOX", "P.O.BOX"],
            "number_patterns": [r'\d+$', r'#\d+', r'\d+[A-Z]?$'],
            "case_sensitive": False
        }
        
        self.settings = default_settings
        
        # Update text widgets
        self.apt_words_text.delete("1.0", "end")
        self.apt_words_text.insert("1.0", "\n".join(self.settings["apartment_words"]))
        
        self.po_words_text.delete("1.0", "end")
        self.po_words_text.insert("1.0", "\n".join(self.settings["po_box_words"]))
        
        self.num_patterns_text.delete("1.0", "end")
        self.num_patterns_text.insert("1.0", "\n".join(self.settings["number_patterns"]))
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DataJoinerApp()
    app.run()
