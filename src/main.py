import os
import flipkart
import amazon_in
import snapdeal
import ebay

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

    # search the element
    flipkart.get(search_element, max_product_count)
    amazon_in.get(search_element, max_product_count)
    snapdeal.get(search_element, max_product_count)
    ebay.get(search_element, max_product_count)


if __name__ == "__main__":
    main()
