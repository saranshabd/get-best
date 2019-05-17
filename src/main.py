import os
from web_scrapers import flipkart, amazon_in, snapdeal
import time
from threading import Thread
from sort import sort

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
    try:
        order_choice = int(
            input('1. price: low to high\n2. price: high to low\n-> ')
        )
    except ValueError:
        print('enter a number next time')
        exit()

    # make searched item into URL string
    search_element = make_searchable(search_element)

    # create threads to search each web page parallely
    flipkart_thread = Thread(target=flipkart.get, args=(
        search_element, max_product_count))
    amazon_in_thread = Thread(target=amazon_in.get, args=(
        search_element, max_product_count))
    snapdeal_thread = Thread(target=snapdeal.get, args=(
        search_element, max_product_count))

    start_time = time.time()

    # search the element
    flipkart_thread.start()
    amazon_in_thread.start()
    snapdeal_thread.start()

    # wait for the threads to end
    flipkart_thread.join()
    amazon_in_thread.join()
    snapdeal_thread.join()

    end_time = time.time()

    print(str(end_time - start_time) + ' seconds')

    if 1 == order_choice:
        sort.price_ascending()
    elif 2 == order_choice:
        sort.price_descending()
    else:
        print('choose wisely next time.')


if __name__ == "__main__":
    main()
