import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'http://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics%20card'

# Open Connection
uClient = uReq(my_url)
page_html = uClient.read()

# Close Connection
uClient.close()

# Parse HTML
page_soup = soup(page_html, "html.parser")

# Grab Each Product
containers = page_soup.findAll("div",{"class":"item-container"})
# print(containers[0])

contain_arr = []
for container in containers:
    brand = container.div.div.a.img["title"]
    title_contain = container.findAll("a", {"class":"item-title"})
    product_name = title_contain[0].text
    price_contain = container.findAll("li", {"class":"price-current"})
    price = price_contain[0].text.strip()
    shipping_contain = container.findAll("li", {"class":"price-ship"})
    shipping = shipping_contain[0].text.strip()
    rating_container = container.div.div.findAll("a", {"class":"item-rating"})
    rating = ""
    if (len(rating_container) > 0):
        rating_contain = rating_container[0].findAll("span", {"class":"item-rating-num"})
        rating = rating_contain[0].text.strip()
    contain_arr.append({"brand":brand.replace(",", "|"), "product_name":product_name.replace(",", "|"), "price":price.replace(",", ""), "shipping":shipping.replace(",", ""), "rating":rating.replace(",", "")})

contain_arr = sorted(contain_arr, key = lambda i: i['price'], reverse=True)

filename = "products.csv"
f = open(filename, "w")
headers = "brand, product_name, price, shipping, rating,\n"
f.write(headers)

for container in contain_arr:
    f.write(container["brand"])
    f.write(",")
    f.write(container["product_name"])
    f.write(",")
    f.write(container["price"])
    f.write(",")
    f.write(container["shipping"])
    f.write(",")
    f.write(container["rating"])
    f.write(",\n")
f.close()