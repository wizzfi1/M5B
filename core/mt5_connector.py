# core/mt5_connector.py

import MetaTrader5 as mt5
from config.settings import (
    MT5_LOGIN, MT5_PASSWORD, MT5_SERVER, MT5_PATH
)

class MT5Connector:
    def __init__(self):
        self.connected = False

    def connect(self):
        if MT5_PATH:
            mt5.initialize(path=MT5_PATH)
        else:
            mt5.initialize()

        authorized = mt5.login(
            login=MT5_LOGIN,
            password=MT5_PASSWORD,
            server=MT5_SERVER
        )

        if not authorized:
            raise RuntimeError(f"MT5 login failed: {mt5.last_error()}")

        self.connected = True
        return True

    def shutdown(self):
        if self.connected:
            mt5.shutdown()
            self.connected = False

    def account_info(self):
        return mt5.account_info()

    def symbol_info(self, symbol):
        info = mt5.symbol_info(symbol)
        if info is None:
            raise RuntimeError(f"Symbol {symbol} not found")
        return info

    def ensure_symbol(self, symbol):
        info = self.symbol_info(symbol)
        if not info.visible:
            if not mt5.symbol_select(symbol, True):
                raise RuntimeError(f"Failed to select symbol {symbol}")
