from bs4 import BeautifulSoup
import requests
import json
import re
from proxy import proxy_request
from threading import Thread


# global variables

product_images = []
product_name = []
product_price = []
product_link = []


# helper functions

def extract_num(price):
    return max(map(int, re.findall(r'\d+', price)))


# threading functions

def get_names(products):
    for product in products:
        product_name.append(product.find('img')['alt'])


def get_image(products):
    for product in products:
        product_images.append(product.find('img')['src'])


def get_price(products):
    for product in products:
        product_price.append(extract_num(
            product.find('div', class_='_1vC4OE').get_text()))


def get_link(products):
    for product in products:
        product_link.append('https://www.flipkart.com' +
                            product.find('a')['href'])


# main function

def get(search_element, max_product_count):

    # request web page and parse it
    url = 'https://www.flipkart.com/search?q=' + search_element
    response = proxy_request(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # get all product details

    products = soup.find_all(
        'div', class_='_3liAhj _1R0K0g', limit=max_product_count)

    # check for empty response
    if 0 == len(products):
        print('empty result set from flipkart.com')
        with open('json/flipkart.json', 'w') as file:
            json.dump([], file)
        exit()

    # create threads to search for each attribute in parallel
    image_thread = Thread(target=get_image, args=(products,))
    name_thread = Thread(target=get_names, args=(products,))
    price_thread = Thread(target=get_price, args=(products,))
    link_thread = Thread(target=get_link, args=(products,))

    # search items
    image_thread.start()
    name_thread.start()
    price_thread.start()
    link_thread.start()

    # wait for the threads to end
    image_thread.join()
    name_thread.join()
    price_thread.join()
    link_thread.join()

    # create array storing dictionaries containing all product details
    product_arr = []
    for i in range(len(product_name)):
        product_arr.append({
            'name': product_name[i],
            'price': product_price[i],
            'image': product_images[i],
            'link': product_link[i]
        })

    # store this object into a local JSON file
    with open('json/flipkart.json', 'w') as file:
        json.dump(product_arr, file)

    print('flipkart: done')
