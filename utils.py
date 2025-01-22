import time
from price import get_ticker_data


def add_time_prefix():
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f"监控时间：{time.strftime('%Y-%m-%d %H:%M:%S')}\n-----------------------------\n{result}"
        return wrapper
    return decorator


@add_time_prefix()
def say_hello(name):
    return f"Hello, {name}!"


@add_time_prefix()
def price_query_message(ticker: dict):
    change_percentage_24h = (float(ticker.get('last')) - float(ticker.get('open24h'))) / \
        float(ticker.get('open24h')) * 100
    trading_url = f"https://www.okx.com/trade-spot/{ticker.get('instId').lower()}"
    return f"""产品：{ticker.get('instId')}
最新价：{ticker.get('last')}
{"📈📈📈" if change_percentage_24h >= 0 else "📉📉📉"}24h涨跌幅：{"+" if change_percentage_24h >= 0 else ""}{change_percentage_24h:.2f}%
24h成交量：{ticker.get('vol24h')}
24h成交额：{ticker.get('volCcy24h')}

前往交易（OKX）：{trading_url}
"""

if __name__ == "__main__":
    print(price_query_message(get_ticker_data("BTC-USDT")))
