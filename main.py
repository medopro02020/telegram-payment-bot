from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

BOT_TOKEN = '7862184684:AAGPD3jKKDp6xUUBg5ohHtpsXYtMTpYAvoI'
PAYMENT_LINK = 'https://www.paypal.com/ncp/payment/HY4D5R4427E4G'

async def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("💳 اضغط هنا للدفع", url=PAYMENT_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 أهلاً! للدفع اضغط الزر، ثم ابعتلي بعد الدفع.", reply_markup=reply_markup)

async def after_payment(update: Update, context: CallbackContext):
    await update.message.reply_text("✅ شكراً! ابعت صورة الدفع هنا، وسيتم التفعيل.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, after_payment))
print("✅ Bot is running...")
app.run_polling()
