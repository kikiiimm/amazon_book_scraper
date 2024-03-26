from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Configure Chrome WebDriver
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the initial page
driver.get('https://www.audible.com/search')

# Click the sort button (assuming it's necessary)
sort_by_button = driver.find_element(By.XPATH, "//select[@name='sort']/option[@value='pubdate-desc-rank']")
sort_by_button.click()

# Lists to store scraped data
title = []
author = []
released_date = []

# Loop through all pages
while True:
    # Find all books on the current page
    books = driver.find_elements(By.XPATH, "//li[contains(@class, 'productListItem')]")

    # Scrape data from each book
    for book in books:
        title.append(book.find_element(By.XPATH, ".//h3[contains(@class, 'bc-heading')]").text)
        author.append(book.find_element(By.XPATH, ".//li[contains(@class, 'authorLabel')]").text)
        released_date.append(book.find_element(By.XPATH, ".//li[contains(@class, 'releaseDateLabel')]").text)

    # Check if there is a next page
    try:
        next_page_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'nextButton')]//a"))
        )
        next_page_link.click()
    except:
        print("No more pages left.")
        break
    

# Create DataFrame and save to CSV
df = pd.DataFrame({'title': title, 'author': author, 'released_date': released_date})
df.to_csv('data2.csv', index=False)

# Close the WebDriver
driver.quit()
