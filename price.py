import okx.MarketData as MarketData
from loguru import logger
import time

marketDataAPI = MarketData.MarketAPI()


def get_tickers_data():
    try:
        result = marketDataAPI.get_tickers(instType="SPOT")
        if result.get("code") == "0":
            return result.get("data")
        else:
            logger.error(f"获取tickers数据失败: {result.get('msg')}")
            return None

    except Exception as e:
        logger.error(f"获取tickers数据时发生错误: {e}")
        return None


def get_ticker_data(inst_id):
    try:
        result = marketDataAPI.get_ticker(instId=inst_id)
        if result.get("code") == "0":
            return result.get("data")[0]
        else:
            logger.error(f"获取ticker数据失败: {result.get('msg')}")
            return None
    except Exception as e:
        logger.error(f"获取ticker数据时发生错误: {e}")
        return None


def parse_ticker_data_from_tickers(data, inst_id):
    for item in data:
        if item.get("instId") == inst_id:
            return item
    return None


def get_candle_data(inst_id, period: str, after: str = None, limit: str = None):
    try:
        result = marketDataAPI.get_history_candlesticks(
            instId=inst_id, bar=period, after=after, limit=limit)
        if result.get("code") == "0":
            return result.get("data")
        else:
            logger.error(f"获取candle数据失败: {result.get('msg')}")
            return None
    except Exception as e:
        logger.error(f"获取candle数据时发生错误: {e}")
        return None


def get_coin_price_at_timestamp(inst_id, timestamp: str) -> float:
    try:
        candle_data = get_candle_data(inst_id, "1m", after=timestamp, limit=1)
        if candle_data:
            # print(candle_data[-1][0])
            # 距离时间点最近的收盘价作为价格 https://www.okx.com/docs-v5/zh/#order-book-trading-market-data-get-candlesticks
            return float(candle_data[-1][4])
        else:
            logger.error(f"获取{inst_id} 于 {timestamp} 的价格时发生错误: 没有找到数据")
            return None
    except Exception as e:
        logger.error(f"获取{inst_id} 于 {timestamp} 的价格时发生错误: {e}")
        return None


def get_coin_price_percentage(inst_id, interval: int, current_price: float):
    """
    获取当前时间点前 interval 毫秒时间的收盘价涨跌幅
    """
    current_timestamp = int(time.time() * 1000)
    last_timestamp = current_timestamp - interval
    last_price = get_coin_price_at_timestamp(inst_id, last_timestamp)
    if last_price:
        return (last_price - current_price) / current_price
    else:
        logger.error(f"获取{inst_id} 于 {last_timestamp} 的价格时发生错误: 没有找到数据")
        return None


def test():
    print(get_coin_price_percentage("DOGE-USDT", 10000000, 0.3769))


if __name__ == "__main__":
    test()
