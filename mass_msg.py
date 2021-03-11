import pickledb
import telegram
import time

token = "1635198132:AAGddYiizcGA2kVAMFawNrFJmyyscX-K1Mw"
bot = telegram.Bot(token=token)
users = pickledb.load('users.db', True)
for user in users.getall():
    try:
        data = eval(users[user])
        bot.send_message(chat_id=str(data["chat_id"]), text="- Update -\n\nCoursehero has been updated to work more consistently, added support for Q&A on Coursehero.\n\nAs always check out cool stats with /stats or invite friends for free ad-supported unlocks (3 per hour). They have to use /gogators to enable this.\n\nContact me with suggestions or other sites you'd like to see on here @pixxllated")
        time.sleep(1)
    except Exception:
        print("failed " + user)