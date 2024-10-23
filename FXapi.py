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

## returns [(time, price), (time, price)]
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
        trading_algorithm(qty, trader_id, side)

def trading_algorithm(qty, trader_id, side):
    prices = [get_price_history()]
    ema = None
    ema_period = 2
    alpha = 2/(ema_period+1)
    for i in range(qty):
        api_url = URL + "/price/EURGBP"
        data = {"trader_id": trader_id, "quantity": qty, "side": side}
        res = requests.get(api_url, json=data)
        if res.status_code == 200:
            json_res = json.loads(res.content.decode('utf-8'))
            current_price = float(json_res["price"])
            prices.append(current_price)
            # Initialize EMA with the first price
            if ema is None:
                ema = current_price
            else:
                # Calculate EMA
                ema = ema + alpha * (current_price - ema)

            if current_price < ema:
                print(f"Buying at {current_price}")
                trade(trader_id, 1, Side.BUY)
            elif current_price > ema:
                print(f"Selling at {current_price}")
                trade(trader_id, 1, Side.SELL)





if __name__ == '__main__':
    print("Expected to trade at:" + str(get_price()))
    print("Effectively traded at:" + str(trade(TRADER_ID, 100, Side.BUY)))
