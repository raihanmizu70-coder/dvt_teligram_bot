from telegram import *
from telegram.ext import *
import os

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

users = {}
tasks = []
waiting = {}

def start(update, context):
    uid = update.effective_user.id
    users.setdefault(uid, {"balance":0,"task":0})
    kb = [["🧩 Tasks","💰 Balance"],["💸 Withdraw"]]
    update.message.reply_text(
        "🤖 DVT Task Bot",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True)
    )

def show_task(update, context):
    uid = update.effective_user.id
    i = users[uid]["task"]
    if i >= len(tasks):
        update.message.reply_text("✅ আজকের সব টাস্ক শেষ")
        return
    t = tasks[i]
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Open Link", url=t["link"])],
        [InlineKeyboardButton("📸 Submit Screenshot", callback_data="send")]
    ])
    update.message.reply_text(
        f"🧩 Task {i+1}\n{t['title']}\n💰 Reward: ৳{t['amount']}",
        reply_markup=kb
    )

def button(update, context):
    q = update.callback_query
    if q.data == "send":
        waiting[q.from_user.id] = True
        q.message.reply_text("📸 Screenshot পাঠাও")

def photo(update, context):
    uid = update.effective_user.id
    if uid not in waiting:
        return
    del waiting[uid]
    admin_kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"ok_{uid}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"no_{uid}")
        ]
    ])
    context.bot.send_photo(
        ADMIN_ID,
        update.message.photo[-1].file_id,
        caption=f"User: {uid}\nTask: {tasks[users[uid]['task']]['title']}",
        reply_markup=admin_kb
    )
    update.message.reply_text("⏳ Review এ গেছে")

def admin(update, context):
    q = update.callback_query
    if q.from_user.id != ADMIN_ID:
        return
    act, uid = q.data.split("_")
    uid = int(uid)
    if act == "ok":
        amt = tasks[users[uid]["task"]]["amount"]
        users[uid]["balance"] += amt
        users[uid]["task"] += 1
        context.bot.send_message(uid, f"✅ Approved +৳{amt}")
    else:
        context.bot.send_message(uid, "❌ Rejected")
    q.message.edit_reply_markup()

def balance(update, context):
    uid = update.effective_user.id
    update.message.reply_text(f"💰 Balance: ৳{users[uid]['balance']}")

def withdraw(update, context):
    uid = update.effective_user.id
    context.bot.send_message(ADMIN_ID, f"💸 Withdraw request from {uid}")
    update.message.reply_text("⏳ Withdraw request sent")

def main():
    tasks.append({
        "title":"CPA Signup",
        "link":"https://example.com",
        "amount":3
    })

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.regex("🧩 Tasks"), show_task))
    dp.add_handler(MessageHandler(Filters.regex("💰 Balance"), balance))
    dp.add_handler(MessageHandler(Filters.regex("💸 Withdraw"), withdraw))
    dp.add_handler(CallbackQueryHandler(button, pattern="send"))
    dp.add_handler(CallbackQueryHandler(admin, pattern="ok_|no_"))
    dp.add_handler(MessageHandler(Filters.photo, photo))

    updater.start_polling()
    updater.idle()

main()
