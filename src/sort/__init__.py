import json

# global variables

products = []


# helper functions

# loads all products into 'products' objects
def load_products():
    # amazon
    try:
        with open('json/amazon_in.json', 'r') as file:
            amazon_products = json.load(file)
            for product in amazon_products:
                products.append(product)
    except FileNotFoundError:
        pass

    # flipkart
    try:
        with open('json/flipkart.json', 'r') as file:
            flipkart_products = json.load(file)
            for product in flipkart_products:
                products.append(product)
    except FileNotFoundError:
        pass

    # snapdeal
    try:
        with open('json/snapdeal.json', 'r') as file:
            snapdeal_products = json.load(file)
            for product in snapdeal_products:
                products.append(product)
    except FileNotFoundError:
        pass


# dumps all products from 'products' into a local file
def dump_products():
    if 0 == len(products):
        return

    with open('json/result.json', 'w') as file:
        json.dump(products, file)


def clear_result_file():
    try:
        with open('json/result.json', 'w') as file:
            json.dump([], file)
    except FileNotFoundError:
        pass


# sorts all products in ascending order on the basis of their prices
def perform_sort():
    products.sort(key=lambda x: x['price'])


# sorts all products in descending order on the basis of their prices
def perform_rev_sort():
    products.sort(key=lambda x: x['price'])
    products.reverse()
