import os
from web_scrapers import flipkart, amazon_in, snapdeal, ebay
import time
from threading import Thread

# global contants

max_product_count = 5


# helper functions

def make_searchable(search_element):
    return str(search_element).strip().replace(
        ' ', '+').replace(',', '+').replace('.', '+').replace('/', '+')


# main function

def main():

    # create 'json' folder to store results, if does not exists already
    if False == os.path.isdir('json'):
        os.makedirs('json')

    # get user input to search an item
    search_element = input('enter element to search: ')

    # make searched item into URL string
    search_element = make_searchable(search_element)

    # create threads to search each web page parallely
    flipkart_thread = Thread(target=flipkart.get, args=(
        search_element, max_product_count))
    amazon_in_thread = Thread(target=amazon_in.get, args=(
        search_element, max_product_count))
    snapdeal_thread = Thread(target=snapdeal.get, args=(
        search_element, max_product_count))
    ebay_thread = Thread(target=ebay.get, args=(
        search_element, max_product_count))

    start_time = time.time()

    # search the element
    flipkart_thread.start()
    amazon_in_thread.start()
    snapdeal_thread.start()
    ebay_thread.start()

    # wait for the threads to end
    flipkart_thread.join()
    amazon_in_thread.join()
    snapdeal_thread.join()
    ebay_thread.join()

    end_time = time.time()

    print(str(end_time - start_time) + ' seconds')


if __name__ == "__main__":
    main()
