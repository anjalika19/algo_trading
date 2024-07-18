import backtrader as bt
import yfinance as yf
import pandas as pd

# Create a custom strategy
class TrendFollowingStrategy(bt.Strategy):
    params = (
        ('sma_period', 50),
    )

    def __init__(self):
        # Define indicators
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period = self.params.sma_period)
        self.adx = bt.indicators.AverageDirectionalMovementIndex(self.data)
        self.bollinger = bt.indicators.BollingerBands(self.data.close)

    def next(self):
        # if not self.position:  # Not in the market
        if self.data.close > self.sma and self.adx.adx > 18:  # Trend following condition
                if self.data.close > self.bollinger.lines.bot:  # Bollinger Bands condition
                    self.buy()  # Buy signal
        else:
            if self.data.close < self.sma or self.adx.adx < 18:
                self.sell()  # Sell signal

# Fetch data using yfinance and prepare it for Backtrader
data = yf.download("AAPL", start = "2023-02-01", end = "2024-02-01")

# Convert the data to a format that Backtrader can use
data_feed = bt.feeds.PandasData(dataname=data)

# Initialize Cerebro
cerebro = bt.Cerebro()

# Add data feed to Cerebro
cerebro.adddata(data_feed)

# Add strategy to Cerebro
cerebro.addstrategy(TrendFollowingStrategy)

# Set initial cash
cerebro.broker.set_cash(10000)

# Print out the starting cash
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Run the backtest
cerebro.run()

# Print out the final cash
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Plot the result
cerebro.plot(style = "candle")

