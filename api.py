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


def gold_today():
    while True:
        response = get_nbp_rates("http://api.nbp.pl/api/cenyzlota/today/")
        print("Dzisiejsza cena złota to:", response[0]["cena"], "\n0 oznacza, że nbp jeszcze nie podał danych.")
        break


def currency_exchange():
    while True:
        response_rates = get_nbp_rates("https://api.nbp.pl/api/exchangerates/tables/A/")
        currencies = get_all_available_currencies(response_rates)

        code = get_code(currencies)
        quantity = get_quantity(code)

        api = f'http://api.nbp.pl/api/exchangerates/rates/a/{code}/'

        api_response = requests.get(api)

        mid = float(extract_mid_json(api_response))
        kantor = mid * quantity
        print(round(kantor, 2))
        if input("Chcesz zamknąć? T/N ").upper() == "T":
            break


def rates_over_time():
    response = get_nbp_rates("https://api.nbp.pl/api/exchangerates/tables/a/")
    currencies = get_all_available_currencies(response)
    print(
        f"Dane dla jakiej waluty (z poniżej wymienionych) chcesz sprawdzić?\n{', '.join(str(elem) for elem in currencies)}")
    code = input("Trzy literowy kod waluty z lity powyżej: ")
    print("Od kiedy?")
    year_start = input("Rok (w formacie RRRR): ")
    month_start = input("Miesiąc (w formacie MM): ")
    day_start = input("Dzień (w formacie DD): ")
    print("Do kiedy?")
    year_end = input("Rok (w formacie RRRR): ")
    month_end = input("Miesiąc (w formacie MM): ")
    day_end = input("Dzień (w formacie DD): ")
    response = get_nbp_rates(
        f"http://api.nbp.pl/api/exchangerates/rates/a/{code}/{year_start}-{month_start}-{day_start}/{year_end}-{month_end}-{day_end}/")
    n = 0
    for elem in response["rates"]:
        print("Data:", response["rates"][n]["effectiveDate"], ":", response["rates"][n]["mid"])
        n = n + 1


while True:
    print("\n>>\tMenu główne\t<<")
    print("0 - Zamknij program")
    print("1 - Przelicznik walutowy")
    print("2 - Dzisiejsza wartość złota")
    print("3 - Wartość waluty w wybranym okresie")
    print("*Wszystkie dane są na podstawie notowań NBP.")
    print(">>\t\t\t\t<<")
    menu_option = input("W czym Ci mogę dzisiaj pomóc?\nWpisz numer z listy powyżej. ")
    if menu_option == "1":
        currency_exchange()
    elif menu_option == "2":
        gold_today()
    elif menu_option == "3":
        rates_over_time()
    elif menu_option == "0":
        break
