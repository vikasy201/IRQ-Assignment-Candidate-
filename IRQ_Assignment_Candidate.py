import time
import math
from datetime import datetime, timedelta


class Stock:
    def __init__(self, symbol, stock_type, last_dividend, fixed_dividend, par_value):
        self.symbol = symbol
        self.stock_type = stock_type
        self.last_dividend = last_dividend
        self.fixed_dividend = fixed_dividend
        self.par_value = par_value
        self.trades = []

    def dividend_yield(self, price):
        if self.stock_type == "Common":
            return self.last_dividend / price
        elif self.stock_type == "Preferred":
            return (self.fixed_dividend * self.par_value) / price

    def pe_ratio(self, price):
        dividend = self.dividend_yield(price) * price
        if dividend == 0:
            return float('inf')
        return price / dividend

    def record_trade(self, quantity, buy_sell_indicator, price):
        trade = {
            'timestamp': datetime.now(),
            'quantity': quantity,
            'buy_sell_indicator': buy_sell_indicator,
            'price': price
        }
        self.trades.append(trade)

    def volume_weighted_stock_price(self):
        cutoff_time = datetime.now() - timedelta(minutes=10)
        recent_trades = [trade for trade in self.trades if trade['timestamp'] >= cutoff_time]

        total_quantity = sum(trade['quantity'] for trade in recent_trades)
        total_trade_price_quantity = sum(trade['price'] * trade['quantity'] for trade in recent_trades)

        if total_quantity == 0:
            return 0

        return total_trade_price_quantity / total_quantity


class Market:
    def __init__(self):
        self.stocks = {}

    def add_stock(self, stock):
        self.stocks[stock.symbol] = stock

    def gbce_all_share_index(self):
        if not self.stocks:
            return 0

        product_vwsp = 1
        n = len(self.stocks)

        for stock in self.stocks.values():
            vwsp = stock.volume_weighted_stock_price()
            if vwsp > 0:
                product_vwsp *= vwsp

        return math.pow(product_vwsp, 1 / n)


# Sample data from the International Refreshment Quoter
stocks_data = [
    {"symbol": "TEA", "type": "Common", "last_dividend": 0, "fixed_dividend": None, "par_value": 100},
    {"symbol": "POP", "type": "Common", "last_dividend": 8, "fixed_dividend": None, "par_value": 100},
    {"symbol": "ALE", "type": "Common", "last_dividend": 23, "fixed_dividend": None, "par_value": 60},
    {"symbol": "GIN", "type": "Preferred", "last_dividend": 8, "fixed_dividend": 0.02, "par_value": 100},
    {"symbol": "JOE", "type": "Common", "last_dividend": 13, "fixed_dividend": None, "par_value": 250}
]

# Create market and add stocks
market = Market()
for stock_data in stocks_data:
    stock = Stock(
        symbol=stock_data["symbol"],
        stock_type=stock_data["type"],
        last_dividend=stock_data["last_dividend"],
        fixed_dividend=stock_data["fixed_dividend"],
        par_value=stock_data["par_value"]
    )
    market.add_stock(stock)

# Example Usage
stock = market.stocks["POP"]
print(f"Dividend Yield for POP at price 100: {stock.dividend_yield(100)}")
print(f"P/E Ratio for POP at price 100: {stock.pe_ratio(100)}")

# Record a trade
stock.record_trade(quantity=100, buy_sell_indicator="buy", price=105)

# Calculate Volume Weighted Stock Price for POP
print(f"Volume Weighted Stock Price for POP: {stock.volume_weighted_stock_price()}")

# Calculate GBCE All Share Index
print(f"GBCE All Share Index: {market.gbce_all_share_index()}")
