import asyncio
import telegram as tg
import configparser
from loguru import logger

config = configparser.ConfigParser()
config.read("config.cfg")
TELEGRAM_BOT_TOKEN = config.get("telegram", "TELEGRAM_BOT_TOKEN")
TELEGRAM_WEBHOOK_URL = config.get("telegram", "TELEGRAM_WEBHOOK_URL")

# Command


async def setup():
    # 设置命令
    bot = tg.Bot(TELEGRAM_BOT_TOKEN)

    logger.info("设置Bot命令...")
    await bot.set_my_commands([
        tg.BotCommand(command="/start", description="开始"),
        tg.BotCommand(command="/help", description="帮助"),
        tg.BotCommand(command="/price", description="价格，例如 /price BTC，/price ETH-BTC"),
    ])

    logger.info(await bot.get_my_commands())
    logger.info("Done!")


if __name__ == "__main__":
    asyncio.run(setup())
