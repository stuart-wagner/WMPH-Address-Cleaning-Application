@echo off
echo =================================================================
echo =           Building Standalone Executable for Data Joiner        =
echo =================================================================
echo.
echo This script will use PyInstaller to package the Python application
echo into a standalone executable in the 'dist' folder.
echo.
echo Press any key to begin the checks...
pause

REM Step 1: Check if the 'python' command itself is available.
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [FATAL ERROR] The 'python' command was not found.
    echo Please ensure Python is installed and that its location is added to your system's PATH environment variable.
    pause
    exit /b 1
)

REM Step 2: Now that we know 'python' works, check for PyInstaller.
python -m PyInstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] PyInstaller is not installed or could not be found.
    echo Please install it by running: python -m pip install pyinstaller
    pause
    exit /b 1
)

echo.
echo [SUCCESS] PyInstaller was found.
echo Press any key to start the build process...
pause
echo.

echo Cleaning up previous build directories...
REM Forcefully remove the previous build output and temporary directories.
REM This helps prevent "Access is denied" errors from locked files.
if exist "WMPH_Data_Cleaner" (
    echo Deleting old 'WMPH_Data_Cleaner' directory...
    rmdir /s /q "WMPH_Data_Cleaner"
)
if exist "build_temp" (
    echo Deleting old 'build_temp' directory...
    rmdir /s /q "build_temp"
)
echo Cleanup complete.
echo.

echo Running PyInstaller...
REM The main build command. We set the output directory to the current folder ('.')
python -m PyInstaller --name "WMPH_Data_Cleaner" --windowed --noconfirm --distpath "." --workpath "build_temp" --icon="wmph logo.ico" --add-data "wmph logo.ico;." --add-data "default_settings.py;." --add-data "colors.py;." data_joiner.py

REM Check if the PyInstaller command was successful
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] PyInstaller failed to build the executable. See the error messages above.
    pause
    exit /b 1
)

echo.
echo =================================================================
echo =                      Build Complete!                          =
echo =================================================================
echo The distributable application is located in:
echo %~dp0WMPH_Data_Cleaner
echo.
echo You can zip the 'WMPH_Data_Cleaner' folder and share it.
echo.
pause