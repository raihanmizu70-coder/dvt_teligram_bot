from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

TOKEN = "YOUR_BOT_TOKEN"
ADMIN_ID = 123456789

def start(update, context):
    kb = [["🧩 Tasks"]]
    update.message.reply_text(
        "🤖 Bot Started Successfully",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True)
    )

def show_task(update, context):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Open Link", url="https://example.com")]
    ])
    update.message.reply_text(
        "🧩 Task 1\nVisit the link\nReward: 3৳",
        reply_markup=kb
    )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.regex("🧩 Tasks"), show_task))

    updater.start_polling()
    updater.idle()

main()
