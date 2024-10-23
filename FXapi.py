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


def trade(trader_id, qty, side):
    api_url = URL + "/trade/EURGBP"
    data = {"trader_id": trader_id, "quantity": qty, "side": side}
    res = requests.post(api_url, json=data)
    if res.status_code == 200:
        resp_json = json.loads(res.content.decode('utf-8'))
        trading_algorithm(qty, resp_json, trader_id)

def trading_algorithm(qty, resp_json, trader_id):
    prices = [resp_json["price"]]
    ema = prices[0]
    ema_period = 2
    alpha = 2/(ema_period+1)
    for i in range(1, qty):
        #TODO: Get new prices instead of constantly grabbing same ones
        current_price = resp_json["price"]
        prices.append(current_price)
        ema = float(ema) + alpha * (float(current_price)-float(ema))

        #Buy when low
        if float(current_price) > float(ema):
            print(f"Buying at {current_price}")
            trade(trader_id, i, Side.BUY)

        #Sell when high
        elif float(current_price) < float(ema):
            print(f"Selling at {current_price}")
            trade(trader_id, i, Side.SELL)


if __name__ == '__main__':
    print("Expected to trade at:" + str(get_price()))
    print("Effectively traded at:" + str(trade(TRADER_ID, 100, Side.BUY)))
