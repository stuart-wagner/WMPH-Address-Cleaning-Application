#!/usr/bin/env python3
"""
Defines the default settings for the Data Joiner application.
This provides a single source of truth for default configurations.
"""

class DefaultSettings:
    """A class to hold the default settings for the application."""

    @staticmethod
    def get_defaults():
        """Returns the default settings dictionary."""
        return {
            "apartment_words": [
                "APT", "APARTMENT", "UNIT", "U", "LOT", "SUITE", "STE",
                "BLDG", "BUILDING", "FLOOR", "FL", "ROOM", "RM"
            ],
            "po_box_words": [
                "PO BOX", "P.O. BOX", "POBOX", "P.O.BOX"
            ],
            "number_patterns": [r'\d+$', r'#\d+', r'\d+[A-Z]?$'],
            "case_sensitive": False
        }