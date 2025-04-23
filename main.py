import requests
import telebot
import json
import threading
from bs4 import BeautifulSoup as BS
import time

bot = telebot.TeleBot("8034462858:AAFODzmWHFofakAomMOGEilsyu06XW1sCbs")

# Храним пользователей, которые написали боту
users = set()

# Команда /start — добавляет пользователя в список подписчиков
@bot.message_handler(commands=['start'])
def send_welcome(message):
    users.add(message.chat.id)
    bot.reply_to(message, "✅ Ты добавлен в список отслеживания цен!")

# Список предметов для мониторинга
items = [
    {"id": "139654846", "name": "M4A4 | Звездный крейсер (После полевых испытаний)"},
    {"id": "176460476", "name": "Desert Eagle | Термическая обработка (После полевых испытаний)"}
]

currency = 37
start_prices = {item["id"]: {"buy": "", "sell": ""} for item in items}

# Функция мониторинга цен
def monitor_prices():
    while True:
        try:
            for item in items:
                item_id = item["id"]
                item_name = item["name"]
                link = f"https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency={currency}&item_nameid={item_id}"

                req = requests.get(link)
                req.raise_for_status()
                js = json.loads(req.content)

                if not all(k in js for k in ["sell_order_summary", "buy_order_summary"]):
                    continue

                def parse_price(data):
                    return BS(data, 'html.parser').text.split(':')[-1].strip()

                new_buy_price = parse_price(js["buy_order_summary"])
                new_sell_price = parse_price(js["sell_order_summary"])

                if start_prices[item_id] != {"buy": new_buy_price, "sell": new_sell_price}:
                    message_text = (
                        f"📌 Название: {item_name}\n"
                        f"💰 Начальная цена: {new_buy_price}\n"
                        f"📈 Максимальная цена: {new_sell_price}"
                    )

                    start_prices[item_id] = {"buy": new_buy_price, "sell": new_sell_price}

                    # Отправляем обновления всем пользователям
                    for user_id in users:
                        bot.send_message(user_id, message_text, parse_mode="Markdown")
                else:
                    pass
            time.sleep(60)

        except Exception as e:
            print(f"⚠️ Ошибка: {e}")

# Запускаем мониторинг в отдельном потоке
monitor_thread = threading.Thread(target=monitor_prices)
monitor_thread.start()

# Запускаем Telegram-бота (в основном потоке)
bot.polling()