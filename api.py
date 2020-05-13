import requests

code = input("Chcesz wymienić EUR, GBP czy USD? ")
quantity = input(f"Ile {code} chcesz wymienić? ")
api = f'http://api.nbp.pl/api/exchangerates/rates/a/{code}/'

print(api)
mid = 0

r = requests.get(api)
request_text = r.text
dot = request_text.find(".")

if request_text.endswith("}]}"):
    mid = request_text[dot - 1:dot + 5]

quantity = float(quantity)
mid = float(mid)
kantor = mid * quantity
print(round(kantor, 2))