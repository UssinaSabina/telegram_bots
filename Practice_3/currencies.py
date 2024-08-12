import requests
import decimal

ERROR_FETCHING_VALUE = -1
ERROR_CURRENCY_FROM_NOT_FOUND = -2
ERROR_CURRENCY_TO_NOT_FOUND = -3

API_EXCHANGE_BASE_URL = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{currency}.json"
CURRENCIES_API_URL = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json"


def get_currency_ratio(from_currency: str, to_currency: str):
    from_currency = from_currency.lower()
    to_currency = to_currency.lower()

    url = API_EXCHANGE_BASE_URL.format(currency=from_currency)

    response = requests.get(url)

    if response.status_code != 200:
        if response.status_code == 404:
            return ERROR_CURRENCY_FROM_NOT_FOUND
        return ERROR_FETCHING_VALUE

    json_data = response.json(parse_float=decimal.Decimal)
    values = json_data[from_currency]

    if to_currency not in values:
        return ERROR_CURRENCY_TO_NOT_FOUND

    return values[to_currency]


def get_rub_to_kzt_ratio():
    return get_currency_ratio(
        from_currency="rub",
        to_currency="kzt"
    )


def check_if_currency_exists(currency: str) -> bool:
    response = requests.get(CURRENCIES_API_URL)
    json_data = response.json()
    return currency in json_data
