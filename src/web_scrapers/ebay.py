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

def get_price(products):
    for product in products:
        product_price.append(
            str(product.get_text()).strip().replace(',', '')[4:-3])


def get_name_and_image(soup, max_product_count):
    products = soup.find_all(
        'img', class_='s-item__image-img', limit=max_product_count)
    for product in products:
        # product name
        product_names.append(product['alt'])
        # product image
        product_images.append(product['src'])


def get_link(soup, max_product_count):
    products = soup.find_all(
        'a', class_='s-item__link', limit=max_product_count)
    for product in products:
        product_link.append(product['href'])


# main function

def get(search_element, max_product_count):

    # request web page and parse it
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=' + search_element
    response = proxy_request(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # get all product details

    products = soup.find_all(
        'span', class_='s-item__price', limit=max_product_count)

    # check for empty response
    if 0 == len(products):
        print('empty result set from ebay.com')
        exit()

    # create threads to search for each attribute in parallel
    price_thread = Thread(target=get_price, args=(products,))
    name_image_thread = Thread(
        target=get_name_and_image, args=(soup, max_product_count,))
    link_thread = Thread(target=get_link, args=(soup, max_product_count,))

    # search items
    price_thread.start()
    name_image_thread.start()
    link_thread.start()

    # wait for the threads to end
    price_thread.join()
    name_image_thread.join()
    link_thread.join()

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
    with open('json/ebay.json', 'w') as file:
        json.dump(product_arr, file)

    print('ebay: done')
