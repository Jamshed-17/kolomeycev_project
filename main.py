import requests
import telebot

import json #json )
import pprint #красивый вывод json
from bs4 import BeautifulSoup as BS

bot = telebot.TeleBot('8034462858:AAFODzmWHFofakAomMOGEilsyu06XW1sCbs')

start_price = ""
start_price1 = ""

while True:
    #link = "https://steamcommunity.com/market/listings/730/M4A4%20%7C%20The%20Battlestar%20(Field-Tested)?l=russian" #сама пагадже
    #maket = "https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=1&item_nameid="
    item_id = "139654846"
    currency = 37    # 1-usd; 2-франки;3 -евро;5-рубли
    link = f"https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency={currency}&item_nameid={item_id}" #api link for request

    req = requests.get(link) #делаем get

    # price = soup.select(".market_commodity_orders_header_promote") #здесь только ради тега
    js = json.loads(req.content) #загружаем json
    searched_tag = js["sell_order_summary"] #берем нужное
    searched_tag1 = js["buy_order_summary"] #берем нужное
    addition_soup = BS(searched_tag, 'html.parser') #это вообще только ради того, чтобы взять только текст
    addition_soup1 = BS(searched_tag1, 'html.parser') #это вообще только ради того, чтобы взять только текст


    if start_price == (addition_soup1.text.split(':')[-1]) and start_price1 == (addition_soup.text.split(':')[-1]):
        pass
    else:


        finishText = ("Название: M4A4 | Звездный крейсер\n"
                      + "Износ: После полевых испытаний\n"
                      + addition_soup1.text.split('Начальная цена')[-2]
                      + "\nНачальная цена: "
                      + addition_soup1.text.split(':')[-1]
                      + "\nМаксимальная цена: "
                      + addition_soup.text.split(':')[-1])

        start_price = addition_soup1.text.split(':')[-1]
        start_price1 = addition_soup.text.split(':')[-1]

        bot.send_message(2008381570, finishText)
        print(start_price)
        print(start_price1)
        print()
    time.sleep(60)
