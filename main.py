from telegram.ext import Updater, CommandHandler

TOKEN = "8506336833:AAHqTala7chpEiJJ2W1s6lSN5qgwdJpC5b8"

def start(update, context):
    update.message.reply_text("🤖 Bot is alive!")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

main()
