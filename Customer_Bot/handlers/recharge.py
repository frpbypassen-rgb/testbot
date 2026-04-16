from config import customer_bot, db, users
from telebot import types
import datetime

cards_collection = db.recharge_cards


# --- 1. التقاط الضغطة من الأزرار العادية (الكيبورد) ---
@customer_bot.message_handler(func=lambda m: m.text in ["💳 شحن كارت", "شحن رصيد"])
def ask_for_code_msg(msg):
    trigger_recharge_prompt(msg.chat.id)

# --- 2. التقاط الضغطة من الزر الشفاف (الإنلاين) في قسم الحساب ---
@customer_bot.callback_query_handler(func=lambda call: call.data == "recharge_wallet")
def ask_for_code_call(call):
    customer_bot.answer_callback_query(call.id) # إخفاء علامة التحميل من الزر
    trigger_recharge_prompt(call.message.chat.id)

# --- 3. الدالة المشتركة التي تطلب الكود ---
def trigger_recharge_prompt(chat_id):
    res = customer_bot.send_message(
        chat_id, 
        "✍️ **يرجى إدخال كود الشحن الخاص بك:**\n*(انسخ الكود كما هو، مثلاً: AHRAM-XXXXXXXX)*", 
        parse_mode="Markdown"
    )
    customer_bot.register_next_step_handler(res, use_recharge_card)

# --- 4. معالجة الكود وتحديث الرصيد ---
def use_recharge_card(msg):
    code = msg.text.strip().upper()
    uid = msg.chat.id
    
    card = cards_collection.find_one({"code": code, "status": "active"})
    
    if not card:
        return customer_bot.send_message(uid, "❌ **عذراً، هذا الكود غير صحيح أو تم استخدامه مسبقاً.**")
    
    card_value = float(card.get('value', 0.0))
    
    # تحديث رصيد العميل
    users.update_one({"_id": uid}, {"$inc": {"balance": card_value}})
    
    # حرق الكارت
    cards_collection.update_one(
        {"code": code}, 
        {"$set": {
            "status": "used", 
            "used_by": uid, 
            "used_date": datetime.datetime.now()
        }}
    )
    
    customer_bot.send_message(
        uid, 
        f"✅ **تم شحن حسابك بنجاح!**\n💰 القيمة المضافة: `{card_value}` د.ل\n🔄 تم تحديث رصيدك، يمكنك الشراء الآن.",
        parse_mode="Markdown"
    )