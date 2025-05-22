
# Shodiyaxon Beauty Bot

This is a Telegram bot built for Shodiyaxon Beauty using Python, Google Sheets, and Telebot.

## 🧾 Features
- Display product categories
- Retrieve product details from Google Sheets
- Handles orders and returns responses based on category

## 📦 Requirements
- Python 3.11+
- Libraries listed in `requirements.txt`

## 🚀 Deploy on Render

### 1. Create a new Web Service
Go to https://dashboard.render.com and click **"New + → Web Service"**

### 2. Connect your GitHub repo

Choose the repository where you've uploaded:
- `shodiyaxon_bot_final.py`
- `requirements.txt`

### 3. Fill in Settings:

**Build Command:**  
```
pip install -r requirements.txt
```

**Start Command:**  
```
python shodiyaxon_bot_final.py
```

**Environment Variables:**  
Go to “Environment” tab and add:

```
KEY: TELEGRAM_TOKEN
VALUE: (your Telegram token)
```

```
KEY: GOOGLE_CREDENTIALS
VALUE: (paste the content from google_credentials_env.txt)
```

**Python Version (optional):**  
In `render.yaml` or manually choose 3.11.11

---

## ✅ Result
Your bot will be live and respond to Telegram users with product details from Google Sheets!

