from bs4 import BeautifulSoup
import requests
import json
import re


# helper functions

def extract_num(price):
    return max(map(int, re.findall(r'\d+', price)))


# main function

def get(search_element):

    # request web page and parse it
    url = 'https://www.flipkart.com/search?q=' + search_element
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_images = []
    product_name = []
    product_price = []
    product_link = []

    # get all product details
    products = soup.find_all('div', class_='_3liAhj _1R0K0g')

    # check for empty response
    if 0 == len(products):
        print('empty result set from flipkart')
        exit()

    for product in products:
        # product image
        product_images.append(product.find('img')['src'])
        # product name
        product_name.append(product.find('img')['alt'])
        # product price
        product_price.append(extract_num(
            product.find('div', class_='_1vC4OE').get_text()))
        # product link
        link = product.find('a')
        product_link.append('https://www.flipkart.com' + link['href'])

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
