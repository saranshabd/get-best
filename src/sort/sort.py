from sort import products, load_products, perform_sort, perform_rev_sort, dump_products, clear_result_file


def price_ascending():
    clear_result_file()
    load_products()
    perform_sort()
    dump_products()


def price_descending():
    clear_result_file()
    load_products()
    perform_rev_sort()
    dump_products()
