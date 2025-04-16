import alpaca_trade_api as tradeapi
import time
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TradingBot:
    def __init__(self, api_key, api_secret, base_url='https://paper-api.alpaca.markets'):
        """
        Initialize with connection testing
        """
        try:
            self.api = tradeapi.REST(api_key, api_secret, base_url)
            self.api.get_clock()  # Test connection
            self.account = self.api.get_account()
            logger.info(f"Initialized trading bot for account {self.account.account_number}")
        except Exception as e:
            logger.error(f"Failed to initialize: {str(e)}")
            raise

    def check_market_hours(self):
        """
        More robust market hours check
        """
        try:
            clock = self.api.get_clock()
            logger.debug(f"Market is {'open' if clock.is_open else 'closed'}")
            return clock.is_open
        except Exception as e:
            logger.error(f"Error checking market hours: {str(e)}")
            return False

    def get_account_info(self):
        """
        Get current account information
        """
        self.account = self.api.get_account()
        return {
            'buying_power': float(self.account.buying_power),
            'cash': float(self.account.cash),
            'portfolio_value': float(self.account.portfolio_value),
            'equity': float(self.account.equity)
        }

    def get_position(self, symbol):
        """
        Get current position for a symbol
        """
        try:
            position = self.api.get_position(symbol)
            return {
                'symbol': position.symbol,
                'qty': float(position.qty),
                'market_value': float(position.market_value),
                'avg_entry_price': float(position.avg_entry_price)
            }
        except:
            return None

    def get_historical_data(self, symbol, timeframe='1D', limit=100):
        """
        Get historical price data for analysis - improved version
        """
        try:
            # Get bars with timeout and error handling
            barset = self.api.get_bars(
                symbol,
                timeframe,
                limit=limit,
                adjustment='raw'  # Get unadjusted data
            )

            if not barset:
                logger.warning(f"No bars returned for {symbol}")
                return pd.DataFrame()

            # Convert to DataFrame and ensure proper columns
            df = barset.df
            if df.empty:
                logger.warning(f"Empty DataFrame for {symbol}")
                return pd.DataFrame()

            logger.debug(f"Got {len(df)} bars for {symbol}")
            return df

        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return pd.DataFrame()

    def simple_moving_average_strategy(self, symbol, short_window=20, long_window=50):
        """
        SMA crossover strategy with better data validation
        """
        # Get sufficient data for the longest window
        data = self.get_historical_data(symbol, limit=long_window + 10)

        # Validate data
        if data.empty:
            logger.warning("No data returned from API")
            return 'hold'

        if len(data) < long_window:
            logger.warning(f"Only {len(data)} bars available, need at least {long_window}")
            return 'hold'

        # Calculate SMAs
        data['short_sma'] = data['close'].rolling(window=short_window).mean()
        data['long_sma'] = data['close'].rolling(window=long_window).mean()

        # Need at least 2 data points after calculating SMAs
        if len(data) < 2:
            return 'hold'

        latest = data.iloc[-1]
        previous = data.iloc[-2]

        # Generate signals
        if pd.isna(previous['short_sma']) or pd.isna(previous['long_sma']):
            return 'hold'

        if previous['short_sma'] <= previous['long_sma'] and latest['short_sma'] > latest['long_sma']:
            return 'buy'
        elif previous['short_sma'] >= previous['long_sma'] and latest['short_sma'] < latest['long_sma']:
            return 'sell'
        return 'hold'

    def simple_moving_average_strategy(self, symbol, short_window=20, long_window=50):
        """
        Basic SMA crossover strategy
        """
        data = self.get_historical_data(symbol)

        # Check if we got valid data
        if data.empty or len(data) < long_window:
            logger.warning("Not enough data for SMA calculation")
            return 'hold'

        data['short_sma'] = data['close'].rolling(window=short_window).mean()
        data['long_sma'] = data['close'].rolling(window=long_window).mean()

        # Get the latest values
        latest = data.iloc[-1]
        previous = data.iloc[-2]

        # Buy signal: short SMA crosses above long SMA
        if previous['short_sma'] <= previous['long_sma'] and latest['short_sma'] > latest['long_sma']:
            return 'buy'
        # Sell signal: short SMA crosses below long SMA
        elif previous['short_sma'] >= previous['long_sma'] and latest['short_sma'] < latest['long_sma']:
            return 'sell'
        else:
            return 'hold'
    def execute_trade(self, symbol, qty, side, type='market', time_in_force='gtc'):
        """
        Execute a trade order
        """
        try:
            if side.lower() not in ['buy', 'sell']:
                raise ValueError("Side must be either 'buy' or 'sell'")

            logger.info(f"Placing {side} order for {qty} shares of {symbol}")

            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type=type,
                time_in_force=time_in_force
            )

            logger.info(f"Order placed: {order.id}")
            return order
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return None

    def run_bot(self, symbol, strategy='sma', trade_amount=1000, risk_per_trade=0.01):
        """
        Main bot execution loop with error recovery
        """
        logger.info(f"Starting trading bot for {symbol}...")

        retry_count = 0
        max_retries = 3

        while True:
            try:
                if retry_count >= max_retries:
                    logger.error("Max retries reached, shutting down")
                    break

                if not self.check_market_hours():
                    logger.info("Market is closed. Sleeping for 5 minutes...")
                    time.sleep(300)
                    continue

                # Rest of your trading logic...

                # Reset retry count after successful iteration
                retry_count = 0
                time.sleep(60)

            except Exception as e:
                retry_count += 1
                logger.error(f"Error in main loop (attempt {retry_count}/{max_retries}): {str(e)}")
                time.sleep(10)

    def is_symbol_tradeable(self, symbol):
        try:
            asset = self.api.get_asset(symbol)
            return asset.tradable and asset.status == 'active'
        except:
            return False

if __name__ == "__main__":
    # Replace with your Alpaca API keys
    API_KEY = 'PKRRLNTL9PEXVJZL0HE7'
    API_SECRET ='pwmEaIdAdwHZh8t9mOWlQVEypI42uib345bcm15v'

    # Initialize and run the bot
    bot = TradingBot(API_KEY, API_SECRET)

    # Run with a simple strategy for AAPL
    bot.run_bot('AAPL', strategy='sma')
