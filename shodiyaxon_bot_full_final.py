import telebot
import gspread
import re
import time
import datetime
import json
from oauth2client.service_account import ServiceAccountCredentials
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- Tokenni ochiq yozdik faqat lokal test uchun! ---
TOKEN = '8016989870:AAEDPPuzrt_H0ShF9qpU4Aa1UbOJGVGt1SE'
bot = telebot.TeleBot(TOKEN)

# --- Google Sheets credentials ---
creds_dict = {
  "type": "service_account",
  "project_id": "pelagic-range-460509-r8",
  "private_key_id": "7dedecc03d8f2cb786ffb8051b675f6f409b8052",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEv...YOUR_KEY...IDAQAB\n-----END PRIVATE KEY-----\n",
  "client_email": "shodiyaxon-beauty-bot@ulugbekyaminov337.iam.gserviceaccount.com",
  "client_id": "100264477152104897923",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/shodiyaxon-beauty-bot%40ulugbekyaminov337.iam.gserviceaccount.com"
}

SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
client = gspread.authorize(creds)

SHEET_ID = '13fJhXz3BAoz4-hA4F2YdmZQqpWaoL_dwhsl-76FZiVQ'
SHEET_NAME = 'Sheet1'
sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

user_states = {}
user_orders = {}

def to_safe_callback(text):
    text = text.lower().strip().replace(" ", "_")
    return re.sub(r"[^a-z0-9_]", "", text)[:50]

@bot.message_handler(commands=['start'])
def start_handler(message):
    rows = sheet.get_all_records()
    kategoriyalar = sorted(set([row['Kategoriya'] for row in rows if row.get('Kategoriya')]))
    markup = InlineKeyboardMarkup()
    for kat in kategoriyalar:
        markup.add(InlineKeyboardButton(text=kat, callback_data=f"kat_{to_safe_callback(kat)}"))
    bot.send_message(message.chat.id, "🗂 Kategoriya tanlang:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("kat_"))
def show_products(call):
    kategoriya_kod = call.data.split("_", 1)[1]
    rows = sheet.get_all_records()
    mahsulotlar = [r for r in rows if to_safe_callback(r['Kategoriya']) == kategoriya_kod]

    if not mahsulotlar:
        bot.send_message(call.message.chat.id, "❌ Bu kategoriyada mahsulot topilmadi.")
        return

    for mahsulot in mahsulotlar:
        nomi = mahsulot['Nomi']
        narx = mahsulot['Narx']
        rasm_url = mahsulot.get('Rasm URL', '').strip()
        caption = f"📦 {nomi}\n💰 {narx} so'm"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🛒 Buyurtma berish", callback_data=f"buyurt_{to_safe_callback(nomi)}"))
        try:
            if rasm_url.startswith("http"):
                bot.send_photo(call.message.chat.id, photo=rasm_url, caption=caption, reply_markup=markup)
            else:
                bot.send_message(call.message.chat.id, caption, reply_markup=markup)
        except Exception as e:
            print(f"Xatolik: {e}")
            bot.send_message(call.message.chat.id, caption, reply_markup=markup)
        time.sleep(1)

@bot.callback_query_handler(func=lambda call: call.data.startswith("buyurt_"))
def ask_name(call):
    user_id = call.from_user.id
    product_name = call.data.split("_", 1)[1]
    user_orders[user_id] = {'mahsulot': product_name}
    user_states[user_id] = 'ask_name'
    bot.send_message(call.message.chat.id, "📛 Ismingizni kiriting:")

@bot.message_handler(func=lambda message: message.chat.id in user_states)
def handle_order(message):
    user_id = message.chat.id
    state = user_states.get(user_id)

    if state == 'ask_name':
        user_orders[user_id]['ism'] = message.text
        user_states[user_id] = 'ask_phone'
        bot.send_message(user_id, "📞 Telefon raqamingizni kiriting:")

    elif state == 'ask_phone':
        user_orders[user_id]['telefon'] = message.text
        user_states[user_id] = 'ask_address'
        bot.send_message(user_id, "📍 Manzilingizni kiriting:")

    elif state == 'ask_address':
        user_orders[user_id]['manzil'] = message.text
        order = user_orders[user_id]
        del user_states[user_id]
        sana = datetime.datetime.now().strftime("%Y-%m-%d")
        sheet.append_row([sana, order['mahsulot'], order['ism'], order['telefon'], order['manzil']])
        matn = (
            f"🛍 Buyurtma:\n"
            f"📦 Mahsulot: {order['mahsulot']}\n"
            f"👤 Ism: {order['ism']}\n"
            f"📞 Tel: {order['telefon']}\n"
            f"📍 Manzil: {order['manzil']}"
        )
        bot.send_message(user_id, "✅ Buyurtmangiz qabul qilindi!")
        bot.send_message(user_id, matn)

print("Bot ishga tushdi...")
bot.infinity_polling()


