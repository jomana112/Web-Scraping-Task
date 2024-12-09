import requests
import csv
import json
from bs4 import BeautifulSoup

url = "https://www.baraasallout.com/test.html"
response = requests.get(url)

if response.status_code != 200:
    print(f"Error: Unable to load the page (Status code: {response.status_code})")
    exit()

page = BeautifulSoup(response.text, "html.parser")

headers = page.find_all(["h1", "h2"])
header_text = [header.get_text(strip=True) for header in headers]

paragraph = page.find("p")
if paragraph:
    paragraph_text = paragraph.get_text(strip=True)
else:
    paragraph_text = "N/A"

lists = page.find_all("li")
list_text = [item.get_text(strip=True) for item in lists]

with open("Extract_Text_Data.CSV", mode="w", newline="", encoding="UTF-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Header", "Paragraph", "List Items"])
    writer.writerow([", ".join(header_text), paragraph_text, ", ".join(list_text)])

table = page.find("table")
if table:
    rows = table.find_all("tr")
    with open("Extract_Table_Data.CSV", mode="w", newline="", encoding="UTF-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Product Name", "Price", "Stock Status"])
        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 0:
                product_name = cols[0].text.strip()
                price = cols[1].text.strip()
                stock_status = cols[2].text.strip()
                writer.writerow([product_name, price, stock_status])

product_cards = page.find_all("div", class_="product-card")
products_data = []

for card in product_cards:
    product_name_element = card.find("span", class_="name")
    if product_name_element:
        product_name = product_name_element.get_text(strip=True)
    else:
        product_name = "N/A"

    price_element = card.find("span", class_="price")
    if price_element:
        price = price_element.get_text(strip=True)
    else:
        price = "N/A"

    stock_element = card.find("span", class_="stock")
    if stock_element:
        stock = stock_element.get_text(strip=True)
    else:
        stock = "N/A"

    add_to_basket_element = card.find("button", class_="add-to-basket")
    if add_to_basket_element:
        add_to_basket = add_to_basket_element.get_text(strip=True)
    else:
        add_to_basket = "N/A"

    products_data.append({
        "name": product_name,
        "price": price,
        "stock": stock,
        "add_to_basket": add_to_basket
    })

with open("Product_Information.json", "w", encoding="UTF-8") as json_file:
    json.dump(products_data, json_file, indent=4, ensure_ascii=False)

form = page.find("form")
if form:
    input_fields = form.find_all("input")
else:
    input_fields = []

form_data = []
for field in input_fields:
    field_name = field.get("name")
    if not field_name:
        field_name = "N/A"

    field_type = field.get("type")
    if not field_type:
        field_type = "N/A"

    default_value = field.get("value")
    if not default_value:
        default_value = "N/A"

    form_data.append({
        "field_name": field_name,
        "field_type": field_type,
        "default_value": default_value
    })

with open("Form_Details.json", "w", encoding="UTF-8") as json_file:
    json.dump(form_data, json_file, indent=4, ensure_ascii=False)

links = page.find_all("a")
links_data = []

for link in links:
    text = link.get_text(strip=True)
    href = link.get("href")
    links_data.append({"text": text, "href": href})

with open("Links_Data.json", "w", encoding="UTF-8") as json_file:
    json.dump(links_data, json_file, indent=4, ensure_ascii=False)

iframe = page.find("iframe")
if iframe:
    video_link = iframe.get("src")
else:
    video_link = "N/A"

multimedia_data = {"video_link": video_link}

with open("Multimedia_Data.json", "w", encoding="UTF-8") as json_file:
    json.dump(multimedia_data, json_file, indent=4, ensure_ascii=False)

featured_products = page.find_all("div", class_="featured-product")
featured_data = []

for product in featured_products:
    product_name_element = product.find("span", class_="name")
    if product_name_element:
        product_name = product_name_element.get_text(strip=True)

    hidden_price_element = product.find("span", class_="price", style="display: none;")
    if hidden_price_element:
        hidden_price = hidden_price_element.get_text(strip=True)

    colors_element = product.find("span", class_="colors")
    if colors_element:
        colors = colors_element.get_text(strip=True)

    product_id = product.get("data-id")

    featured_data.append({
        "id": product_id,
        "name": product_name,
        "price": hidden_price,
        "colors": colors
    })

with open("Featured_Products.json", "w", encoding="UTF-8") as json_file:
    json.dump(featured_data, json_file, indent=4, ensure_ascii=False)






