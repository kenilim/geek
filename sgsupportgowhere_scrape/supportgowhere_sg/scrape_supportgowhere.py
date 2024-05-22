import csv
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options

def init_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Edge(service=EdgeService("/usr/local/bin/msedgedriver"), options=options)
    return driver

def read_urls(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def scrape_data(driver, url):
    driver.get(url)
    time.sleep(2)  # Wait for the page to load
    data = {'Content': '', 'Source URL': url}

    try:
        content_element = driver.find_element(By.TAG_NAME, 'body')
        data['Content'] = content_element.text.replace(';', ' ').replace('\n', ' ').strip()
    except Exception as e:
        print(f"Error extracting content: {e}")

    return data

def write_to_csv(data, output_file):
    file_exists = os.path.isfile(output_file)
    with open(output_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        if not file_exists:
            writer.writerow(['Content', 'Source URL'])
        writer.writerow([data['Content'], data['Source URL']])

def write_to_xlsx(data_list, output_file):
    df = pd.DataFrame(data_list, columns=['Content', 'Source URL'])
    df.to_excel(output_file, index=False)

def main():
    urls_file_path = '/Users/kenilim/geek/sgsupportgowhere_scrape/supportgowhere_sg/all_urls.txt'
    output_csv_file = '/Users/kenilim/geek/sgsupportgowhere_scrape/supportgowhere_sg/scraped_data.csv'
    output_xlsx_file = '/Users/kenilim/geek/sgsupportgowhere_scrape/supportgowhere_sg/scraped_data.xlsx'

    urls = read_urls(urls_file_path)
    driver = init_driver()
    all_data = []

    for url in urls:
        data = scrape_data(driver, url)
        write_to_csv(data, output_csv_file)
        all_data.append(data)
        print(f"Data written to CSV for URL: {url}")

    driver.quit()

    write_to_xlsx(all_data, output_xlsx_file)
    print(f"Data written to XLSX file: {output_xlsx_file}")

if __name__ == "__main__":
    main()
