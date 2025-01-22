import telegram as tg
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import configparser
import asyncio
from price import get_ticker_data
from utils import price_query_message
from loguru import logger
from setup import setup

config = configparser.ConfigParser()
config.read("config.cfg")

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
        query = context.args[0].upper()
        if "-" not in query:
            query = f"{query}-USDT"
        logger.info(f"用户 {update.message.from_user.username} 使用机器人 /price 查询 {query} 的价格")
        ticker_data = get_ticker_data(query)
        logger.success(f"查询 {query} 成功！")
        await update.message.reply_text(price_query_message(ticker_data))
    except Exception as e:
        logger.error(f"用户 {update.message.from_user.username} 使用机器人 /price 查询 {query} 的价格失败，错误信息：{e}")
        await update.message.reply_text("请输入正确的币种名称，例如 /price BTC，/price ETH-BTC")


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
