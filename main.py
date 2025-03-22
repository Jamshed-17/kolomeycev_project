import requests
import telebot
import time
import json
from bs4 import BeautifulSoup as BS

bot = telebot.TeleBot('8034462858:AAFODzmWHFofakAomMOGEilsyu06XW1sCbs')

start_price = ""
start_price1 = ""

while True:
    try:
        item_id = "139654846"
        currency = 37
        link = f"https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency={currency}&item_nameid={item_id}"

        req = requests.get(link)
        req.raise_for_status() 

        js = json.loads(req.content)
        searched_tag = js["sell_order_summary"]
        searched_tag1 = js["buy_order_summary"]
        addition_soup = BS(searched_tag, 'html.parser')
        addition_soup1 = BS(searched_tag1, 'html.parser')

        new_price = addition_soup1.text.split(':')[-1]
        new_price1 = addition_soup.text.split(':')[-1]

        if start_price != new_price or start_price1 != new_price1:
            finishText = (
                "Название: M4A4 | Звездный крейсер\n"
                + "Износ: После полевых испытаний\n"
                + addition_soup1.text.split('Начальная цена')[-2]
                + "\nНачальная цена: " + new_price
                + "\nМаксимальная цена: " + new_price1
            )

            start_price = new_price
            start_price1 = new_price1
            bot.send_message(2008381570, finishText)

        else:
            pass

    except Exception as e:
        bot.send_message(2008381570, f"Ошибка - {e}")

    time.sleep(60)
