import requests
import telebot
import time
import sys

# 🔑 Твой токен и канал
BOT_TOKEN = "8214125690:AAFms15KN37G_j8549oM4Lvn19FW3XmyJrs"
CHANNEL_ID = "@dollarpricetg"

bot = telebot.TeleBot(BOT_TOKEN)

# 💱 Валюты Центральной Азии + основные
TARGETS = ["RUB", "KZT", "KGS", "UZS", "TJS", "AFN", "TRY", "EUR", "CNY"]
last_rates = {}

def fetch_rates():
    """Получаем курсы USD -> TARGETS из open.er-api.com"""
    url = "https://open.er-api.com/v6/latest/USD"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()

    if data.get("result") != "success":
        raise RuntimeError("Не удалось получить курсы от open.er-api.com")

    rates = data["rates"]
    return {code: rates.get(code) for code in TARGETS}

def get_trend(iso_code, new_value):
    """Определяем тренд (рост, падение, процент изменения)"""
    if iso_code not in last_rates:
        return "🆕", None
    old_value = last_rates[iso_code]
    if not old_value or old_value == 0:
        return "➡️", 0
    change = ((new_value - old_value) / old_value) * 100
    if change > 0.05:
        return "📈", change
    elif change < -0.05:
        return "📉", change
    else:
        return "➡️", change

def format_message(rates: dict) -> str:
    msg = "💵 **Курс доллара (1 USD):**\n\n"

    for code in TARGETS:
        if code not in rates or not rates[code]:
            continue

        trend, change = get_trend(code, rates[code])
        val = rates[code]
        change_text = f" ({change:+.2f}%)" if change is not None else ""

        if code == "RUB":
            msg += f"🇷🇺 Рубль: {val:.2f} ₽ {trend}{change_text}\n"
        elif code == "KZT":
            msg += f"🇰🇿 Казахстанский тенге: {val:.2f} ₸ {trend}{change_text}\n"
        elif code == "KGS":
            msg += f"🇰🇬 Кыргызский сом: {val:.2f} с {trend}{change_text}\n"
        elif code == "UZS":
            msg += f"🇺🇿 Узбекский сум: {val:,.0f} сум {trend}{change_text}\n".replace(",", " ")
        elif code == "TJS":
            msg += f"🇹🇯 Таджикский сомони: {val:.2f} сомони {trend}{change_text}\n"
        elif code == "AFN":
            msg += f"🇦🇫 Афгани: {val:.2f} ؋ {trend}{change_text}\n"
        elif code == "TRY":
            msg += f"🇹🇷 Турецкая лира: {val:.2f} ₺ {trend}{change_text}\n"
        elif code == "EUR":
            msg += f"🇪🇺 Евро: {val:.2f} € {trend}{change_text}\n"
        elif code == "CNY":
            msg += f"🇨🇳 Юань: {val:.2f} ¥ {trend}{change_text}\n"

    msg += "\n🔁 Обновление каждые 3 часа"
    return msg

def debug_print(rates):
    print("---- Текущие курсы ----")
    for code, val in rates.items():
        print(f"{code}: {val}")
    print("-----------------------")

print("✅ Бот запущен. Отслеживаются валюты Центральной Азии + основные мировые.")

while True:
    try:
        rates = fetch_rates()
        debug_print(rates)

        message = format_message(rates)
        bot.send_message(CHANNEL_ID, message, parse_mode="Markdown")
        print("✅ Сообщение отправлено.\n")

        last_rates = rates.copy()
        time.sleep(10800)  # каждые 3 часа
    except KeyboardInterrupt:
        print("⛔ Остановлено пользователем.")
        sys.exit(0)
    except Exception as e:
        print("⚠️ Ошибка:", e)
        time.sleep(60)
