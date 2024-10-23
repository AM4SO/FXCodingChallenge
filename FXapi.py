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
    prices = []
    ema = None
    ema_period = 2
    alpha = 2 / (ema_period + 1)

    # Get initial price history
    price_history = get_price_history()
    if price_history is None:
        print("Failed to retrieve price history.")
        return None

    # Extract prices from the price history
    for _, price in price_history:
        prices.append(float(price))

    # Start trading loop
    for _ in range(qty):
        current_price = get_price()

        if current_price is None:
            print("Failed to retrieve current price.")
            continue

        # Append current price to list
        prices.append(float(current_price))

        # Initialize EMA with the first price
        if ema is None:
            ema = current_price
        else:
            # Calculate EMA
            ema = ema + alpha * (current_price - ema)

        # Make a trade decision based on EMA
        if current_price < ema:
            print(f"Buying at {current_price}")
            trade2(trader_id, 1, Side.BUY)
        elif current_price > ema:
            print(f"Selling at {current_price}")
            trade2(trader_id, 1, Side.SELL)

    # Calculate RSI if needed
    rsi = calc_rsi(prices)

    # Return trade data
    return {"ema": ema, "rsi": rsi}

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

