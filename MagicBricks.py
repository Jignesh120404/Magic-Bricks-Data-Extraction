import csv
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

csv_file = 'output_data1 copy.csv'
page_url = "https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=1,2,3&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment&cityName=Mira-Road-and-Beyond-area-Mumbai"

# Function to read existing URLs from CSV
def read_existing_urls(file_name):
    existing_urls = set()
    try:
        with open(file_name, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                existing_urls.add(row['URL'])
    except FileNotFoundError:
        pass
    return existing_urls

# Open the CSV file for writing
with open(csv_file, 'a', newline='', encoding='utf-8') as output_csv:
    fieldnames = ['URL']
    writer = csv.DictWriter(output_csv, fieldnames=fieldnames)

    # Start WebDriver
    driver = webdriver.Chrome()
    driver.get(page_url)

    # Define functions
    def scroll_down():
        for _ in range(20):
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(1)

    def wait_until_loaded():
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "script")))
        time.sleep(2)

    # Initial scroll
    scroll_down()

    counter = 0
    batch_size = 25
    scraped_urls = set()
    existing_urls = read_existing_urls(csv_file)

    while True:
        wait_until_loaded()
        script_elements = driver.find_elements(By.TAG_NAME, "script")
        for script in script_elements:
            script_content = script.get_attribute('innerHTML')
            if script_content.startswith('{') and script_content.endswith('}'):
                try:
                    json_data = json.loads(script_content)
                    if 'url' in json_data:
                        url = json_data['url']
                        if url in existing_urls:
                            count=0
                            print(f"Already present{count}.")
                            count+=1
                        elif url not in scraped_urls:
                            counter += 1
                            print(f"URL {counter}: {url}")
                            writer.writerow({'URL': url})
                            scraped_urls.add(url)

                            if counter % batch_size == 0:
                                scroll_down()
                except json.JSONDecodeError:
                    pass

    print("Done With all Done for Mumbai")
    driver.quit()
