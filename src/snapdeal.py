from bs4 import BeautifulSoup
import requests
import json


# main function

def get(search_element, max_product_count):

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

    # check for empty result set
    if 0 == len(products):
        print('empty result set from snapdeal.com')
        exit()

    count = max_product_count
    for product in products:
        if 0 == count:
            break
        # product names
        product_names.append(product['title'])
        # product images
        try:
            temp = product['src']
            product_images.append(temp)
        except:
            product_images.append(product['data-src'])
        count -= 1

    # product links
    products = soup.find_all('div', class_='product-tuple-image')
    count = max_product_count
    for product in products:
        if 0 == count:
            break
        product_link.append(product.find('a')['href'])
        count -= 1

    # product prices
    products = soup.find_all('div', class_='lfloat marR10')
    count = max_product_count
    for product in products:
        if 0 == count:
            break
        product_price.append(product.find(
            'span', class_='lfloat product-price')['display-price'])
        count -= 1

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
