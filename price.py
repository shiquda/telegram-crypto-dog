import okx.MarketData as MarketData
from loguru import logger

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


def test():
    data = get_tickers_data()
    ticker_data = parse_ticker_data_from_tickers(data, "DOGE-USDT")
    print(ticker_data)
    # print(type(ticker_data))


if __name__ == "__main__":
    test()
