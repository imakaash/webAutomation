# SMARD Data Extractor

## Overview

This Python script automates the process of downloading and consolidating electricity market data from the SMARD (Strommarktdaten) website. It uses Selenium WebDriver to navigate the SMARD download center, select various data categories, and download CSV files. The script then processes these files and combines them into a single consolidated report.

## Features

-   Automated navigation of the SMARD website
-   Dynamic date range for data extraction (last 2 years from current date)
-   Supports multiple data categories including:
    
    -   Electricity generation
    -   Electricity consumption
    -   Market data
    -   Balancing data
    
-   Consolidates downloaded data into a single CSV file
-   Headless browser operation for efficiency
-   Cross-platform compatibility for download directory detection

## Dependencies

The script relies on the following Python libraries:

-   `selenium`: For web automation
-   `pandas`: For data manipulation and CSV handling
-   `os`: For file and directory operations
-   `time`: For implementing delays and timeouts
-   `shutil`: For file moving operations
-   `platform`: For cross-platform compatibility
-   `datetime`: For date calculations

To install the required dependencies, run:

bash

`pip install selenium pandas` 

Additionally, you need to have Chrome WebDriver installed and accessible in your system PATH.

## Usage

1.  Ensure all dependencies are installed and Chrome WebDriver is set up.
2.  Run the script:

bash

`python smard_data_extractor.py` 

The script automatically sets the date range to cover the last 2 years from the current date.

## Data Extraction

The script extracts data for various categories as defined in the `main_category` and `data_category` dictionaries within the code.

## Output

The script generates two main outputs:

1.  Individual CSV files for each data category, stored in the `data` subdirectory of the current working directory.
2.  A consolidated CSV file named `consolidated_report.csv` in the `final_report` subdirectory, which combines all the downloaded data with additional columns for Main Category and Data Category.

## Key Functions

-   `setup_chrome_options()`: Configures Chrome for headless operation.
-   `manage_directory()`: Creates or clears directories for data storage.
-   `check_new_file()`: Monitors the download directory for new files.
-   `select_option()`: Performs click operations on web elements.
-   `get_download_path()`: Determines the default download directory for the current operating system.
-   `download_data()`: Main function for navigating the website and downloading data.
-   `main()`: Orchestrates the entire data extraction and consolidation process.

## Customization

You can modify the script by adjusting the dictionaries that define the data categories, resolutions, and file types. The current settings are:

-   Resolution: Hourly
-   File Type: CSV
-   Country: Germany

## Notes

-   The script uses a headless Chrome browser to improve performance and avoid GUI interactions.
-   It implements wait times and checks to ensure proper loading of web elements and successful file downloads.
-   The consolidated report reorders columns to place Main Category and Data Category at the beginning for easier analysis.
-   The script is designed to work across different operating systems, automatically detecting the appropriate download directory.

Ensure you have the necessary permissions to access the SMARD website and download data before using this script.