import logging, time
from dotenv import load_dotenv
from binance.um_futures import UMFutures
from binance.error import ClientError
from typing import Dict, Any, Optional
import os

load_dotenv()

LOGGER = logging.getLogger(__name__)

class BasicBot:
    def __init__(self):
        self.client = UMFutures(
            key=os.getenv("BINANCE_API_KEY"),
            secret=os.getenv("BINANCE_API_SECRET"),
            base_url="https://testnet.binancefuture.com"
        )

    def get_balance(self, asset="USDT"):
        try:
            balances = self.client.balance()
            for b in balances:
                if b["asset"] == asset:
                    return b
            return None
        except ClientError as e:
            LOGGER.error(f"Error fetching balance: {e}")
            return None
        
    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            if order_type.upper() == "MARKET":
                return self.client.new_order(
                    symbol=symbol, side=side, type=order_type, quantity=quantity
                )
            elif order_type.upper() == "LIMIT":
                return self.client.new_order(
                    symbol=symbol, side=side, type=order_type, quantity=quantity, price=price, timeInForce="GTC",
                )
            elif order_type.upper() == "STOP_MARKET":
                return self.client.new_order(
                    symbol=symbol, side=side, type="STOP_MARKET", stopPrice=stop_price, quantity=quantity,
                )
            elif order_type.upper() == "OCO":
                return self.place_oco(symbol, side, quantity, price, stop_price)
            else:
                raise ValueError(f"Unsupported order type: {order_type}")
        except ClientError as e:
            LOGGER.error(f"Order failed: {e}")
            return None
        
    def place_oco(self, symbol, side, quantity, price, stop_price):
        """
        Simulate OCO (Take-Profit + Stop-Loss) on Futures.
        These only make sense AFTER you already hold a position.
        BUY position -> exit SELL TP/SL
        SELL position -> exit BUY TP/SL
        """
        if not price or not stop_price:
            raise ValueError("OCO requires both take profit (price) and stop-loss (stop-price).")
        
        ticker = self.client.ticker_price(symbol=symbol)
        current_price = float(ticker["price"])
        LOGGER.info(f"Current {symbol} price: {current_price}")

        exit_side = "SELL" if side.upper() == "BUY" else "BUY"
        
        if side.upper() == "BUY":
            if price <= current_price:
                raise ValueError(f"For BUY position, TP({price}) must be ABOVE market current price, i.e. {current_price}")
            if stop_price >= current_price:
                raise ValueError(f"For BUY position, SL({stop_price}) must be BELOW market current price, i.e. {current_price}")
        elif side.upper() == "SELL":
            if price >= current_price:
                raise ValueError(f"For SELL position, TP({price}) must be BELOW market current price, i.e. {current_price}")
            if stop_price <= current_price:
                raise ValueError(f"For SELL position, SL({stop_price}) must be ABOVE market current price, i.e. {current_price}")
        LOGGER.info(f"Placing OCO Exit Orders on side={exit_side}; TP={price}, SL={stop_price}")
        take_profit = self.client.new_order(symbol=symbol, side=exit_side, type="TAKE_PROFIT_MARKET", stopPrice=price, reduceOnly=True, quantity=quantity, workingType="MARK_PRICE")
        stop_loss = self.client.new_order(symbol=symbol, side=exit_side, type="STOP_MARKET", stopPrice=stop_price, reduceOnly=True, quantity=quantity, workingType="MARK_PRICE")
        LOGGER.info(f"OCO Orders placed: TP={take_profit['orderId']} SL={stop_loss['orderId']}")
        return {"take_profit": take_profit, "stop_loss": stop_loss}
        while True:
            tp_status = next((o for o in self.client.get_orders(symbol=symbol) if o["orderId"] == take_profit["orderId"]), None)
            sl_status = next((o for o in self.client.get_orders(symbol=symbol) if o["orderId"] == stop_loss["orderId"]), None)
            if tp_status and tp_status["status"] == "FILLED":
                LOGGER.info("Take-Profit filled ✅, cancelling Stop-Loss")
                self.client.cancel_order(symbol=symbol, orderId=stop_loss["orderId"])
                return {"take_profit": tp_status, "stop_loss": "CANCELLED"}
            if sl_status and sl_status["status"] == "FILLED":
                LOGGER.info("Stop-Loss filled ❌, cancelling Take-Profit")
                self.client.cancel_order(symbol=symbol, orderId=take_profit["orderId"])
                return {"take_profit": "CANCELLED", "stop_loss": sl_status}
            
            time.sleep(2)