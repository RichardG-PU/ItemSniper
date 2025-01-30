from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
import time
import os

# Setup Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")  # Added for GitHub Actions stability
options.add_argument("--window-size=1920,1080")  # Ensure full page loads
options.add_argument("--remote-debugging-port=9222")  # Helps with debugging
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")

print("Initializing WebDriver...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
postURL = "https://discord.com/api/webhooks/1194124780765458472/5UOtknX2HUmPdZb9ft67rPQU48v3PCTmKR47F0kS1Y5ClzVaXUdos2Z_IrNy-wr1DtSy"
URL = "https://www.amazon.ca/gp/product/B002Q8I7OA?smid=A3DWYIK6Y9EEQB&th=1&psc=1"

print(f"Navigating to URL: {URL}")
driver.get(URL)
time.sleep(5)

# Debug: Capture entire page HTML
page_source = driver.page_source
print("Page source captured. Checking for availability element...")

# Save page source for debugging
with open("debug_page.html", "w", encoding="utf-8") as f:
    f.write(page_source)

# Send page source to Discord for debugging
debug_message = {
    "content": f"Debugging Amazon Page Source: {URL}\nFirst 1000 characters:\n```{page_source[:1000]}```"
}
requests.post(postURL, json=debug_message)

# Find availability text
availability_element = driver.find_elements(By.ID, "availability")
if availability_element:
    availability_text = availability_element[0].text.strip()
    print(f"Found availability: {availability_text}")
else:
    print("Availability element not found!")
    availability_text = "Unknown"

# Send to Discord
postJSON = {
    "content": "",
    "embeds": [
        {
            "title": "Sniped items",
            "description": f"<@356119350677078016>:\nItem 1: {URL}\nAvailability: {availability_text}",
            "color": 16711680,
        }
    ],
}

response = requests.post(postURL, json=postJSON)
print(f"Discord response: {response.status_code}, {response.text}")

# Close driver
driver.quit()