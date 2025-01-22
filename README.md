# 加密货币监控 Telegram 机器人

*本项目正处于早期开发之中。*

🐶Wolf!🐶

本项目是一个基于 Telegram 的加密货币价格监控机器人，能够实时查询各类加密货币的最新价格和相关数据，并期望实现行情的自动提醒。

## 功能

- **查询价格**：通过 `/price` 命令查询指定加密货币的最新价格。
- **支持Webhook与轮询**：可选择使用 Webhook 或 Polling 方式接收 Telegram 更新。
- **日志记录**：使用 Loguru 记录运行日志，方便调试与维护。

## 安装

### 克隆仓库

```bash
git clone <仓库地址>
cd <仓库目录>
```

### 安装依赖

确保已安装 [Python 3.7+](https://www.python.org/downloads/)，然后安装所需依赖：

```bash
pip install -r requirements.txt
```

## 配置

复制示例配置文件并进行编辑：

```bash
cp config.cfg.example config.cfg
```

编辑 `config.cfg` 文件：

```config.cfg
[telegram]
TELEGRAM_BOT_TOKEN = 你的Telegram机器人令牌
TELEGRAM_CHAT_ID = 你的聊天ID
TELEGRAM_WEBHOOK_URL = https://your.webhook.url
USE_WEBHOOK = False
# 本地webhook监听端口
LISTEN_PORT = 8080 
```

## 使用

### 设置Bot命令

运行以下命令设置 Telegram Bot 的可用命令：

```bash
python setup.py
```

### 启动机器人

启动 Telegram 机器人：

```bash
python bot.py
```

机器人将根据配置文件选择使用 Webhook 或 Polling 方式运行。

## TO-DO

- [ ] 实现更多行情数据的获取，例如1h涨跌幅、5min涨跌幅
- [ ] 实现群组消息主动发送
- [ ] 实现用户添加监控币种功能
- [ ] 实现消息面信息智能解读功能
- [ ] ...设想中

## 许可证

本项目采用 AGPL v3 许可证，详情请参阅 [LICENSE](LICENSE) 文件。
