import telegram as tg
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import configparser
import asyncio
from price import get_ticker_data, get_coin_price_percentage
from utils import price_query_message
from loguru import logger
from setup import setup

config = configparser.ConfigParser()
config.read("config.cfg")

DEBUG = config.getboolean("general", "DEBUG")

TELEGRAM_BOT_TOKEN = config.get("telegram", "TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = config.get("telegram", "TELEGRAM_CHAT_ID")
TELEGRAM_WEBHOOK_URL = config.get("telegram", "TELEGRAM_WEBHOOK_URL")
USE_WEBHOOK = config.getboolean("telegram", "USE_WEBHOOK")
LISTEN_PORT = config.getint("telegram", "LISTEN_PORT")


async def send_message_to_group(chat_id, message):
    bot = tg.Bot(TELEGRAM_BOT_TOKEN)
    async with bot:
        # print(await bot.get_me())
        await bot.send_message(chat_id=chat_id, text=message)

# command


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"用户 {update.message.from_user.username} 使用机器人 /start")
    await update.message.reply_text("🐶我可以帮您监控币圈动态！🐶")


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        coin_swap = context.args[0].upper()
        if "-" not in coin_swap:
            coin_swap = f"{coin_swap}-USDT"
        logger.info(f"用户 {update.message.from_user.username} 使用机器人 /price 查询 {coin_swap} 的价格")

        loop = asyncio.get_event_loop()
        ticker_data = await loop.run_in_executor(None, get_ticker_data, coin_swap)

        if ticker_data is None:
            logger.error(f"未能获取到ticker数据")
            raise ValueError("未能获取到ticker数据")

        # 查询前1min、15min、1h、4h的涨跌幅
        current_price = float(ticker_data.get("last"))

        tasks = [
            loop.run_in_executor(None, get_coin_price_percentage, coin_swap, 60*1000, current_price),
            loop.run_in_executor(None, get_coin_price_percentage, coin_swap, 15*60*1000, current_price),
            loop.run_in_executor(None, get_coin_price_percentage, coin_swap, 60*60*1000, current_price),
            loop.run_in_executor(None, get_coin_price_percentage, coin_swap, 4*60*60*1000, current_price)
        ]

        price_percentage_1min, price_percentage_15min, price_percentage_1h, price_percentage_4h = await asyncio.gather(*tasks)

        percentage_dict = {
            "1min": price_percentage_1min,
            "15min": price_percentage_15min,
            "1h": price_percentage_1h,
            "4h": price_percentage_4h
        }
        logger.success(f"查询 {coin_swap} 成功！")
        await update.message.reply_text(price_query_message(ticker_data, percentage_dict))
    except Exception as e:
        logger.error(f"用户 {update.message.from_user.username} 使用机器人 /price 查询 {coin_swap} 的价格失败，错误信息：{e}")
        await update.message.reply_text("请输入正确的币种名称，例如 /price BTC，/price ETH-BTC")
        if DEBUG:
            await update.message.reply_text(f"[DEBUG] 错误信息：{e}")


def run():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("price", price))

    if USE_WEBHOOK:
        logger.info("开始使用Webhook监听...")

        app.run_webhook(
            listen="0.0.0.0",
            port=LISTEN_PORT,
            url_path="telegram",
            webhook_url=f"{TELEGRAM_WEBHOOK_URL}/telegram",
        )
    else:
        logger.info("开始使用Polling轮询...")
        app.run_polling()


if __name__ == "__main__":
    run()
