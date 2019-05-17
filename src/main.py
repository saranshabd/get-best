import flipkart
import amazon_in
import os


# helper functions

def make_searchable(search_element):
    return str(search_element).strip().replace(
        ' ', '+').replace(',', '+').replace('.', '+').replace('/', '+')


# main function

def main():

    # create 'json' folder to store results
    os.makedirs('json')

    # get user input to search an item
    search_element = input('enter element to search: ')

    # make searched item into URL string
    search_element = make_searchable(search_element)

    # search the element
    flipkart.get(search_element)
    amazon_in.get(search_element)


if __name__ == "__main__":
    main()
