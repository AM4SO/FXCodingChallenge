import json
import requests

URL = "http://fx-trading-game-leicester-challenge.westeurope.azurecontainer.io:443/"
TRADER_ID = "3ohLR6Pr6n8OKmWXyVbURuoYfKRAce02"


class Side:
    BUY = "buy"
    SELL = "sell"

def get_price():
    api_url = URL + "/price/EURGBP"
    res = requests.get(api_url)
    if res.status_code == 200:
        return json.loads(res.content.decode('utf-8'))["price"]
    return None

def get_price_history():
    api_url = URL + "/priceHistory/EURGBP"
    res = requests.get(api_url)
    if res.status_code == 200:
        trades = json.loads(res.content.decode('utf-8'))
        ret = []
        for k in trades.keys():
            ret.append((k, trades[k]))
        return ret
    print("Failed to get price history.")

def trade(trader_id, qty, side):
    api_url = URL + "/trade/EURGBP"
    data = {"trader_id": trader_id, "quantity": qty, "side": side}
    res = requests.post(api_url, json=data)
    if res.status_code == 200:
        resp_json = json.loads(res.content.decode('utf-8'))
        print(res.content.decode('utf-8'))
        prices = []
        for i in range(qty):
            price = resp_json["price"]
            prices.append(price)
        #EMA formula, takes last value minus first value divided by n+1. Add first value.
        #TODO: Make it less sensitive.
        ema = (float(prices[-1]) - float(prices[0]) / (1 + 1)) + float(prices[0])
        return ema
    return None


def trade2(trader_id, qty, side):
    api_url = URL + "/trade/EURGBP"
    data = {"trader_id": trader_id, "quantity": qty, "side": side}
    res = requests.post(api_url, json=data)
    if res.status_code == 200:
        resp_json = json.loads(res.content.decode('utf-8'))
        print(res.content.decode('utf-8'))

        price = resp_json["price"]
        #EMA formula, takes last value minus first value divided by n+1. Add first value.
        #TODO: Make it less sensitive.
        return price
    return None






if __name__ == '__main__':
    #print("Expected to trade at:" + str(get_price()))
    #print("Effectively traded at:" + str(trade2(TRADER_ID, 1, Side.BUY)))
    print("Getting prices")
    get_price_history()
    print("Got price history")
