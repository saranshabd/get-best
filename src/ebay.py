from bs4 import BeautifulSoup
import requests
import json


# main function

def get(search_element, max_product_count):

    # request web page and parse it
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=' + search_element
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_names = []
    product_images = []
    product_price = []
    product_link = []

    # get all product details

    products = soup.find_all('span', class_='s-item__price')

    # check for empty response
    if 0 == len(products):
        print('empty result set from ebay.com')
        exit()

    # product price
    count = max_product_count
    for product in products:
        if 0 == count:
            break
        product_price.append(
            str(product.get_text()).strip().replace(',', '')[4:-3])
        count -= 1

    products = soup.find_all('img', class_='s-item__image-img')
    count = max_product_count
    for product in products:
        if 0 == count:
            break
        # product name
        product_names.append(product['alt'])
        # product image
        product_images.append(product['src'])
        count -= 1

    # product link
    products = soup.find_all('a', class_='s-item__link')
    count = max_product_count
    for product in products:
        if 0 == count:
            break
        product_link.append(product['href'])
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
    with open('json/ebay.json', 'w') as file:
        json.dump(product_arr, file)
