import json
import requests

URL = "http://fx-trading-game-leicester-challenge.westeurope.azurecontainer.io:443/"
TRADER_ID = "3ohLR6Pr6n8OKmWXyVbURuoYfKRAce02"

SIDE_BUY = "Buy"
SIDE_SELL = "Sell"

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
        resp_json = json.loads(res.content.decode('utf-8'))
        prices = [get_price_history()]
        for i in range(qty):
            price = resp_json["price"]
            prices.append(price)
        #EMA formula, takes last value minus first value divided by n+1. Add first value.
        #TODO: Make it less sensitive.
        ema = (float(prices[-1]) - float(prices[0]) / (1 + 1)) + float(prices[0])
        return ema
    return None

def getNormalisedCapitals():
    api_url = URL + "/normalizedCapitals"
    res = requests.get(api_url)
    res = json.loads(res.content.decode("utf-8"))
    return res["Team5"]

def trade2(qty, side): ## returns trade execution price
    api_url = URL + "/trade/EURGBP"
    data = {"trader_id": TRADER_ID, "quantity": qty, "side": side}
    res = requests.post(api_url, json=data)
    if res.status_code == 200:
        resp_json = json.loads(res.content.decode('utf-8'))
        price = resp_json["price"]
        
        return price
    print("Failed to execute trade.")
    return None


# Function to calculate RSI (Relative Strength Index)
def calc_rsi(prices, period=14):
    gains = []
    losses = []
    for i in range(1, len(prices)):
        change =  prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
        else:
            losses.append(abs(change))

    averageGain = sum(gains[-period:]) / period 
    averageLoss = sum(losses[-period:]) / period if losses else 0

    if averageLoss == 0:
        return 100 # RSI stays at 100 if there are no losses 

    rs = averageGain / averageLoss
    rsi = 100 - (100 / (1+rs)) 
    return rsi       


if __name__ == '__main__':
    print("Expected to trade at:" + str(get_price()))
    trade_data = trade(TRADER_ID, 100, Side.BUY)
    if trade_data:
        print(f"Effectively traded at: {trade_data['ema']}")
        print(f"RSI: {trade_data['rsi']}")

    print("Expected to trade at:" + str(get_price()))
     print("Effectively traded at:" + str(trade(TRADER_ID, 100, Side.BUY)))

