import requests
from bs4 import BeautifulSoup


def get_exchang():
    exchange_rate = {}
    response = requests.get('https://www.bnm.md/ru')
    soup = BeautifulSoup(response.content, 'html.parser')
    currencies = soup.find_all('span', class_="currency")

    for currency in currencies:
        value = currency.find_next('span').text
        exchange_rate[str.lower(currency.text)] = value

    return exchange_rate
