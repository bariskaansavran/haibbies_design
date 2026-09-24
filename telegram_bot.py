import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Telegram Bot Token (Buraya eklenecek)
TOKEN = "TELEGRAM_BOT_TOKEN_BURAYA"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def load_catalog():
    try:
        with open('katalog_guncel.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "🌟 *Haibbies Design Yönetim Botuna Hoş Geldiniz!* 🌟\n\n"
        "Genel Müdür Asistanınız hazır. Güncel ürün kataloğunuzu görmek, "
        "fiyatlara bakmak veya satış linklerini almak için aşağıdaki butona tıklayın veya /katalog yazın."
    )
    
    keyboard = [[InlineKeyboardButton("📦 Kataloğu Getir", callback_data='show_catalog')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, parse_mode='Markdown', reply_markup=reply_markup)

async def send_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback=False):
    catalog = load_catalog()
    if not catalog:
        text = "Katalog şu an boş. Lütfen JSON dosyasını güncelleyin."
    else:
        text = "🔥 *GÜNCEL HAIBBIES DESIGN KATALOĞU* 🔥\n\n"
        for idx, item in enumerate(catalog, 1):
            title = item.get("title", "Ürün")
            price = item.get("price", "Fiyat Belirsiz")
            text += f"{idx}. *{title}* - {price} TL\n"
    
    if is_callback:
        await update.callback_query.message.reply_text(text, parse_mode='Markdown')
    else:
        await update.message.reply_text(text, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'show_catalog':
        await send_catalog(update, context, is_callback=True)

async def katalog_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_catalog(update, context)

if __name__ == '__main__':
    if TOKEN == "TELEGRAM_BOT_TOKEN_BURAYA":
        print("LUTFEN TELEGRAM_BOT_TOKEN_BURAYA KISMINI GÜNCELLEYİN!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("katalog", katalog_command))
        app.add_handler(CallbackQueryHandler(button_handler))
        
        print("Haibbies Design Telegram Botu Çalışıyor...")
        app.run_polling()
