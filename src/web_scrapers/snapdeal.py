from bs4 import BeautifulSoup
import requests
import json
from proxy import proxy_request
from threading import Thread


# global variables

product_names = []
product_images = []
product_price = []
product_link = []


# threading functions

def get_name_and_image(products):
    for product in products:
        # product names
        product_names.append(product['title'])
        # product images
        try:
            temp = product['src']
            product_images.append(temp)
        except:
            product_images.append(product['data-src'])


def get_link(soup, max_product_count):
    products = soup.find_all(
        'div', class_='product-tuple-image', limit=max_product_count)
    for product in products:
        product_link.append(product.find('a')['href'])


def get_price(soup, max_product_count):
    products = soup.find_all(
        'div', class_='lfloat marR10', limit=max_product_count)
    for product in products:
        product_price.append(product.find(
            'span', class_='lfloat product-price')['display-price'])


# main function

def get(search_element, max_product_count):

    # request web page and parse it
    url = 'https://www.snapdeal.com/search?keyword=' + search_element
    response = proxy_request(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # get all product details
    products = soup.find_all(
        'img', class_='product-image', limit=max_product_count)

    # check for empty result set
    if 0 == len(products):
        print('empty result set from snapdeal.com')
        exit()

    # create threads to search for each attribute in parallel
    name_image_thread = Thread(target=get_name_and_image, args=(products,))
    link_thread = Thread(target=get_link, args=(soup, max_product_count,))
    price_thread = Thread(target=get_price, args=(soup, max_product_count,))

    # search items
    name_image_thread.start()
    link_thread.start()
    price_thread.start()

    # wait for the threads to end
    name_image_thread.join()
    link_thread.join()
    price_thread.join()

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

    print('snapdeal: done')
