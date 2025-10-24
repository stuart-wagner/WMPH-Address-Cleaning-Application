#!/usr/bin/env python3
"""
Defines a centralized color palette for the Data Joiner application.
This provides a single source of truth for UI colors.
"""

class Colors:
    """A class to hold the color definitions for the application's UI."""

    # --- Standard Action Colors ---
    # Used for primary "go" actions like exporting
    GO_GREEN = "#00AE4C" # Primary green for success/export actions
    GO_GREEN_HOVER = "#008C3D" # Darker green for hover state

    # --- Action Blue Palette ---
    ACTION_BLUE = "#4A53A5"  # Main blue for buttons, selected tabs
    ACTION_BLUE_HOVER = "#5A64B4" # Slightly lighter blue for hover states
    ACTION_BLUE_UNSELECTED = "#7A82C0" # Lighter blue for unselected tabs

    # --- Destructive/Warning Colors ---
    # Used for actions that remove or delete data (currently orange as per user's last change)
    DESTRUCTIVE_RED = "#F7971D" # Orange for destructive actions (as per user's last change)
    DESTRUCTIVE_RED_HOVER = "#D47B1A" # Darker orange for hover state

    # Used for informational warnings or notes
    WARNING_ORANGE = "#E67E22"

    # --- Greyscale for Text and Backgrounds ---
    TEXT_PRIMARY = "#2F2F2F"#242424"
    TEXT_SECONDARY = "#6E6E6E"
    
