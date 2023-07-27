from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

print("start...")

url = "https://www.memoryexpress.com/Category/VideoCards?Search=rtx+4070"
html = requests.get(url).text

soup = BeautifulSoup(html, 'lxml')
products = soup.find_all("div",{"class":"c-shca-icon-item" })

productNames = []
productCosts = []
productInventories = []


for product in products:
    productName = product.find("div", {"class": "c-shca-icon-item__body-name"})
    productName = productName.find('a').text
    productName = re.sub('^\s+|\s+$', '', productName)

    productCost = product.find("div", {"class": "c-shca-icon-item__summary-list"}).text
    productCost = re.sub('\s+|\+', '', productCost)

    try:
        productStock = product.find('div', {'class': 'c-shca-icon-item__body-inventory'}).text
        productStock = re.sub('\n+(\s*)', '' , productStock)
    except:
        productStock = "AVAILABLE"

    productNames.append(productName)
    productCosts.append(productCost)
    productInventories.append(productStock)

productTable = {
    "Name": productNames,
    "Price": productCosts,
    "Stock": productInventories
}

df = pd.DataFrame(productTable)

stocks = df["Stock"]
has_stock = df.loc[stocks == "AVAILABLE"]
print(has_stock)

print(df)