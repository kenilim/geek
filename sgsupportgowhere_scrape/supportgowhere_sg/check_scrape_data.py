import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def init_driver():
    options = webdriver.EdgeOptions()
    options.headless = True
    service = EdgeService(executable_path="/usr/local/bin/msedgedriver")
    driver = webdriver.Edge(service=service, options=options)
    return driver

def read_urls(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file]
    return urls

def scrape_data(driver, url):
    driver.get(url)
    time.sleep(2)  # Wait for the page to load

    data = {}
    data['Source URL'] = url

    try:
        content = driver.find_element(By.TAG_NAME, 'body').text
        data['Content'] = content.replace("\n", " ")  # Replacing newline with space
    except Exception as e:
        data['Content'] = ''
        print(f"Error extracting content: {e}")

    return data

def write_to_csv(data, output_file):
    file_exists = os.path.isfile(output_file)
    with open(output_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Source URL', 'Content'], delimiter=';')
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def main():
    urls_file = '/Users/kenilim/geek/sgsupportgowhere_scrape/supportgowhere_sg/all_urls.txt'
    output_file = '/Users/kenilim/geek/sgsupportgowhere_scrape/supportgowhere_sg/scraped_data.csv'
    
    urls = read_urls(urls_file)
    driver = init_driver()
    
    # Ensure the CSV file is created first
    if not os.path.exists(output_file):
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Source URL', 'Content'], delimiter=';')
            writer.writeheader()

    for url in urls:
        data = scrape_data(driver, url)
        write_to_csv(data, output_file)
        print(f"Data written to CSV for URL: {url}")

    driver.quit()

if __name__ == "__main__":
    main()
