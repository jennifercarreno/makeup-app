from itertools import product
import requests, json

x = requests.get('http://makeup-api.herokuapp.com/api/v1/products.json')
products = json.loads(x.text)
for i in range(len(products)):

    print(products[i].get("name"))
