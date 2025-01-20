#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 21:16:50 2025

@author: akash
"""

# install libraries
# !pip install selenium

# Import libraries
import os
import time
import shutil
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Headless action
def setup_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return chrome_options

def create_directories(base_dir):
    os.makedirs(os.path.join(base_dir, 'data'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'final_report'), exist_ok=True)
    print(f"Directories created successfully in {base_dir}")

def check_new_file(download_dir, initial_count, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        current_count = len(os.listdir(download_dir))
        if current_count > initial_count:
            return True
        time.sleep(0.1)
    return False

def select_option(driver, xpath):
    element = driver.find_element(By.XPATH, xpath)
    element.click()
    return element

def download_data(driver, url, download_dir, base_dir, from_date, to_date):
    # Defining keys and xpath's as values according to webpage layout
    main_tag = '/html/body/main/div[2]/div/div[2]/download-center/download-center-market-data/form/div/ui-select[{}]/div/select'
    tag = main_tag + '/option[{}]'
    
    main_category = {
        'Main category: Electricity generation': tag.format(1,2),
        'Main category: Electricity consumption': tag.format(1,3),
        'Main category: Market': tag.format(1,4),
        'Main category: Balancing': tag.format(1,5)
    }

    data_category = {
        'Main category: Electricity generation':{
            'Data category: Actual generation': tag.format(2,2),
            'Data category: Forecasted generation Day-Ahead': tag.format(2,3),
            'Data category: Generation Forecast Intraday': tag.format(2,4),
            'Data category: Installed generation capacity': tag.format(2,5)
        },
        'Main category: Electricity consumption':{
            'Data category: Actual consumption': tag.format(2,2),
            'Data category: Forecasted consumption': tag.format(2,3)
        },
        'Main category: Market':{
            'Data category: Day-ahead prices': tag.format(2,2),
            'Data category: Scheduled commercial exchanges': tag.format(2,3),
            'Data category: Cross-border physical flows': tag.format(2,4)
        },
        'Main category: Balancing':{
            'Data category: Balancing energy': tag.format(2,2),
            'Data category: Costs of TSO': tag.format(2,3),
            'Data category: Frequency Containment Reserve': tag.format(2,4),
            'Data category: Automatic Frequency Restoration Reserve': tag.format(2,5),
            'Data category: Manual Frequency Restoration Reserve': tag.format(2,6),
            'Data category: Exported balancing services': tag.format(2,7),
            'Data category: Imported balancing services': tag.format(2,8)
        }
    }

    country_bidding_zone = {
        'Bidding zone: DE/LU (from 10/01/2018)': tag.format(3,2),
        'Bidding zone: DE/AT/LU (until 09/30/2018)': tag.format(3,3),
        'Country: Germany': tag.format(3,4),
        'Country: Austria': tag.format(3,5),
        'Country: Luxembourg': tag.format(3,6),
        'Control Area (DE): 50Hertz': tag.format(3,7),
        'Control Area (DE): Amprion': tag.format(3,8),
        'Control Area (DE): TenneT': tag.format(3,9),
        'Control Area (DE): TransnetBW': tag.format(3,10),
        'Control Area (AT): APG': tag.format(3,11),
        'Control Area (LU): Creos': tag.format(3,12)
    }

    resolution = {
        'Resolution: original resolution': tag.format(4,2),
        'Resolution: Quarterhour': tag.format(4,3),
        'Resolution: Hour': tag.format(4,4),
        'Resolution: Day': tag.format(4,5),
        'Resolution: Week': tag.format(4,6),
        'Resolution: Month': tag.format(4,7),
        'Resolution: Year': tag.format(4,8),
    }

    file_type = {
        'CSV': tag.format(5,2),
        'XLSX': tag.format(5,3),
        'XML': tag.format(5,4),
    }

    # Navigate to the website
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "help-categories")))

    # Empty df to store results
    consolidated_df = pd.DataFrame()

    for main_key, main_value in main_category.items():
        # Defining opt tag
        opt = "//option[contains(text(), '{}')]"
        
        # Select Main category
        select_option(driver, main_tag.format(1))
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, opt.format(main_key))))
        select_option(driver, main_value)

        for data_key, data_value in data_category[main_key].items():
            # Select Data category
            select_option(driver, main_tag.format(2))
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, opt.format(data_key))))
            select_option(driver, data_value)

            # Enter the "from" date and "to" date
            from_date_input = driver.find_element(By.CSS_SELECTOR, "input.c-date-picker__from")
            to_date_input = driver.find_element(By.CSS_SELECTOR, "input.c-date-picker__to")
            from_date_input.clear()
            from_date_input.send_keys(from_date)
            to_date_input.clear()
            to_date_input.send_keys(to_date)
            select_option(driver, "/html/body/main/div[2]/div/div[2]/download-center/download-center-market-data/div[1]/div[2]/div/div[2]/div/button[2]")

            # Select Country/Bidding Zone
            select_option(driver, main_tag.format(3))
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, opt.format('Country: Germany'))))
            select_option(driver, tag.format(3,4))

            # Select Resolution
            select_option(driver, main_tag.format(4))
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, opt.format('Resolution: Hour'))))
            select_option(driver, tag.format(4,4))

            # Select File Type
            select_option(driver, main_tag.format(5))
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, opt.format('CSV'))))
            select_option(driver, tag.format(5,2))

            # Before starting the download, count files, and their names
            initial_count = len(os.listdir(download_dir))
            before_files = set(os.listdir(download_dir))

            select_option(driver, '//*[@id="help-download"]')

            # Wait for the new file
            if check_new_file(download_dir, initial_count):
                print(f"New file detected for {main_key} - {data_key}")
                time.sleep(2)
                current_files = set(os.listdir(download_dir))
                new_file = list(current_files - before_files)[0]
                shutil.move(os.path.join(download_dir, new_file), os.path.join(base_dir, 'data'))
                df = pd.read_csv(os.path.join(base_dir, 'data', new_file), sep=';')
                df['Main Category'] = main_key
                df['Data Category'] = data_key
                consolidated_df = pd.concat([consolidated_df, df], ignore_index=True)
            else:
                print(f"Download timeout for {main_key} - {data_key}")

            time.sleep(5)

    return consolidated_df

def main(base_dir, url, download_dir, from_date, to_date):
    create_directories(base_dir)
    chrome_options = setup_chrome_options()
    driver = webdriver.Chrome(options=chrome_options)

    try:
        consolidated_df = download_data(driver, url, download_dir, base_dir, from_date, to_date)
        # Reordering the consolidated df columns
        reordered_columns = ['Main Category', 'Data Category'] + [col for col in consolidated_df.columns if col not in ['Main Category', 'Data Category']]
        consolidated_df = consolidated_df[reordered_columns]

        # Display the shape and the first few rows of the DataFrame
        print(f"DataFrame shape: {consolidated_df.shape}")
        print(consolidated_df.head())

        # Saving the consolidated df
        consolidated_df.to_csv(os.path.join(base_dir, 'final_report', 'consolidated_report.csv'), index=False)
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    # Input
    url = r'https://www.smard.de/en/downloadcenter/download-market-data/'
    base_dir = r'/Users/akash/Desktop/akash'
    download_dir = "/Users/akash/Downloads"
    from_date = '01/01/2023'
    to_date = '12/31/2024'

    main(base_dir, url, download_dir, from_date, to_date)