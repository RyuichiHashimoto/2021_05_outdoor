import requests
import warnings
warnings.simplefilter('ignore')

items = {
    "Balance":1000000,
    "Noodles":2,
    "Soup":2,
    "Wallet":"XRCIjmzd7Tvvn-WPe9iZP41HQeKIPzndcua3P70I"
}

r = requests.post("https://cant-use-db.quals.beginners.seccon.jp/",params=items,verify=False)

print(r.text)