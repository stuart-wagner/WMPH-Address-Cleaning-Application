#!/usr/bin/env python3
"""
Setup script for Data Joiner application
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing packages: {e}. Please ensure requirements.txt is present and valid.")
        return False

# Removed create_demo_data function as demo_usage.py is no longer part of the project.
# If you wish to re-enable demo data creation, you will need to restore demo_usage.py
# and uncomment the relevant sections.

# def create_demo_data():
#     """Create demo data for testing"""
#     print("Creating demo data...")
#     try:
#         import demo_usage
#         demo_usage.create_demo_datasets()
#         print("✓ Demo data created successfully!")
#         return True
#     except Exception as e:
#         print(f"✗ Error creating demo data: {e}")
#         return False

def main():
    """Main setup function"""
    print("=" * 50)
    print("Data Joiner Application Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("✗ Python 3.7 or higher is required!")
        return False
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Demo data creation has been removed.
    # If you need demo data, you will have to create it manually or restore the demo_usage.py script.
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print("\nTo run the application:")
    print("1. Double-click 'run_app.bat'")
    print("2. Or run: `python data_joiner.py`")
    print("\nFor detailed instructions, refer to `UPDATED_WORKFLOW_GUIDE.md`.")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
