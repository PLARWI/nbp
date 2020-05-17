import requests


def get_nbp_rates(endpoint):
    response = requests.get(endpoint)
    return response.json()


def get_all_available_currencies(response):
    currencies = []
    rates_list = response[0]["rates"]
    for rate in rates_list:
        currencies.append(rate["code"])
    return currencies


def extract_mid_json(response):
    return response.json()["rates"][-1]["mid"]


def get_code(currencies):
    while True:
        code = input(f"Chcesz wymienić {', '.join(currencies)}? ").upper()
        if code in currencies:
            return code
        else:
            print("Wprowadź właściwe dane.")


def get_quantity(code):
    while True:
        quantity = input(f"Ile {code} chcesz wymienić? ")
        try:
            return float(quantity)
        except:
            print("Niewłaściwa ilość.")


while True:
    response = get_nbp_rates("https://api.nbp.pl/api/exchangerates/tables/A/")
    currencies = get_all_available_currencies(response)

    code = get_code(currencies)
    quantity = get_quantity(code)

    api = f'http://api.nbp.pl/api/exchangerates/rates/a/{code}/'

    api_response = requests.get(api)

    mid = float(extract_mid_json(api_response))
    kantor = mid * quantity
    print(round(kantor, 2))
    if input("Chcesz zamknąć? T/N ").upper() == "T":
        break