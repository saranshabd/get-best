from bs4 import BeautifulSoup
import requests
import re
import json


# helper functions

def extract_num(price):
    return max(map(int, re.findall(r'\d+', price)))


# main function

def get(search_element):

    # request for webpage and parse it
    url = 'https://www.amazon.in/s?k=' + search_element
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # check for empty result set
    products = soup.find_all('li', class_='s-result-item celwidget')
    if 0 == len(products):
        print('empty result set from amazon.in')
        exit()

    # lists to fill at the end of all queries
    product_names = []
    product_images = []
    product_prices = []
    product_links = []

    # get all products and their details

    products = soup.find_all("div", class_='a-row a-spacing-small')
    for product in products:
        # product names
        product_names.append(str(product.find('h2').get_text()).strip())
        # product links
        product_links.append(product.find('a')['href'])

    # product images
    products = soup.find_all('div', class_='a-column a-span12 a-text-center')
    for product in products:
        product_images.append(product.find('img')['src'])

    # product prices
    products = soup.find_all('div', class_='a-column a-span7')
    for product in products:
        temp_result = product.find(
            'span', class_='a-size-base a-color-price s-price a-text-bold')
        product_prices.append(extract_num(temp_result.get_text()))

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
