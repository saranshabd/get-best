from bs4 import BeautifulSoup
import requests
import re
import json
from proxy import proxy_request
from threading import Thread


# global variables

product_names = []
product_images = []
product_prices = []
product_links = []


# threading functions

def get_name_and_link(soup, max_product_count):
    products = soup.find_all(
        "div", class_='a-row a-spacing-small', limit=max_product_count)
    for product in products:
        # product names
        product_names.append(str(product.find('h2').get_text()).strip())
        # product links
        product_links.append(product.find('a')['href'])


def get_image(soup, max_product_count):
    products = soup.find_all(
        'div', class_='a-column a-span12 a-text-center', limit=max_product_count)
    for product in products:
        product_images.append(product.find('img')['src'])


def get_price(soup, max_product_count):
    products = soup.find_all(
        'div', class_='a-column a-span7', limit=max_product_count)
    for product in products:
        temp_result = product.find(
            'span', class_='a-size-base a-color-price s-price a-text-bold')
        product_prices.append(extract_num(temp_result.get_text()))

# helper functions


def extract_num(price):
    return max(map(int, re.findall(r'\d+', price)))


# main function

def get(search_element, max_product_count):

    # request for webpage and parse it
    url = 'https://www.amazon.in/s?k=' + search_element
    response = proxy_request(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    with open('web/amazon-temp.html', 'w') as file:
        file.write(soup.prettify())

    # check for empty result set
    products = soup.find_all('li', class_='s-result-item celwidget', limit=1)
    if 0 == len(products):
        print('empty result set from amazon.in')
        with open('json/amazon_in.json', 'w') as file:
            json.dump([], file)
        exit()

    # create threads to search for each attribute in parallel
    name_link_thread = Thread(target=get_name_and_link,
                              args=(soup, max_product_count,))
    image_thread = Thread(target=get_image, args=(soup, max_product_count,))
    price_thread = Thread(target=get_price, args=(soup, max_product_count,))

    # search items
    name_link_thread.start()
    image_thread.start()
    price_thread.start()

    # wait for the threads to end
    name_link_thread.join()
    image_thread.join()
    price_thread.join()

    # create array storing dictionaries containing all product details
    product_arr = []
    for i in range(len(product_names)):
        product_arr.append({
            'name': product_names[i],
            'price': product_prices[i],
            'image': product_images[i],
            'link': product_links[i]
        })

    # storing this object into a JSON file
    with open('json/amazon_in.json', 'w') as file:
        json.dump(product_arr, file)

    print('amazon: done')
