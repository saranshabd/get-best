import flipkart
import amazon_in
import snapdeal
import os


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
    flipkart.get(search_element)
    amazon_in.get(search_element)
    snapdeal.get(search_element)


if __name__ == "__main__":
    main()
