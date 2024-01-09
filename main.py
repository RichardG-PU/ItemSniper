import requests
from bs4 import BeautifulSoup

URL = "https://fearofgod.com/collections/athletics-mens/products/heavy-fleece-hoodie"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="add")

postURL = "https://discord.com/api/webhooks/1194124780765458472/5UOtknX2HUmPdZb9ft67rPQU48v3PCTmKR47F0kS1Y5ClzVaXUdos2Z_IrNy-wr1DtSy"

if results.text == "Sold Out":
    postJSON = {
        "content": "",
        "embeds": [
            {
                "title": "Sniped items",
                "description": "Item 1 : https://fearofgod.com/collections/athletics-mens/products/heavy-fleece-hoodie \nCurrently sold out",
                "color": 5814783,
            }
        ],
    }
    requests.post(postURL, json=postJSON)
else:
    postJSON = {
        "content": "",
        "embeds": [
            {
                "title": "Sniped items",
                "description": "<@326065487395946506> : \n\tItem 1 : https://fearofgod.com/collections/athletics-mens/products/heavy-fleece-hoodie \nCurrently sold out",
                "color": 5814783,
            }
        ],
    }
