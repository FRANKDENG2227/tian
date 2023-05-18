import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def scrape_powerball_data():
    # Make a request to the Powerball historical data page
    url = "https:/pip/www.powerball.com/previous-results?gc=powerball&sd=1992-04-22&ed=2023-05-01"
    
    # Launch a new instance of the Chrome browser
    driver = webdriver.Chrome()

    # Navigate to the Powerball website
    driver.get(url)
    n=0.101
    
    # Find the "load more" button and click it until all results are displayed
    while True:
        try:
            
            # Wait for the "load more" button to become clickable
            load_more_button = WebDriverWait(driver, 10+n).until(
                EC.element_to_be_clickable((By.ID, 'loadMore'))
            )

            # Extract the values of the "data-val" and "data-max" attributes
            val = load_more_button.get_attribute('data-val')
            max = load_more_button.get_attribute('data-max')
            print(val)
            print(max)
            
            # Click the "load more" button
            load_more_button.click()
            
           # Wait for the new results to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a.card'))
            )

            # Wait for 1 second to avoid triggering rate limiting or anti-scraping measures
            time.sleep(5)
        
        except:
            print('error1')
            if(val >= max):
                break
            else:
                print('error')
        # Close the browser window
        driver.quit()

    # Extract the winning numbers and other relevant information
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all the card elements on the page
    cards = soup.select('a.card')

    data = []
    for card in cards:
         #find parent in card
        parent = card.select_one('[class="col d-flex gap-1 gap-lg-2 mx-0 align-items-center w-100 justify-content-center | game-ball-group"]')
        #print(parent)
        print(parent.select_one('div:nth-of-type(1)'))
        
        # Extract relevant information from the card
        result_date = card.select_one('[class="card-title"]').text.strip()
        result_whiteball1 = parent.select_one('div:nth-of-type(1)').text.strip()
        result_whiteball2 = parent.select_one('div:nth-of-type(2)').text.strip()
        result_whiteball3 = parent.select_one('div:nth-of-type(3)').text.strip()
        result_whiteball4 = parent.select_one('div:nth-of-type(4)').text.strip()
        result_whiteball5 = parent.select_one('div:nth-of-type(5)').text.strip()
        print(f"white1:{result_whiteball1}")
        result_powerball=card.select_one('[class="form-control col powerball item-powerball"]').text.strip()
        print(f"date: {result_date}")
   
        # Store the data as a tuple
        data.append((result_date, result_whiteball1, result_whiteball2, result_whiteball3, result_whiteball4, result_whiteball5, result_powerball))

        return data
    

def save_data_to_file(data, filename):
    with open(filename, 'w') as file:
        for entry in data:
            date, white1, white2, white3, white4, white5, powerball = entry
            file.write(f"{date}: whiteball: {white1} {white2} {white3} {white4} {white5}- Powerball: {powerball}\n")

# Scrape the Powerball data
powerball_data = scrape_powerball_data()

# Save the data to a text file
filename = "powerball_data.txt"
save_data_to_file(powerball_data, filename)

print(f"All Powerball data has been scraped and saved to {filename}.")
