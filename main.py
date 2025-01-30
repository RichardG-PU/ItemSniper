from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

# Setup Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Required for GitHub Actions
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")  # Helps avoid rendering issues
options.add_argument("--window-size=1920,1080")  # Ensure elements load fully
options.add_argument("--remote-debugging-port=9222")  # Debugging

print("Initializing WebDriver...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

postURL = "https://discord.com/api/webhooks/1194124780765458472/5UOtknX2HUmPdZb9ft67rPQU48v3PCTmKR47F0kS1Y5ClzVaXUdos2Z_IrNy-wr1DtSy"
URL = "https://www.amazon.ca/gp/product/B002Q8I7OA?smid=A3DWYIK6Y9EEQB&th=1&psc=1"

print(f"Navigating to URL: {URL}")
driver.get(URL)

# Wait up to 20 seconds for the availability element to appear
try:
    print("Waiting for availability element...")
    availability_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "availability"))
    )
    availability_text = availability_element.text.strip()
    print(f"Found availability: {availability_text}")
except Exception as e:
    print(f"Availability element NOT found. Exception: {e}")
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

driver.quit()