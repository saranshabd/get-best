from bs4 import BeautifulSoup
import requests
import json


# main function

def get(search_element):

    # request web page and parse it
    url = 'https://www.snapdeal.com/search?keyword=' + search_element
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_names = []
    product_images = []
    product_price = []
    product_link = []

    # get all product details
    products = soup.find_all('img', class_='product-image')
    for product in products:
        # product names
        product_names.append(product['title'])
        # product images
        try:
            temp = product['src']
            product_images.append(temp)
        except:
            product_images.append(product['data-src'])

    # product links
    products = soup.find_all('div', class_='product-tuple-image')
    for product in products:
        product_link.append(product.find('a')['href'])

    # product prices
    products = soup.find_all('div', class_='lfloat marR10')
    for product in products:
        product_price.append(product.find('span', class_='lfloat product-price')['display-price'])

    # create array storing dictionaries containing all product details
    product_arr = []
    for i in range(len(product_names)):
        product_arr.append({
            'name': product_names[i],
            'price': product_price[i],
            'image': product_images[i],
            'link': product_link[i]
        })

    # store this object into a local JSON file
    with open('json/snapdeal.json', 'w') as file:
        json.dump(product_arr, file)
