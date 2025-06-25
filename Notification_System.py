import schedule
import time
from AI_Stock_Crypto_Indicator import run_ai_indicator, notification_system, build_email, send_alert

schedule.every(6).hours.do(notification_system)

while True:
    schedule.run_pending()
    time.sleep(60)