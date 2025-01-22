import time
from price import get_ticker_data


def add_time_prefix():
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f"监控时间：{time.strftime('%Y-%m-%d %H:%M:%S')}\n-----------------------------\n{result}"
        return wrapper
    return decorator


def get_signed_percentage(percentage: float):
    percentage *= 100
    return f"{'' if percentage < 0 else '+'}{percentage:.2f}%"


def get_percentage_string(period: str, percentage: float):
    return f"{period}涨跌幅：{get_signed_percentage(percentage)} {'📈📈📈' if percentage > 0 else '📉📉📉'}"


@add_time_prefix()
def price_query_message(ticker: dict, percentage_dict: dict):
    change_percentage_24h = (float(ticker.get('last')) - float(ticker.get('open24h'))) / float(ticker.get('open24h'))
    percentage_dict.update({"24h": change_percentage_24h})
    trading_url = f"https://www.okx.com/trade-spot/{ticker.get('instId').lower()}"
    percentage_string = '\n'.join([get_percentage_string(period, percentage)
                                  for period, percentage in percentage_dict.items()])
    return f"""产品：{ticker.get('instId')}
最新价：{ticker.get('last')}
{percentage_string}
24h成交量：{ticker.get('vol24h')}
24h成交额：{ticker.get('volCcy24h')}

前往交易（OKX）：{trading_url}
"""


if __name__ == "__main__":
    print(price_query_message(get_ticker_data("BTC-USDT"), {}))
