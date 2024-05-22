from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

def setup_driver():
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Edge(options=options)
    return driver

def get_all_links(driver, url):
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    
    # Extracting links from Schemes tab
    schemes_cards = driver.find_elements(By.XPATH, "//a[contains(@href, '/schemes/')]")
    schemes_links = [card.get_attribute('href') for card in schemes_cards]
    
    # Click on the Services tab using JavaScript to avoid ElementClickInterceptedException
    services_tab = driver.find_element(By.XPATH, "//span[contains(text(), 'Services')]/parent::button")
    driver.execute_script("arguments[0].click();", services_tab)
    time.sleep(5)  # Wait for the page to load

    services_cards = driver.find_elements(By.XPATH, "//a[contains(@href, '/schemes/')]")
    services_links = [card.get_attribute('href') for card in services_cards]

    return schemes_links + services_links

def save_links_to_file(links, filename='all_urls.txt'):
    try:
        with open(filename, mode='w', encoding='utf-8') as file:
            for link in links:
                file.write(f"{link}\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

def main():
    driver = setup_driver()
    url = 'https://supportgowhere.life.gov.sg/schemes?activeTab=schemes'
    
    all_links = get_all_links(driver, url)
    print(f"Found {len(all_links)} scheme and service links")

    save_links_to_file(all_links)
    
    driver.quit()

if __name__ == "__main__":
    main()
