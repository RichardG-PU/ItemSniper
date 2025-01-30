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
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

print("Initializing WebDriver...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

postURL = "https://discord.com/api/webhooks/1194124780765458472/5UOtknX2HUmPdZb9ft67rPQU48v3PCTmKR47F0kS1Y5ClzVaXUdos2Z_IrNy-wr1DtSy"
URL = "https://www.amazon.ca/gp/product/B002Q8I7OA?smid=A3DWYIK6Y9EEQB&th=1&psc=1"

print(f"Navigating to URL: {URL}")
driver.get(URL)
time.sleep(5)

# Scroll down to trigger lazy loading
print("Scrolling down to force rendering...")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

# Check if element is inside an iframe
print("Checking for iframes...")
iframes = driver.find_elements(By.TAG_NAME, "iframe")
print(f"Found {len(iframes)} iframes.")

for iframe in iframes:
    driver.switch_to.frame(iframe)
    try:
        print("Looking for availability in iframe...")
        availability_element = driver.find_element(By.ID, "availability")
        print("Found availability inside an iframe!")
        break
    except:
        driver.switch_to.default_content()

# Wait until the availability element is visible
print("Waiting for availability to be visible...")
availability_element = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.ID, "availability"))
)
availability_text = availability_element.text.strip()
print(f"Availability found: {availability_text}")

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

if availability_text != "Unknown":
    response = requests.post(postURL, json=postJSON)
    print(f"Discord response: {response.status_code}, {response.text}")

driver.quit()