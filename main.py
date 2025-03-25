from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

BOT_TOKEN = '7862184684:AAGPD3jKKDp6xUUBg5ohHtpsXYtMTpYAvoI'
PAYMENT_LINK = 'https://www.paypal.com/ncp/payment/HY4D5R4427E4G'

# رسالة الترحيب مع زر الدفع
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("💳 اضغط هنا للدفع", url=PAYMENT_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 أهلاً وسهلاً! للدخول في الخدمة، برجاء الضغط على الزر والدفع أولاً، ثم أرسل صورة الدفع أو رقم المعاملة هنا.",
        reply_markup=reply_markup
    )

# رد بعد الدفع
async def after_payment(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "✅ شكرًا على الدفع! ابعت صورة إيصال الدفع أو رقم المعاملة هنا ليتم التفعيل."
    )

# إعداد البوت
app = ApplicationBuilder().token(BOT_TOKEN).build()

# إضافة المعالجات
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, after_payment))

# تشغيل البوت
print("✅ Bot is running...")
app.run_polling()
