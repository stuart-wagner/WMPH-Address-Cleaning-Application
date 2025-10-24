#!/usr/bin/env python3
"""
Defines a centralized color palette for the Data Joiner application.
This provides a single source of truth for UI colors.
"""

class Colors:
    """A class to hold the color definitions for the application's UI."""

    # --- Standard Action Colors ---
    # Used for primary "go" actions like exporting
    GO_GREEN = "#2CC985"
    GO_GREEN_HOVER = "#28B477"

    # Used for alternative actions
    ACTION_BLUE = "#3B8ED0"
    ACTION_BLUE_HOVER = "#36719F"

    # --- Destructive/Warning Colors ---
    # Used for actions that remove or delete data
    DESTRUCTIVE_RED = "#D32F2F"
    DESTRUCTIVE_RED_HOVER = "#B71C1C"

    # Used for informational warnings or notes
    WARNING_ORANGE = "#E67E22"

    # --- Greyscale for Text and Backgrounds ---
    TEXT_PRIMARY = "#242424"
    TEXT_SECONDARY = "#6E6E6E"