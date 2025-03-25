import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, ChatMemberHandler

BOT_TOKEN = '7862184684:AAGPD3jKKDp6xUUBg5ohHtpsXYtMTpYAvoI'
PAYMENT_LINK = 'https://www.paypal.com/ncp/payment/HY4D5R4427E4G'

# PayPal API Credentials
PAYPAL_CLIENT_ID = "AUx8aZl2S9MWNF2bEUcAEMwufHP5F_AICCwi-my2oNMu8ju_goTWytZKff1TLPBlfR5WGemaQMUaCCvG"
PAYPAL_SECRET = "ELM-nbIbBDwWAEStEN9Uhk79o3tiG72A1i7vNIyLuzVjhOcVP7wLdIJUDWNrcmg41Ruj_UdQwCfen-3y"
PAYPAL_API_URL = "https://api.sandbox.paypal.com/v1/oauth2/token"

# دالة للحصول على Access Token من PayPal
def get_paypal_token():
    try:
        auth = (PAYPAL_CLIENT_ID, PAYPAL_SECRET)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'grant_type': 'client_credentials'}
        response = requests.post(PAYPAL_API_URL, auth=auth, data=data, headers=headers)

        # تحقق من استجابة PayPal
        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            print(f"Error getting token: {response.text}")
            return None
    except Exception as e:
        print(f"Error during PayPal token request: {e}")
        return None

# دالة للتحقق من الدفع باستخدام رقم المعاملة
def verify_payment(transaction_id):
    token = get_paypal_token()
    
    if not token:
        return False

    verify_url = f"https://api.sandbox.paypal.com/v1/payments/payment/{transaction_id}"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(verify_url, headers=headers)

        # تحقق من استجابة PayPal
        if response.status_code == 200:
            payment_data = response.json()
            if payment_data.get('state') == 'approved':
                return True
            else:
                print(f"Payment not approved: {payment_data}")
                return False
        else:
            print(f"Error verifying payment: {response.text}")
            return False
    except Exception as e:
        print(f"Error during PayPal payment verification: {e}")
        return False

# رسالة الترحيب مع زر الدفع
async def welcome_message(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("💳 اضغط هنا للدفع", url=PAYMENT_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 أهلاً وسهلاً! للدخول في الخدمة، برجاء الضغط على الزر والدفع أولاً، ثم أرسل رقم المعاملة هنا.",
        reply_markup=reply_markup
    )

# رد بعد الدفع والتحقق من المعاملة
async def after_payment(update: Update, context: CallbackContext):
    message = update.message.text
    transaction_id = message.strip()

    if verify_payment(transaction_id):
        await update.message.reply_text(
            "✅ تم التحقق من الدفع بنجاح! الخدمة مفعلة الآن."
        )
    else:
        await update.message.reply_text(
            "❌ لم يتم التحقق من الدفع. تأكد من أن الرقم صحيح أو حاول مرة أخرى."
        )

# إعداد البوت
app = ApplicationBuilder().token(BOT_TOKEN).build()

# إضافة معالجين:
# إضافة معالج لرسالة الترحيب في البداية للمستخدمين الجدد
app.add_handler(ChatMemberHandler(welcome_message, ChatMemberHandler.MY_CHAT_MEMBER))

# إضافة معالج عند كتابة أي رسالة نصية للتحقق من رقم المعاملة
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, after_payment))

# تشغيل البوت
print("✅ Bot is running...")
app.run_polling()
