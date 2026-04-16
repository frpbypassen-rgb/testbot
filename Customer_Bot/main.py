import sys
import os
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import customer_bot

# استدعاء مباشر لكي يكشف لنا بايثون أي خطأ فوراً
import Customer_Bot.handlers.start_menu
import Customer_Bot.handlers.shop
import Customer_Bot.handlers.balance
import Customer_Bot.handlers.complaints
import Customer_Bot.handlers.recharge

print("✅ تم تحميل جميع أوامر وأزرار بوت العميل بنجاح.")

if __name__ == "__main__":
    print("🚀 بوت العملاء لشركة الأهرام قيد التشغيل...")
    try:
        customer_bot.infinity_polling(timeout=60, long_polling_timeout=20)
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف بوت العميل يدوياً.")
    except Exception as e:
        print("\n🚨 توقف بوت العميل بسبب خطأ فني:")
        traceback.print_exc()