from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
import time
import os

# Setup Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
postURL = "https://discord.com/api/webhooks/1194124780765458472/5UOtknX2HUmPdZb9ft67rPQU48v3PCTmKR47F0kS1Y5ClzVaXUdos2Z_IrNy-wr1DtSy"
URL = "https://www.amazon.ca/gp/product/B002Q8I7OA?smid=A3DWYIK6Y9EEQB&th=1&psc=1"

driver.get(URL)
time.sleep(5)

try:
    availability_text = driver.find_element(By.ID, "availability").text.strip()
except:
    availability_text = "Unknown"

postJSON = {
        "content": "",
        "embeds": [
            {
                "title": "Sniped items",
                "description": "<@356119350677078016>: \n\tItem 1: " + URL + availability_text,
                "color": 16711680,
            }
        ],
    }

response = requests.post(postURL, json=postJSON)
print(f"Discord response: {response.status_code}, {response.text}")
driver.quit()