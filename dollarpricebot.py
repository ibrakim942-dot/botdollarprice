import os
import requests
import telebot

BOT_TOKEN = os.getenv("8214125690:AAFms15KN37G_j8549oM4Lvn19FW3XmyJrs")
CHANNEL_ID = os.getenv("@dollarpricetg")

bot = telebot.TeleBot(BOT_TOKEN)

def get_dollar_price():
    # Пример запроса курса (можешь заменить на любой источник)
    response = requests.get("https://api.exchangerate.host/latest?base=USD&symbols=RUB")
    data = response.json()
    return round(data["rates"]["RUB"], 2)

def main():
    price = get_dollar_price()
    text = f"💵 Текущий курс доллара: {price}₽"
    bot.send_message(CHANNEL_ID, text)

if __name__ == "__main__":
    main()
