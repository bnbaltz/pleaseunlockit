import pickledb
import telegram
import time

token = "1635198132:AAGddYiizcGA2kVAMFawNrFJmyyscX-K1Mw"
bot = telegram.Bot(token=token)
users = pickledb.load('users.db', True)
for user in users.getall():
    try:
        data = eval(users[user])
        bot.send_message(chat_id=str(data["chat_id"]), text="- Update -\n\nDatabase got corrupted if your subscription or credits isn't showing up contact me @pixxllated")
        time.sleep(1)
    except Exception:
        print("failed " + user)