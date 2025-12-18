# main.py

from core.mt5_connector import MT5Connector
from core.telegram_notifier import TelegramNotifier
from core.logger import setup_logger
from config.settings import SYMBOL

def main():
    logger = setup_logger()
    notifier = TelegramNotifier()
    mt5_conn = MT5Connector()

    logger.info("Starting SMC MT5 Bot...")
    notifier.send("🚀 SMC MT5 Bot starting up")

    try:
        mt5_conn.connect()
        mt5_conn.ensure_symbol(SYMBOL)

        account = mt5_conn.account_info()
        logger.info(f"Connected to MT5 | Balance: {account.balance}")
        notifier.send(
            f"✅ Connected to MT5\nBalance: {account.balance}"
        )

    except Exception as e:
        logger.error(str(e))
        notifier.send(f"❌ Bot error: {e}")

    finally:
        mt5_conn.shutdown()
        logger.info("MT5 connection closed")

if __name__ == "__main__":
    main()
