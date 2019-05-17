from bs4 import BeautifulSoup
import requests
from random import choice


# function to get a proxy IP address and port number
def get_proxy():

    # make request to web page and parse it
    url = 'https://www.sslproxies.org/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # scrap the table and get random proxy ip address and port number
    return {
        'https': choice(list(map(lambda x: x[0] + ':' + x[1], list(zip(map(lambda x: x.get_text(), soup.find_all('td')[::8]), map(
            lambda x: x.get_text(), soup.find_all('td')[1::8]))))))
    }


# function to make a proxy request
def proxy_request(url):
    while True:
        try:
            proxy = get_proxy()
            print('get proxy')
            response = requests.get(url, proxies=proxy, timeout=5)
            print('confirm proxy: ' + str(proxy['https']))
            break
        except:
            pass
    return response
