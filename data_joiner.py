import customtkinter as ctk
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
from datetime import datetime
import json
import re
from default_settings import DefaultSettings
from colors import Colors

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class DataJoinerApp:
    def __init__(self):
        # Set appearance mode and color theme
        ctk.set_appearance_mode("light") # Keep light mode
        # Removed ctk.set_default_color_theme("blue") to allow explicit widget colors to take precedence
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("WMPH Client-Services Data Cleaner - Joining and Address Cleaning")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)

        # Set window icon
        try:
            self.root.iconbitmap(resource_path('wmph logo.ico'))
        except Exception as e:
            print(f"Warning: Could not load application icon. {e}")
        
        # Initialize review tab variables
        self.current_preview_dataset = None
        self.column_rename_history = {}
        
        # Initialize data storage
        self.datasets = {}  # Store loaded datasets
        self.dataset_info = {}  # Store time period and service info for each dataset
        self.combined_data = None
        self.deduplicated_data = None
        self.cleaned_data = None
        self.joined_additional_data = None # Data after left join, before deduplication
        self.final_data = None
        self.additional_dataset = None
        self.summarized_additional_data = None
        
        # Status tracking
        self.datasets_joined = False
        self.data_deduplicated = False
        self.address_cleaning_done = False
        self.additional_data_summarized = False # Renamed from additional_join_done
        self.additional_join_done = False
        
        # Backup storage for reverting changes
        self.pre_cleaned_data = None
        self.pre_additional_join_data = None
        self.pre_summarized_data = None
        
        # Settings for address cleaning
        self.settings_file = "settings.json"
        self.load_settings()
        
        # Create the GUI
        self.create_widgets()
    
    def load_settings(self):
        """Load settings from file or create default settings"""
        default_settings = DefaultSettings.get_defaults()
        
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
            text="WMPH Client-Services Data Cleaner", 
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
        self.notebook = ctk.CTkTabview(
            main_frame,
            segmented_button_selected_color=Colors.ACTION_BLUE,
            segmented_button_unselected_color=Colors.ACTION_BLUE_UNSELECTED,
            segmented_button_selected_hover_color=Colors.ACTION_BLUE_HOVER,
            segmented_button_unselected_hover_color=Colors.ACTION_BLUE_HOVER
        )
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
        
        # Step 4: Address Cleaning Tab (was 5)
        self.clean_tab = self.notebook.add("4. Address Cleaning")
        self.create_clean_tab()
        
        # Step 5: Load Additional Dataset Tab (was 6)
        self.additional_tab = self.notebook.add("5. Additional Dataset")
        self.create_additional_tab()
        
        # Step 6: Summarize Data Tab (was 7)
        self.summarize_tab = self.notebook.add("6. Summarize Data")
        self.create_summarize_tab()
        
        # Step 7: Left Join Tab (was 8)
        self.final_tab = self.notebook.add("7. Left Join")
        self.create_final_tab()
        
        # Step 8: Deduplicate by Date Tab (was 4)
        self.deduplicate_tab = self.notebook.add("8. Deduplicate by Date")
        self.create_deduplicate_tab()
        
        # Step 9: Export Tab (remains 9)
        self.export_tab = self.notebook.add("9. Export")
        self.create_export_tab()
        
        # Settings button
        settings_btn = ctk.CTkButton(
            main_frame,
            text="⚙️ Settings",
            command=self.open_settings,
            width=100,
            height=30,
            fg_color=Colors.ACTION_BLUE,
            hover_color=Colors.ACTION_BLUE_HOVER
        )
        settings_btn.pack(side="right", padx=10, pady=10)
        
    def create_load_tab(self):
        # Load datasets section
        load_frame = ctk.CTkFrame(self.load_tab)
        load_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Instructions
        instructions = ctk.CTkLabel(
            load_frame,
            text="Step 1: Load datasets and assign time period & service information",
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
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=Colors.ACTION_BLUE,
            hover_color=Colors.ACTION_BLUE_HOVER
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
        month_label = ctk.CTkLabel(self.info_frame, text="Month:", font=ctk.CTkFont(size=12, weight="bold"))
        month_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December", "NA"]
        self.time_selector = ctk.CTkComboBox(self.info_frame, values=months, width=200)
        self.time_selector.set("NA") # Set default value
        self.time_selector.grid(row=0, column=1, padx=10, pady=10)
        
        # Year input
        year_label = ctk.CTkLabel(self.info_frame, text="Year:", font=ctk.CTkFont(size=12, weight="bold"))
        year_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.year_entry = ctk.CTkEntry(self.info_frame, placeholder_text="e.g., 2023", width=100)
        self.year_entry.grid(row=0, column=3, padx=10, pady=10)

        # Bind the Enter key in the year entry to the add_dataset_info function
        self.year_entry.bind("<Return>", lambda event: self.add_dataset_info())

        # Service input
        service_label = ctk.CTkLabel(self.info_frame, text="Service:", font=ctk.CTkFont(size=12, weight="bold"))
        service_label.grid(row=0, column=4, padx=10, pady=10, sticky="w")
        
        self.service_entry = ctk.CTkEntry(self.info_frame, placeholder_text="e.g., Customer Support, Sales", width=200)
        self.service_entry.grid(row=0, column=5, padx=10, pady=10)
        
        # Bind the Enter key in the service entry to the add_dataset_info function
        self.service_entry.bind("<Return>", lambda event: self.add_dataset_info())
        
        # Add info button
        add_info_btn = ctk.CTkButton(
            self.info_frame,
            text="Add Info",
            command=self.add_dataset_info,
            width=100,
            fg_color=Colors.ACTION_BLUE,
            hover_color=Colors.ACTION_BLUE_HOVER
        )
        add_info_btn.grid(row=0, column=6, padx=10, pady=10)
        
        # Remove dataset button
        remove_btn = ctk.CTkButton(
            load_frame,
            text="Remove Selected Dataset",
            command=self.remove_dataset,
            fg_color=Colors.DESTRUCTIVE_RED,
            hover_color=Colors.DESTRUCTIVE_RED_HOVER,
            text_color=Colors.TEXT_PRIMARY
        )
        remove_btn.pack(pady=10)
    
    def create_join_tab(self):
        """Create the join and preview tab"""
        join_frame = ctk.CTkFrame(self.join_tab)
        join_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Instructions
        instructions = ctk.CTkLabel(
            join_frame,
            text="Step 3: Join datasets and preview the combined result\n• All datasets will be stacked together\n• Time period and service information will be added\n• Review the combined dataset before proceeding",
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
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=Colors.ACTION_BLUE,
            hover_color=Colors.ACTION_BLUE_HOVER
        )
        join_btn.pack(pady=10)
        
        # Debug / summary label to show per-dataset counts and combined shape
        self.join_summary_label = ctk.CTkLabel(join_frame, text="", font=ctk.CTkFont(size=12), justify="left")
        self.join_summary_label.pack(fill="x", padx=10, pady=(0,10))

        # Save Combined CSV button
        self.save_csv_btn = ctk.CTkButton(
            join_frame, 
            text="Save Combined CSV", 
            command=self.save_combined_debug,
            fg_color=Colors.GO_GREEN,
            hover_color=Colors.GO_GREEN_HOVER)
        self.save_csv_btn.pack(pady=(0,5))

        # Save Combined XLSX button
        self.save_xlsx_btn = ctk.CTkButton(join_frame, text="Save Combined XLSX", command=self.save_combined_xlsx,
            fg_color=Colors.GO_GREEN,
            hover_color=Colors.GO_GREEN_HOVER)
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
    
    def create_deduplicate_tab(self):
        """Create the deduplicate by date tab"""
        dedup_frame = ctk.CTkFrame(self.deduplicate_tab)
        dedup_frame.pack(fill="both", expand=True, padx=20, pady=20)

        instructions = ctk.CTkLabel(
            dedup_frame,
            text="Step 8: Keep only the most recent record for each unique entry in a selected column.",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        instructions.pack(pady=(20, 10))

        # Column selection
        column_frame = ctk.CTkFrame(dedup_frame)
        column_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(column_frame, text="Select Column to Group By:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=10, pady=10)
        self.deduplicate_column_selector = ctk.CTkComboBox(column_frame, values=[])
        self.deduplicate_column_selector.pack(side="left", padx=10, pady=10)

        # Deduplicate button
        dedup_btn = ctk.CTkButton(
            dedup_frame, 
            text="Deduplicate by Date", 
            command=self.deduplicate_by_date_action, 
            height=40, font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=Colors.ACTION_BLUE,
            hover_color=Colors.ACTION_BLUE_HOVER)
        dedup_btn.pack(pady=10)

        # Results preview
        self.dedup_preview_frame = ctk.CTkFrame(dedup_frame)
        self.dedup_preview_frame.pack(fill="both", expand=True, pady=10)
        self.dedup_tree_frame = ctk.CTkFrame(self.dedup_preview_frame)
        self.dedup_tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.dedup_tree_scroll_y = tk.Scrollbar(self.dedup_tree_frame)
        self.dedup_tree_scroll_y.pack(side="right", fill="y")
        self.dedup_tree_scroll_x = tk.Scrollbar(self.dedup_tree_frame, orient="horizontal")
        self.dedup_tree_scroll_x.pack(side="bottom", fill="x")
        self.dedup_tree = ttk.Treeview(self.dedup_tree_frame, yscrollcommand=self.dedup_tree_scroll_y.set, xscrollcommand=self.dedup_tree_scroll_x.set)
        self.dedup_tree.pack(side="left", fill="both", expand=True)
        self.dedup_tree_scroll_y.config(command=self.dedup_tree.yview)
        self.dedup_tree_scroll_x.config(command=self.dedup_tree.xview)

    def create_clean_tab(self):
        """Create the address cleaning tab"""
        clean_frame = ctk.CTkFrame(self.clean_tab)
        clean_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Instructions
        instructions = ctk.CTkLabel(
            clean_frame,
            text="Step 4: Clean address data\n• High-confidence words (e.g., 'APT', 'UNIT') are auto-cleaned.\n• Ambiguous patterns (e.g., '#', 'PO BOX') are flagged for review.",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        instructions.pack(pady=(20, 10))
        
        # Address column selection
        column_frame = ctk.CTkFrame(clean_frame)
        column_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(column_frame, text="Select Address Column:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=10, pady=10)
        
        self.address_column_selector = ctk.CTkComboBox(column_frame, values=[])
        self.address_column_selector.pack(side="left", padx=10, pady=10)
        
        # Clean button
        clean_btn = ctk.CTkButton(
            clean_frame,
            text="Clean Address Data",
            command=self.clean_address_data,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=Colors.ACTION_BLUE,
            hover_color=Colors.ACTION_BLUE_HOVER
        )
        clean_btn.pack(pady=10)
        
        # Debug save buttons
        debug_frame = ctk.CTkFrame(clean_frame)
        debug_frame.pack(pady=(0, 10))
        save_cleaned_csv_btn = ctk.CTkButton(
            debug_frame, 
            text="Save Cleaned CSV (Debug)", 
            command=self.save_cleaned_debug_csv,
            fg_color=Colors.GO_GREEN,
            hover_color=Colors.GO_GREEN_HOVER)
        save_cleaned_csv_btn.pack(side="left", padx=5)
        save_cleaned_xlsx_btn = ctk.CTkButton(
            debug_frame, text="Save Cleaned XLSX (Debug)", 
            command=self.save_cleaned_debug_xlsx,
            fg_color=Colors.GO_GREEN,
            hover_color=Colors.GO_GREEN_HOVER)
        save_cleaned_xlsx_btn.pack(side="left", padx=5)

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
            text="Step 5: Load an additional dataset to enrich your data.\n• This dataset will be summarized in the next step before joining.",
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
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=Colors.ACTION_BLUE,
            hover_color=Colors.ACTION_BLUE_HOVER
        )
        load_additional_btn.pack(pady=10)
        
        # Data preview
        self.additional_preview_frame = ctk.CTkFrame(additional_frame)
        self.additional_preview_frame.pack(fill="both", expand=True, pady=10)
        
        # Create treeview for additional data preview
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
    
    def create_summarize_tab(self):
        """Create the summarize additional data tab"""
        summarize_frame = ctk.CTkFrame(self.summarize_tab)
        summarize_frame.pack(fill="both", expand=True, padx=20, pady=20)

        instructions = ctk.CTkLabel(
            summarize_frame,
            text="Step 6: Summarize the additional dataset by a selected column.\n• This creates a count of unique values in that column.",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        instructions.pack(pady=(20, 10))

        # Column selection
        column_frame = ctk.CTkFrame(summarize_frame)
        column_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(column_frame, text="Select Column to Summarize By:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=10, pady=10)
        self.summarize_column_selector = ctk.CTkComboBox(column_frame, values=[])
        self.summarize_column_selector.pack(side="left", padx=10, pady=10)

        # Summarize button
        summarize_btn = ctk.CTkButton(
            summarize_frame, 
            text="Summarize Data", 
            command=self.summarize_additional_data_action, 
            height=40, font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=Colors.ACTION_BLUE,
            hover_color=Colors.ACTION_BLUE_HOVER)
        summarize_btn.pack(pady=10)

        # Results preview
        self.summarize_preview_frame = ctk.CTkFrame(summarize_frame)
        self.summarize_preview_frame.pack(fill="both", expand=True, pady=10)
        self.summarize_tree_frame = ctk.CTkFrame(self.summarize_preview_frame)
        self.summarize_tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.summarize_tree_scroll_y = tk.Scrollbar(self.summarize_tree_frame)
        self.summarize_tree_scroll_y.pack(side="right", fill="y")
        self.summarize_tree_scroll_x = tk.Scrollbar(self.summarize_tree_frame, orient="horizontal")
        self.summarize_tree_scroll_x.pack(side="bottom", fill="x")
        self.summarize_tree = ttk.Treeview(self.summarize_tree_frame, yscrollcommand=self.summarize_tree_scroll_y.set, xscrollcommand=self.summarize_tree_scroll_x.set)
        self.summarize_tree.pack(side="left", fill="both", expand=True)
        self.summarize_tree_scroll_y.config(command=self.summarize_tree.yview)
        self.summarize_tree_scroll_x.config(command=self.summarize_tree.xview)

    def create_final_tab(self):
        """Create the final review tab"""
        final_frame = ctk.CTkFrame(self.final_tab)
        final_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Instructions
        instructions = ctk.CTkLabel(
            final_frame,
            text="Step 7: Join the cleaned data with the summarized additional data.\n• This performs a left join, keeping all rows from your main dataset.",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        instructions.pack(pady=(20, 10))
        
        # Join variables selection
        join_vars_frame = ctk.CTkFrame(final_frame)
        join_vars_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(join_vars_frame, text="Cleaned Data Column:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=10, pady=10)
        self.cleaned_join_column = ctk.CTkComboBox(join_vars_frame, values=[])
        self.cleaned_join_column.pack(side="left", padx=10, pady=10)
        
        ctk.CTkLabel(join_vars_frame, text="Additional Data Column:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=10, pady=10)
        self.additional_join_column = ctk.CTkComboBox(join_vars_frame, values=[])
        self.additional_join_column.pack(side="left", padx=10, pady=10)
        
        # Join button
        join_additional_btn = ctk.CTkButton(
            final_frame,
            text="Join Datasets",
            command=self.join_additional_dataset,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=Colors.ACTION_BLUE,
            hover_color=Colors.ACTION_BLUE_HOVER
        )
        join_additional_btn.pack(pady=10)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            final_frame,
            text="Refresh Preview",
            command=self.refresh_final_preview,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=Colors.ACTION_BLUE,
            hover_color=Colors.ACTION_BLUE_HOVER
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
        self.update_column_btn = ctk.CTkButton(
            self.column_edit_frame, 
            text="Update Column Name", 
            command=self.update_column_name,
            fg_color=Colors.ACTION_BLUE,
            hover_color=Colors.ACTION_BLUE_HOVER)
        self.update_column_btn.pack(side="left", padx=10, pady=10)

        # Add button to update dataset selector
        self.refresh_btn = ctk.CTkButton(
            selector_frame, 
            text="Refresh Dataset List", 
            command=self.update_dataset_selector,
            fg_color=Colors.ACTION_BLUE,
            hover_color=Colors.ACTION_BLUE_HOVER)
        self.refresh_btn.pack(side="left", padx=10, pady=10)
        
    def create_export_tab(self):
        """Create the export tab"""
        export_frame = ctk.CTkFrame(self.export_tab)
        export_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Instructions
        instructions = ctk.CTkLabel(
            export_frame,
            text="Step 9: Export final dataset\n• Export the complete merged dataset\n• Choose between Excel or CSV format\n• Save your processed data",
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
            text="Note: Make sure you have completed all previous steps before exporting.",
            font=ctk.CTkFont(size=12),
            text_color=Colors.WARNING_ORANGE
        )
        note_label.pack(pady=10)
        
        # Combined data preview
        self.combined_preview_frame = ctk.CTkFrame(export_frame)
        self.combined_preview_frame.pack(fill="both", expand=True, pady=10)
        
        # Export buttons
        export_buttons_frame = ctk.CTkFrame(export_frame)
        export_buttons_frame.pack(fill="x", pady=10)
        
        # Frame for pre-deduplication export
        pre_dedup_frame = ctk.CTkFrame(export_buttons_frame)
        pre_dedup_frame.pack(side="left", padx=20, pady=10, fill="x", expand=True)
        ctk.CTkLabel(pre_dedup_frame, text="Export Before Deduplication (from Step 7)", font=ctk.CTkFont(weight="bold")).pack(pady=(5,10))
        
        export_excel_pre_btn = ctk.CTkButton(
            pre_dedup_frame,
            text="Export to Excel (with duplicates)",
            command=lambda: self.export_excel(pre_deduplication=True),
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=Colors.GO_GREEN,
            hover_color=Colors.GO_GREEN_HOVER
        )
        export_excel_pre_btn.pack(side="left", padx=10, pady=10)
        
        # Frame for post-deduplication export
        post_dedup_frame = ctk.CTkFrame(export_buttons_frame)
        post_dedup_frame.pack(side="right", padx=20, pady=10, fill="x", expand=True)
        ctk.CTkLabel(post_dedup_frame, text="Export After Deduplication (from Step 8)", font=ctk.CTkFont(weight="bold")).pack(pady=(5,10))

        export_excel_post_btn = ctk.CTkButton(
            post_dedup_frame,
            text="Export to Excel (deduplicated)",
            command=lambda: self.export_excel(pre_deduplication=False),
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=Colors.GO_GREEN,
            hover_color=Colors.GO_GREEN_HOVER
        )
        export_excel_post_btn.pack(side="left", padx=10, pady=10)
        
        export_csv_post_btn = ctk.CTkButton(
            export_buttons_frame,
            text="Export to CSV (deduplicated)",
            command=lambda: self.export_csv(pre_deduplication=False),
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=Colors.ACTION_BLUE,
            hover_color=Colors.ACTION_BLUE_HOVER
        )
        
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
            month = info.get('month', 'Not set')
            year = info.get('year', 'Not set')
            service = info.get('service', 'Not set')
            rows = len(df)
            cols = len(df.columns)
            display_text = f"{name} ({rows} rows, {cols} cols) - {month} {year} - {service}"
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
        month = self.time_selector.get().strip()
        year_str = self.year_entry.get().strip()
        service = self.service_entry.get().strip()
        
        if not month or not service or not year_str:
            messagebox.showwarning("Warning", "Please enter Month, Year, and Service!")
            return

        try:
            year_val = int(year_str)
        except ValueError:
            messagebox.showwarning("Warning", "Year must be an integer value (e.g., 2023).")
            return
        
        self.dataset_info[selected_name] = {
            'month': month,
            'year': year_val,
            'service': service
        }
        
        self.update_dataset_list()
    
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
        dataset_name = self.dataset_selector.get() # This is a primary action. The default blue theme is probably fine, but I can make it explicit. Let's use `ACTION_BLUE`.
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
            # Establish a stable and predictable column order.
            # Start with the columns from the first loaded dataset, then append new ones.
            if not self.datasets:
                return None

            # Get columns from the first dataset in order
            first_dataset_name = next(iter(self.datasets))
            ordered_columns = list(self.datasets[first_dataset_name].columns)
            
            # Discover new columns from other datasets
            all_columns_set = set(ordered_columns)
            for name, df in self.datasets.items():
                for col in df.columns:
                    if col not in all_columns_set:
                        ordered_columns.append(col)
                        all_columns_set.add(col)

            combined_dfs = []
            
            for name, df in self.datasets.items():
                # If dataset_info missing, supply default metadata but record a warning
                if name not in self.dataset_info:
                    print(f"Warning: No info found for dataset '{name}', using default metadata")
                    info = {'month': 'Unknown', 'year': 0, 'service': 'Unknown'}
                else:
                    info = self.dataset_info[name]
                
                # Create a copy of the dataframe
                df_copy = df.copy()

                # Reindex to ensure all dataframes have the same columns, filling missing with empty string
                df_copy = df_copy.reindex(columns=ordered_columns, fill_value="")
                
                # Add metadata columns
                # Use .get() with a default value for safety, although the check above should handle it.
                df_copy['Month'] = str(info.get('month', 'Unknown'))
                df_copy['Year'] = info.get('year', 0)
                df_copy['Service'] = str(info.get('service', 'Unknown'))
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

    def export_excel(self, pre_deduplication=False):
        if pre_deduplication:
            data_to_export = self.joined_additional_data
            if data_to_export is None:
                messagebox.showwarning("Warning", "Please complete the workflow up to Step 7 (Left Join) first!")
                return
        else:
            data_to_export = self.final_data
            if data_to_export is None:
                messagebox.showwarning("Warning", "Please complete the workflow up to Step 8 (Deduplication) first!")
                return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Excel File",
            initialfile=f"export_{'with_duplicates' if pre_deduplication else 'deduplicated'}_{datetime.now().strftime('%Y%m%d')}.xlsx",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.final_data.to_excel(file_path, index=False)
                data_to_export.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Data exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def export_csv(self, pre_deduplication=False):
        if pre_deduplication:
            data_to_export = self.joined_additional_data
            if data_to_export is None:
                messagebox.showwarning("Warning", "Please complete the workflow up to Step 7 (Left Join) first!")
                return
        else:
            data_to_export = self.final_data
            if data_to_export is None:
                messagebox.showwarning("Warning", "Please complete the workflow up to Step 8 (Deduplication) first!")
                return
        
        file_path = filedialog.asksaveasfilename(
            title="Save CSV File",
            initialfile=f"export_{'with_duplicates' if pre_deduplication else 'deduplicated'}_{datetime.now().strftime('%Y%m%d')}.csv",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.final_data.to_csv(file_path, index=False)
                data_to_export.to_csv(file_path, index=False)
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
            column_list = list(self.combined_data.columns) if self.combined_data is not None else []
            # Update column selector for the next step (Address Cleaning)
            try:
                self.address_column_selector.configure(values=column_list)
                if column_list:
                    self.address_column_selector.set(column_list[0])
            except Exception:
                pass # Ignore if widget doesn't exist yet
            
            total_rows = len(self.combined_data)
            preview_rows = min(200, total_rows)
            messagebox.showinfo("Success", f"Datasets joined successfully!\n\nTotal rows: {total_rows}\nPreview showing: {preview_rows} rows\n\nYou can now proceed to address cleaning.")
            
        except Exception as e:
            error_msg = f"Failed to join datasets: {str(e)}"
            print(f"Join error: {error_msg}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", error_msg)
    
    def deduplicate_by_date_action(self):
        """Groups by a column and keeps the most recent entry based on Year and Month."""
        if not self.additional_join_done or self.joined_additional_data is None:
            messagebox.showwarning("Warning", "Please complete the Left Join in Step 7 first.")
            return

        group_by_col = self.deduplicate_column_selector.get()
        if not group_by_col:
            messagebox.showwarning("Warning", "Please select a column to group by.")
            return
        
        try:
            df = self.joined_additional_data.copy()

            # Map month names to numbers for sorting. 'NA' becomes 0 (oldest).
            month_map = {
                "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
                "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12,
                "NA": 0
            }
            # Ensure 'Month' column exists before mapping
            if 'Month' in df.columns:
                df['Month_Num'] = df['Month'].map(month_map).fillna(0)
            else:
                messagebox.showerror("Error", "The 'Month' column is required for deduplication but was not found.")
                return

            # Sort by Year and Month_Num descending to bring the most recent to the top of each group
            df_sorted = df.sort_values(by=['Year', 'Month_Num'], ascending=[False, False])

            # Drop duplicates on the selected column, keeping the first (most recent) entry
            self.final_data = df_sorted.drop_duplicates(subset=[group_by_col], keep='first')

            # Clean up the temporary Month_Num column
            self.final_data = self.final_data.drop(columns=['Month_Num'])
            self.data_deduplicated = True

            # Update UI
            self.display_dataframe_in_tree(self.dedup_tree, self.final_data)

            messagebox.showinfo("Success", f"Deduplication complete. Kept the most recent record for each unique '{group_by_col}'.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to deduplicate data: {str(e)}")

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
    
    def save_cleaned_debug_csv(self):
        """Save the cleaned dataframe to CSV for debugging purposes"""
        if self.cleaned_data is None:
            messagebox.showwarning("Warning", "No cleaned data to save. Please run 'Clean Address Data' first.")
            return
        try:
            default_name = f"cleaned_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            save_path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=default_name, filetypes=[("CSV files","*.csv"), ("All files","*.*")])
            if not save_path:
                return
            if hasattr(self.cleaned_data, 'to_csv'):
                self.cleaned_data.to_csv(save_path, index=False)
                messagebox.showinfo("Saved", f"Cleaned CSV saved to:\n{save_path}")
            else:
                messagebox.showerror("Error", "Cleaned data is not a valid DataFrame.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save cleaned CSV: {e}")

    def save_cleaned_debug_xlsx(self):
        """Save the cleaned dataframe to XLSX for debugging purposes"""
        if self.cleaned_data is None:
            messagebox.showwarning("Warning", "No cleaned data to save. Please run 'Clean Address Data' first.")
            return
        try:
            default_name = f"cleaned_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=default_name, filetypes=[("Excel files","*.xlsx"), ("All files","*.*")])
            if not save_path:
                return
            if hasattr(self.cleaned_data, 'to_excel'):
                self.cleaned_data.to_excel(save_path, index=False)
                messagebox.showinfo("Saved", f"Cleaned XLSX saved to:\n{save_path}")
            else:
                messagebox.showerror("Error", "Cleaned data is not a valid DataFrame.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save cleaned XLSX: {e}")

    def clean_address_data(self):
        """Clean address data and create apartment indicator"""
        if not self.datasets_joined or self.combined_data is None:
            messagebox.showwarning("Warning", "Please join datasets in Step 3 first!")
            return
        
        address_column = self.address_column_selector.get()
        if not address_column:
            messagebox.showwarning("Warning", "Please select an address column!")
            return
            
        if not address_column in self.combined_data.columns:
            messagebox.showerror("Error", f"Column '{address_column}' not found in the joined data!")
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
            cleaned_addresses, auto_cleaned_flags, may_have_word_flags = self.clean_address_column(self.cleaned_data[address_column])
            
            # Verify the lengths match
            if not (len(cleaned_addresses) == len(self.cleaned_data) and len(auto_cleaned_flags) == len(self.cleaned_data) and len(may_have_word_flags) == len(self.cleaned_data)):
                raise ValueError(f"Mismatch in processed data lengths after cleaning.")
            
            # CRITICAL FIX: Ensure the index of the new Series matches the DataFrame's index to prevent misalignment.
            cleaned_addresses.index = self.cleaned_data.index
            auto_cleaned_flags.index = self.cleaned_data.index
            may_have_word_flags.index = self.cleaned_data.index

            # Add new columns
            new_address_name = f"new_{address_column}"
            auto_cleaned_col_name = f"{address_column}_auto_cleaned"
            may_have_word_col_name = f"{address_column}_may_have_word"

            self.cleaned_data[new_address_name] = cleaned_addresses
            self.cleaned_data[auto_cleaned_col_name] = auto_cleaned_flags
            self.cleaned_data[may_have_word_col_name] = may_have_word_flags
            
            print(f"Processed {len(self.cleaned_data)} rows successfully")  # Debug print
            
            # Set cleaning status
            self.address_cleaning_done = True
            
            # Display preview
            self.display_dataframe_in_tree(self.clean_tree, self.cleaned_data)
            
            # Update column selectors for additional dataset join
            self.update_join_column_selectors()
            
            messagebox.showinfo("Success", f"Address cleaning completed! Created columns:\n- {new_address_name}\n- {auto_cleaned_col_name}\n- {may_have_word_col_name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clean address data: {str(e)}")
    
    def clean_address_column(self, address_series):
        """
        Processes an address series based on new rules:
        1. Auto-cleans addresses with high-confidence 'apartment_words'.
        2. Flags addresses with ambiguous patterns ('#', PO Box, number patterns) for manual review.
        Returns three Series: cleaned_addresses, auto_cleaned_flags, may_have_word_flags.
        """
        cleaned_addresses = []
        auto_cleaned_flags = []
        may_have_word_flags = []
        
        for address in address_series:
            # First, check for pandas NA/NaN values. This is the most reliable check for missing data.
            if pd.isna(address):
                cleaned_addresses.append("")
                auto_cleaned_flags.append("No")
                may_have_word_flags.append("No")
                continue

            # If not NA, convert to string and check if it's empty after stripping whitespace.
            address_str = str(address).strip()
            if not address_str:
                cleaned_addresses.append("")
                auto_cleaned_flags.append("No")
                may_have_word_flags.append("No")
                continue

            address_upper = address_str.upper()
            
            # --- 1. High-Confidence Auto-Cleaning ---
            earliest_pos = len(address_str)
            found_apt_word = False
            for word in self.settings["apartment_words"]:
                pattern = r'\b' + re.escape(word.upper()) + r'\b'
                match = re.search(pattern, address_upper)
                if match and match.start() < earliest_pos:
                    earliest_pos = match.start()
                    found_apt_word = True
            
            if found_apt_word:
                cleaned_addresses.append(address_str[:earliest_pos].strip())
                auto_cleaned_flags.append("Yes")
                may_have_word_flags.append("No") # If auto-cleaned, no need for manual review flag
                continue

            # --- 2. Flag for Manual Review (No Auto-Cleaning) ---
            flag_for_review = False
            # Check for '#' symbol
            if '#' in address_str:
                flag_for_review = True
            
            # Check for PO Box words
            if not flag_for_review:
                for po_box in self.settings["po_box_words"]:
                    if po_box.upper() in address_upper:
                        flag_for_review = True
                        break
            
            # Check for number patterns
            if not flag_for_review:
                for pattern in self.settings["number_patterns"]:
                    if re.search(pattern, address_upper):
                        flag_for_review = True
                        break
            
            # --- 3. Final Assignment ---
            if flag_for_review:
                cleaned_addresses.append(address_str) # Keep original address
                auto_cleaned_flags.append("No")
                may_have_word_flags.append("Yes")
            else:
                # No indicators found
                cleaned_addresses.append(address_str)
                auto_cleaned_flags.append("No")
                may_have_word_flags.append("No")

        return pd.Series(cleaned_addresses), pd.Series(auto_cleaned_flags), pd.Series(may_have_word_flags)
    
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
                
                # Update column selector for summarization tab
                self.summarize_column_selector.configure(values=list(df.columns))
                if not df.columns.empty:
                    self.summarize_column_selector.set(df.columns[0])
                
                # Display preview
                self.display_dataframe_in_tree(self.additional_tree, self.additional_dataset)
                
                messagebox.showinfo("Success", "Additional dataset loaded successfully! You can now proceed to Step 6 to summarize it.")
                
            except Exception as e:
                self.additional_dataset = None
                messagebox.showerror("Error", f"Failed to load additional dataset: {str(e)}")
    
    def join_additional_dataset(self):
        """Join additional dataset with cleaned data"""
        if self.cleaned_data is None:
            messagebox.showwarning("Warning", "Please clean address data first!")
            return
        
        if self.summarized_additional_data is None:
            messagebox.showwarning("Warning", "Please summarize the additional dataset in Step 7 first!")
            return
        
        cleaned_column = self.cleaned_join_column.get()
        additional_column = self.additional_join_column.get()
        
        if not cleaned_column or not additional_column:
            messagebox.showwarning("Warning", "Please select join columns!")
            return
        
        try:
            # Perform left join
            self.joined_additional_data = self.cleaned_data.merge(
                self.summarized_additional_data,
                left_on=cleaned_column,
                right_on=additional_column,
                how='left',
                suffixes=('', '_additional')
            )
            self.additional_join_done = True

            # Display preview
            self.display_dataframe_in_tree(self.final_tree, self.joined_additional_data)

            # Update column selector for the next step (Deduplication)
            if self.joined_additional_data is not None:
                self.deduplicate_column_selector.configure(values=list(self.joined_additional_data.columns))
                if not self.joined_additional_data.columns.empty:
                    self.deduplicate_column_selector.set(self.joined_additional_data.columns[0])
            
            messagebox.showinfo("Success", "Additional dataset joined successfully! You can now proceed to Step 8 to deduplicate.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to join additional dataset: {str(e)}")
    
    def refresh_final_preview(self):
        """Refresh the final preview"""
        if self.joined_additional_data is not None:
            self.display_dataframe_in_tree(self.final_tree, self.joined_additional_data)
        else:
            messagebox.showwarning("Warning", "No final data to preview!")
    
    def update_join_column_selectors(self):
        """Update join column selectors with cleaned data columns"""
        if self.cleaned_data is not None:
            self.cleaned_join_column.configure(values=list(self.cleaned_data.columns))
            if not self.cleaned_data.columns.empty:
                self.cleaned_join_column.set(self.cleaned_data.columns[0])
    
    def summarize_additional_data_action(self):
        """Summarize the additional dataset by a selected column."""
        if self.additional_dataset is None:
            messagebox.showwarning("Warning", "Please load an additional dataset in Step 5 first.")
            return

        summarize_col = self.summarize_column_selector.get()
        if not summarize_col:
            messagebox.showwarning("Warning", "Please select a column to summarize by.")
            return

        try:
            # Perform value_counts
            summary = self.additional_dataset[summarize_col].value_counts().reset_index()
            summary.columns = [summarize_col, 'Count']

            self.summarized_additional_data = summary
            self.additional_data_summarized = True

            # Display preview
            self.display_dataframe_in_tree(self.summarize_tree, self.summarized_additional_data)

            # Update column selectors for the final join tab
            if self.summarized_additional_data is not None:
                self.additional_join_column.configure(values=list(self.summarized_additional_data.columns))
                if not self.summarized_additional_data.columns.empty:
                    self.additional_join_column.set(self.summarized_additional_data.columns[0])

            messagebox.showinfo("Success", f"Data summarized by '{summarize_col}'. You can now proceed to Step 7 to join this summary.")

        except Exception as e:
            self.summarized_additional_data = None
            self.additional_data_summarized = False
            messagebox.showerror("Error", f"Failed to summarize data: {str(e)}")
    
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
        settings_window.geometry("600x550")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Title
        title_label = ctk.CTkLabel(settings_window, text="Address Cleaning Settings", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(20, 10))
        
        # Create a scrollable frame to hold all settings content
        scrollable_frame = ctk.CTkScrollableFrame(settings_window)
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Apartment words
        apt_frame = ctk.CTkFrame(scrollable_frame)
        apt_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(apt_frame, text="Apartment Words (one per line):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.apt_words_text = ctk.CTkTextbox(apt_frame, height=120)
        self.apt_words_text.pack(fill="x", padx=10, pady=(0, 10))
        self.apt_words_text.insert("1.0", "\n".join(self.settings["apartment_words"]))
        
        # PO Box words
        po_frame = ctk.CTkFrame(scrollable_frame)
        po_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(po_frame, text="PO Box Words (one per line):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.po_words_text = ctk.CTkTextbox(po_frame, height=100)
        self.po_words_text.pack(fill="x", padx=10, pady=(0, 10))
        self.po_words_text.insert("1.0", "\n".join(self.settings["po_box_words"]))
        
        # Number patterns
        num_frame = ctk.CTkFrame(scrollable_frame)
        num_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(num_frame, text="Number Patterns (regex, one per line):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.num_patterns_text = ctk.CTkTextbox(num_frame, height=100)
        self.num_patterns_text.pack(fill="x", padx=10, pady=(0, 10))
        self.num_patterns_text.insert("1.0", "\n".join(self.settings["number_patterns"]))
        
        # Buttons
        button_frame = ctk.CTkFrame(scrollable_frame)
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
        default_settings = DefaultSettings.get_defaults()
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
