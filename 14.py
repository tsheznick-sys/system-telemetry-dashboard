import numpy as np
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [QUANT_BACKTEST] %(message)s")

class BacktestEngine:
    def __init__(self, initial_capital: float = 10000.0):
        self.capital = initial_capital
        self.position = 0.0

    def generate_data(self, periods: int = 200) -> pd.DataFrame:
        np.random.seed(42)
        prices = 50000 + np.cumsum(np.random.normal(loc=0, scale=150, size=periods))
        df = pd.DataFrame({"price": prices})
        df["sma_short"] = df["price"].rolling(window=10).mean()
        df["sma_long"] = df["price"].rolling(window=50).mean()
        return df.dropna()

    def run(self):
        df = self.generate_data()
        cash = self.capital
        holding = 0.0

        for i in range(1, len(df)):
            price = df["price"].iloc[i]
            short_ma = df["sma_short"].iloc[i]
            long_ma = df["sma_long"].iloc[i]
            prev_short = df["sma_short"].iloc[i-1]
            prev_long = df["sma_long"].iloc[i-1]
            long_trend_rising = (
                i >= 2 and long_ma > df["sma_long"].iloc[i-2]
            )

            # Buy Signal: Short MA crosses above Long MA
            if (
                prev_short <= prev_long
                and short_ma > long_ma
                and long_trend_rising
                and holding == 0
            ):
                holding = cash / price
                cash = 0.0
                logging.info(f"🟢 BUY executed at ${price:,.2f}")

            # Sell Signal: Short MA crosses below Long MA
            elif prev_short >= prev_long and short_ma < long_ma and holding > 0:
                cash = holding * price
                holding = 0.0
                logging.info(f"🔴 SELL executed at ${price:,.2f} | Portfolio Value: ${cash:,.2f}")

        final_portfolio = cash if holding == 0 else holding * df["price"].iloc[-1]
        pnl = final_portfolio - self.capital
        logging.info(f"=== BACKTEST COMPLETE ===")
        logging.info(f"Initial Capital: ${self.capital:,.2f} | Final Portfolio: ${final_portfolio:,.2f} | PnL: ${pnl:+,.2f}")

if __name__ == "__main__":
    engine = BacktestEngine()
    engine.run()
