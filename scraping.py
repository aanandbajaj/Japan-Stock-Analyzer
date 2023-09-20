import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select  # Import Select class
from bs4 import BeautifulSoup
import time

# URL of the page
url = "https://www2.jpx.co.jp/tseHpFront/JJK020030Action.do"

# Path to your Chrome WebDriver executable
chrome_driver_path = r"C:\Users\aanan\chromedriver.exe"

# Create a Chrome webdriver instance with the executable path specified
driver = webdriver.Chrome()

# Open the URL
driver.get(url)

# Find and interact with checkboxes by their values
checkbox_values = ["011", "012", "013", "008"]
for value in checkbox_values:
    checkbox = driver.find_element(By.XPATH, f"//input[@type='checkbox'][@value='{value}']")
    if not checkbox.is_selected():
        checkbox.click()

# Select an option from the dropdown
display_dropdown = Select(driver.find_element(By.NAME, "dspSsuPd"))
display_dropdown.select_by_value("200")  # Replace with desired option value

# Find and click the search button
search_button = driver.find_element(By.NAME, "searchButton")
search_button.click()

# Give the page some time to load the results
time.sleep(5)  # Adjust as needed

# Specify the complete path to the folder where you want to save the CSV file
output_folder = r"C:\Users\aanan\Documents\Projects\Japanese-Valueline"

# Initialize the CSV file
csv_filename = os.path.join(output_folder, "scraped_data.csv")
csv_headers = ["Column1", "Column2", "Column3", "Column4", "Column5", "Column6", "Column7", "Column8"]  # Replace with actual column names

with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(csv_headers)

    while True:
        # Get the page source using Selenium
        page_source = driver.page_source

        # Use Beautiful Soup to parse the page source
        soup = BeautifulSoup(page_source, "html.parser")

        # Find and extract the table rows
        table_rows = soup.select("table tr")

        # Extract data from each row
        for row in table_rows:
            columns = row.find_all("td")
            data = [column.get_text(strip=True) for column in columns]
            csv_writer.writerow(data)

        # Find the "Next" button element
        next_button = driver.find_element(By.XPATH, "//div[@class='next_e']/a")
        if next_button.get_attribute("href") != "javascript:void(0);":
            next_button.click()
            # Give the page some time to load the next set of results
            time.sleep(5)  # Adjust as needed
        else:
            break

print("Scraping complete.")

# Close the Selenium-controlled browser
driver.quit()
