import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# Bot token
TOKEN = os.environ.get("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")

# Google Sheets credential
google_creds = os.environ.get("GOOGLE_CREDENTIALS")
creds_dict = json.loads(google_creds)

# Google Sheets config
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
client = gspread.authorize(CREDS)

# Sheet ID va nomi
SHEET_ID = "13fJhXz3BAoz4-hA4F2YdmZQqpWaoL_dwhsl-76FZiVQ"
SHEET_NAME = "Sheet1"

sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

# Botni yaratish
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🧴 Yuz", "💇 Soch")
    markup.row("🛁 Tana", "🌸 Intim")
    markup.row("💄 Lab", "💅 Tirnoq")
    bot.send_message(message.chat.id, "👋 Assalomu alaykum!\nQuyidagi kategoriyalardan birini tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def message_handler(message):
    text = message.text.lower()
    all_data = sheet.get_all_records()
    found = [row for row in all_data if text in row["Kategoriya"].lower()]

    if found:
        for product in found:
            javob = f"🛍 {product['Nom']}\n💰 {product['Narx']}\n📦 {product['Kategoriya']}"
            bot.send_message(message.chat.id, javob)
    else:
        bot.send_message(message.chat.id, "🛒 Afsus, bu kategoriya bo‘yicha mahsulot topilmadi.")

print("Bot polling...")
bot.infinity_polling()
