## SMARD Data Extractor

## Overview

This Python script automates the process of downloading and consolidating electricity market data from the SMARD (Strommarktdaten) website. It uses Selenium WebDriver to navigate the SMARD download center, select various data categories, and download CSV files. The script then processes these files and combines them into a single consolidated report.

## Features

-   Automated navigation of the SMARD website
-   Customizable date range for data extraction
-   Supports multiple data categories including:
    
    -   Electricity generation
    -   Electricity consumption
    -   Market data
    -   Balancing data
    
-   Consolidates downloaded data into a single CSV file
-   Headless browser operation for efficiency

## Dependencies

The script relies on the following Python libraries:

-   `selenium`: For web automation
-   `pandas`: For data manipulation and CSV handling
-   `os`: For file and directory operations
-   `time`: For implementing delays and timeouts
-   `shutil`: For file moving operations

To install the required dependencies, run:

bash

`pip install selenium pandas` 

Additionally, you need to have Chrome WebDriver installed and accessible in your system PATH.

## Usage

1.  Set up the required variables:
    
    -   `url`: The SMARD download center URL
    -   `base_dir`: The base directory for storing downloaded data and the final report
    -   `download_dir`: The directory where your browser downloads files by default
    -   `from_date`: Start date for data extraction (format: 'MM/DD/YYYY')
    -   `to_date`: End date for data extraction (format: 'MM/DD/YYYY')
    
2.  Run the script:

bash

`python smardDataExtractor.py` 

## Data Extraction

The script extracts the following types of data:

1.  **Electricity Generation**:
    
    -   Actual generation
    -   Forecasted generation (Day-Ahead)
    -   Generation Forecast Intraday
    -   Installed generation capacity
    
2.  **Electricity Consumption**:
    
    -   Actual consumption
    -   Forecasted consumption
    
3.  **Market Data**:
    
    -   Day-ahead prices
    -   Scheduled commercial exchanges
    -   Cross-border physical flows
    
4.  **Balancing Data**:
    
    -   Balancing energy
    -   Costs of TSO
    -   Frequency Containment Reserve
    -   Automatic Frequency Restoration Reserve
    -   Manual Frequency Restoration Reserve
    -   Exported balancing services
    -   Imported balancing services
    

## Output

The script generates two main outputs:

1.  Individual CSV files for each data category, stored in the `data` subdirectory of the specified `base_dir`.
2.  A consolidated CSV file named `consolidated_report.csv` in the `final_report` subdirectory, which combines all the downloaded data with additional columns for Main Category and Data Category.

## Notes

-   The script uses a headless Chrome browser to improve performance and avoid GUI interactions.
-   It implements wait times and checks to ensure proper loading of web elements and successful file downloads.
-   The consolidated report reorders columns to place Main Category and Data Category at the beginning for easier analysis.

## Customization

You can modify the script to:

-   Change the resolution of the data (currently set to hourly)
-   Adjust the file format (currently set to CSV)
-   Select different countries or bidding zones
-   Add or remove specific data categories

Ensure you have the necessary permissions to access the SMARD website and download data before using this script.
