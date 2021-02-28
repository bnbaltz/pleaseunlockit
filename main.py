import pickledb
import random
import re
import requests
import telegram
import traceback
import uuid
from datetime import datetime, timedelta
from japronto import Application
from telegram.ext import CommandHandler, RegexHandler, Updater


token = "1635198132:AAGddYiizcGA2kVAMFawNrFJmyyscX-K1Mw"
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
users = pickledb.load('users.db', True)
chegg_data = pickledb.load('chegg_data.db', True)
questions = pickledb.load('question.db', True)
answers = pickledb.load('answer.db', True)
urls = pickledb.load('chegg_url.db', True)
orders = pickledb.load('orders.db', True)
px_auth = chegg_data.get("px_auth")
if not px_auth:
    px_auth = "3:f2f9cdae11aa972fea6fc75e177675552bb1eb1dbc5790a5d83cc2abeef0bcd7:txp8Stqk5ZX66+YIF8wg1ijngHmjJ/L4jBbBk87k9Nh2b85H1SUgqO4GuB3aIo2ieJeIr/Xtu+unau6H3Kxalg==:1000:WpFdWU+3bbPVC0xUM3kF7KYL9a7ra7OKfI2xLWJA1hijWLVEVR4OAEmslF42uDxBR1xl6Y2L9Mna9TCDJN0ZiU+7UeN7YXQ833vlOviEi0iVzeIF66c+Ag30xFyazRXvM9pUCsrJVehr//lVQOBw6UUSJsN+iVFlclR8m8ZVC/4="
    chegg_data.set("px_auth", px_auth)
refresh_token = chegg_data.get("refresh_token")
if not refresh_token:
    refresh_token = "ext.a0.t00.v1.MfZgogC5jFq629qgnYBtiCE-xH8onb_ptnJm6_KllJvBArvR0LY4tWXyZde7Su0pYfe5NdRoAdkDByHZ9rPLMHQ"
    chegg_data.set("refresh_token", refresh_token)
access_token = chegg_data.get("access_token")
if not access_token:
    access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhUTkU0cWwxNTRxekZieTBBakxDdSJ9.eyJodHRwczovL3Byb3h5LmNoZWdnLmNvbS9jbGFpbXMvYXBwSWQiOiJobERwWkFQRjA1bXFqQW1nN2NxdElLTE9oVXJ5QjhwMSIsImlzcyI6Imh0dHBzOi8vY2hlZ2ctcHJvZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8ZWQ0ZDYyMzUtOGJlNC00ZGI0LWIyZDItNTczYWNjMjAxNGZkIiwiYXVkIjpbImNoZWdnLW9pZGMiLCJodHRwczovL2NoZWdnLXByb2QudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYxNDIzMjQwNCwiZXhwIjoxNjE0MjMzODQ0LCJhenAiOiIzVFpiaGZzWndkZUhiaG9WTXhPdlpHYjM3TWN2YzBvOCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgYWRkcmVzcyBwaG9uZSBvZmZsaW5lX2FjY2VzcyIsImd0eSI6InBhc3N3b3JkIn0.g91q3Gzn5gvcmE9RsOP90rDkTiZIqx_d2ZG0SrP6h4Nu3yA9CZpTuRiCp51f8NYzxfkRu66Zy6JAhkdxu-7j_N3Cp8pBGzk7nBmIIPFYo_BVY_C7Tu5_D60jC78DLenhOg7BoSip_L1flmUSSyKvej_mRm0B5QC4hrVKSL0I8JX20X_oLAzcmFgUnbdfWiI6I5UIc_3xwboCB4HTE1iqVL4Fapei6RwZoZV0fNQAKYEBV17_2Dw6ZQld43PGnNGqoAcuzwmrJg7rIAVujxIef7Je9yauneVGrrjU7tN0Nvnz0D8GUWpxZohJ6_cXOwkwh0sblw9oFrCNGWA-hA_0hw"
    chegg_data.set("access_token", access_token)
user_id = chegg_data.get("user_id")
if not user_id:
    user_id = "ed4d6235-8be4-4db4-b2d2-573acc2014fd"
    chegg_data.set("user_id", user_id)
chegg_sesh = requests.Session()
venmo_sesh = requests.Session()
csite_sesh = requests.Session()
csite_sesh.headers = {
    'authority': 'www.chegg.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    'sec-fetch-dest': 'document',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'referer': 'https://www.google.com/',
    'accept-language': 'en-US,en;q=0.9',
}
sesh_id = str(uuid.uuid4())


def check_chegg_link(update, context):
    link = update.message.text
    username = update.message.from_user.username
    data = users.get(username)
    if not data:
        data = {
            "subscribed": False,
            "subscription_date": "",
            "credits": 0
        }
        users.set(username, set(data))
    else:
        data = eval(data)
    if not data["subscribed"]:
        if (data["credits"]) > 0:
            data["credits"] = int(data["credits"]) - 1
            users.set(username, str(data))
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="No active subscription or not enough credits to unlock! View /purchase to get started.")
            return
    else:
        expired = datetime.strptime(data["subscription_date"], '%m/%d/%Y') < datetime.now()
        if expired:
            data["subscribed"] = False
            data["subscription_date"] = ""
            users.set(username, set(data))
            context.bot.send_message(chat_id=update.effective_chat.id, text="No active subscription or not enough credits to unlock! View /purchase to renew or get started.")
            return
    i = 0
    while True:
        status = check_sesh()
        if not status:
            new_access = refresh_sesh()
            access_token = new_access["access_token"]
            refresh_token = new_access["refresh_token"]
            chegg_data.set("refresh_token", refresh_token)
            chegg_data.set("access_token", access_token)
            print("access token refreshed")
        else:
            print("access token still valid")
        question_id = check_question(link)
        if not question_id:
            return False
        formatted_html = get_question(question_id)
        if formatted_html == "answer_html":
            i += 1
            continue
        if not formatted_html or i == 2:
            return False
        order_id = str(uuid.uuid4())
        with open("/home/autobuy/html/" + order_id + ".html", "w+", encoding="utf-8") as html:
            html.write(formatted_html)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Deducted 1 credit, new balance: " + str(credit_avl) + "\n\nView here: https://pleaseunlock.it/q/" + order_id)
        return


def check_question(url):
    cleaned_url = url.split("/")[-1].split("?")[0].split("#")[0]
    already_found = urls.get(cleaned_url)
    if not already_found:
        print("fetching url")
        response = csite_sesh.get(url)
        try:
            question_id = re.search('pageNameDetailed":"(.*?)"', response.text).group(1)
        except Exception:
            print("url bad ? or banned")
            return False
        urls.set(cleaned_url, question_id)
        return question_id
    else:
        print("url was cached")
        return already_found


def check_sesh():
    refresh_globals()
    headers = {
        "X-CHEGG-USERID": user_id,
        "Authorization": "Basic aGxEcFpBUEYwNW1xakFtZzdjcXRJS0xPaFVyeUI4cDE6dUJqemFrbXhHeDZXdHFBcg==",
        "X-CHEGG-DEVICEID": "33c3f20d242f5bccfaea8993283dd8102e37ebd2",
        "X-CHEGG-SESSIONID": sesh_id,
        "access_token": access_token,
        "User-Agent": "Chegg Study/9.8.2 (Linux; U; Android 10; Pixel 3 XL Build/QQ1A.200105.003)",
        "X-ADOBE-MC-ID": "43643259243231378820218592977822332436",
        "x-chegg-dfid": "mobile|d0dd873f-70de-3f60-8994-2647e3133c75",
        "x-chegg-auth-mfa-supported": "true",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "X-NewRelic-ID": "UQYGUlNVGwQCVFJTBwcD"
    }
    data = {
        "asset": {
            "id": "1234567",
            "type": "QnA"
        },
        "client": "CS"
    }
    response = chegg_sesh.post("https://proxy.chegg.com/v1/access/_/has", headers=headers, json=data)
    print(response.text)
    return "ACCOUNT_OK" in response.text


def check_venmo_payment(_id, amount):
    headers = {
        "Authorization": "bearer f5685494c7fde0ec2769d6e3a8a79cb0640f9bfadd26bec747d1b97682e862ce",
        "User-Agent": "Venmo/8.16.1 Android/10 Google/Pixel 3 XL",
        "device-id": "5efd1a79-e02f-4206-8357-e4fce1e4794b",
        "X-Venmo-Android-Version-Name": "8.16.1",
        "X-Venmo-Android-Version-CODE": "2293",
        "application-id": "com.venmo",
        "Cache-Control": "max-age=0",
        "Accept-Language": "en-US",
        "Accept-Encoding": "gzip, deflate"
    }
    response = venmo_sesh.get("https://api.venmo.com/v1/stories/target-or-actor/3217037476233216746?limit=20", headers=headers)
    print(response.text)
    for payment in response.json()["data"]:
        if payment["note"] == _id and payment["payment"]["status"] == "settled" and float(payment["payment"]["amount"]) == amount:
            return True
    return False


def get_question(_id):
    already_found = questions.get(_id)
    if not already_found:
        headers = {
            "Accept": "application/vnd.chegg-odin.v1+json",
            "Authorization": "Basic aGxEcFpBUEYwNW1xakFtZzdjcXRJS0xPaFVyeUI4cDE6dUJqemFrbXhHeDZXdHFBcg==",
            "X-CHEGG-DEVICEID": "33c3f20d242f5bccfaea8993283dd8102e37ebd2",
            "X-CHEGG-SESSIONID": "786cdda5-8c17-4062-b804-3dafd989f1ed",
            "access_token": access_token,
            "User-Agent": "Chegg Study/9.8.2 (Linux; U; Android 10; Pixel 3 XL Build/QQ1A.200105.003)",
            "X-ADOBE-MC-ID": "43643259243231378820218592977822332436",
            "x-chegg-dfid": "mobile|d0dd873f-70de-3f60-8994-2647e3133c75",
            "x-chegg-auth-mfa-supported": "true",
            "Accept-Encoding": "gzip, deflate",
            "If-Modified-Since": "Thu, 25 Feb 2021 05:53:44 GMT",
            "X-NewRelic-ID": "UQYGUlNVGwQCVFJTBwcD"
        }
        response = chegg_sesh.get("https://proxy.chegg.com/v1/question/" + _id, headers=headers)
        try:
            print(response.text)
        except Exception:
            print("unicode error")
        question_data = response.json()                                                                                                                                                                                                                                      
        questions.set(_id, question_data)
        if question_data["result"]["statistics"]["answerCount"] > 0:
            response = chegg_sesh.get("https://proxy.chegg.com/v1/answer?f.questionUUIDs=" + _id + "&limit=10&offset=0", headers=headers)
            try:
                print(response.text)
            except Exception:
                print("unicode error")
            answer_data = response.json()
            answers.set(_id, answer_data)
        else:
            return False
    else:
        question_data = already_found
        answer_data = answers.get(_id)
        try:
            question_html = question_data["result"]["content"]["content"]
            answer_html = answer_data["result"][0]["content"]["content"]
        except Exception:
            headers = {
                "Accept": "application/vnd.chegg-odin.v1+json",
                "Authorization": "Basic aGxEcFpBUEYwNW1xakFtZzdjcXRJS0xPaFVyeUI4cDE6dUJqemFrbXhHeDZXdHFBcg==",
                "X-CHEGG-DEVICEID": "33c3f20d242f5bccfaea8993283dd8102e37ebd2",
                "X-CHEGG-SESSIONID": "786cdda5-8c17-4062-b804-3dafd989f1ed",
                "access_token": access_token,
                "User-Agent": "Chegg Study/9.8.2 (Linux; U; Android 10; Pixel 3 XL Build/QQ1A.200105.003)",
                "X-ADOBE-MC-ID": "43643259243231378820218592977822332436",
                "x-chegg-dfid": "mobile|d0dd873f-70de-3f60-8994-2647e3133c75",
                "x-chegg-auth-mfa-supported": "true",
                "Accept-Encoding": "gzip, deflate",
                "If-Modified-Since": "Thu, 25 Feb 2021 05:53:44 GMT",
                "X-NewRelic-ID": "UQYGUlNVGwQCVFJTBwcD"
            }
            response = chegg_sesh.get("https://proxy.chegg.com/v1/question/" + _id, headers=headers)
            try:
                print(response.text)
            except Exception:
                print("unicode error")
            question_data = response.json()                                                                                                                                                                                                                                                              
            questions.set(_id, question_data)
            if question_data["result"]["statistics"]["answerCount"] > 0:
                response = chegg_sesh.get("https://proxy.chegg.com/v1/question/" + _id + "/answers", headers=headers)
                try:
                    print(response.text)
                except Exception:
                    print("unicode error")
                answer_data = response.json()
                answers.set(_id, answer_data)
            else:
                return False
    question_html = question_data["result"]["content"]["content"]
    print(question_html)
    try:
        answer_html = answer_data["result"][0]["content"]["content"]
        print(answer_html)
    except Exception:
        return "answer_html"
    html = '''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=0, minimal-ui">
        <title>PleaseUnlockIT</title>
    </head>
    <body>
        <!-- header-bg -->
        <style type="text/css">
            .badge, .badge-timer {
            background-color: #F6F5F2;
            border-radius: .2rem;
            }
            .crypto-amount {
            padding: .1rem;
            border-radius: .3rem;
            background-color: #F6F5F2;
            }
            .qrcode {
            width: 100%;
            text-align: center;
            }
            canvas {
            background-color: #fff;
            border-radius: .3rem;
            padding: 1rem;
            }
            .info {
            padding: 1rem;
            background-color: #F6F5F2;
            border-radius: .4rem;
            }
        </style>
        <div class="wrapper" style="padding-top: 2rem !important">
            <div class="container-fluid">
                <!-- START ROW -->
                    <div class="card m-b-30">
                        <div class="card-body">
                            <h4>
                            <b>QUESTION:</b>
                            <br>
                            </h4>
                            <div class="mb-0" id="info">
                            <div class="row">
                                <div class="col-md-9">
                                    ''' + question_html + '''
                                </div>

                            </div>
                            </div>
                            <div class="mt-3 invoice-card">

                            <div id="details" class="mt-4 info">
                                <h4>
                                    <b>ANSWER:</b>
                                    <br>
                                </h4>
                                <div class="row">
                                    <div class="col">
                                        ''' + answer_html + '''
                                    </div>
                                </div>
                            </div>
                            </div>
                        </div>
                    </div>

                <!-- END ROW -->

                <!-- end container-fluid -->
            </div>
            <!-- end wrapper -->
        </div>

    </body>
    </html>
    '''
    return html


def refresh_globals():
    global access_token
    global refresh_token
    access_token = chegg_data.get("access_token")
    refresh_token = chegg_data.get("refresh_token")


def refresh_sesh():
    headers = {
        "Authorization": "Basic aGxEcFpBUEYwNW1xakFtZzdjcXRJS0xPaFVyeUI4cDE6dUJqemFrbXhHeDZXdHFBcg==",
        "X-PX-AUTHORIZATION": "3",
        "X-PX-ORIGINAL-TOKEN": px_auth,
        "X-CHEGG-DEVICEID": "33c3f20d242f5bccfaea8993283dd8102e37ebd2",
        "X-CHEGG-SESSIONID": sesh_id,
        "User-Agent": "Chegg Study/9.8.2 (Linux; U; Android 10; Pixel 3 XL Build/QQ1A.200105.003)",
        "X-ADOBE-MC-ID": "43643259243231378820218592977822332436",
        "x-chegg-dfid": "mobile|d0dd873f-70de-3f60-8994-2647e3133c75",
        "x-chegg-auth-mfa-supported": "true",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate",
        "X-NewRelic-ID": "UQYGUlNVGwQCVFJTBwcD"
    }
    data = {
        "refresh_token": refresh_token,
        "source_page": "android Study 9.8.2|cs",
        "grant_type": "refresh_token",
        "source_product": "android|cs"
    }
    response = chegg_sesh.post("https://proxy.chegg.com/oidc/token", headers=headers, data=data)
    print(response.text)
    return response.json()


def serve_static(request):
    try:
        q_id = request.match_dict["q_id"]
        if ".." in q_id or "/" in q_id:
            return request.Response(headers={"Location": "https://pleaseunlock.it"}, code=302)
        with open('/home/autobuy/html/' + q_id + '.html', 'r', encoding="utf-8") as html:
            return request.Response(text=html.read(), mime_type="text/html")
    except Exception:
        return request.Response(headers={"Location": "https://pleaseunlock.it"}, code=302)


def tele_purchase(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="We have two options available:\n\nCredits\n- 1 credit = 1 unlock\n- $0.15 each\n\nSubcription\n- Unlimited unlocks\n- $5 for 30 days access\n\nTo purchase use /venmo {number-of-credits} or /venmo sub, only venmo accepted at this time!")


def tele_chegg(update, context):
    username = update.message.from_user.username
    data = users.get(username)
    if not data:
        data = {
            "subscribed": False,
            "subscription_date": "",
            "credits": 0
        }
        users.set(username, set(data))
        context.bot.send_message(chat_id=update.effective_chat.id, text="- Account Status -\n\nSubscribed: " + str(data["subscribed"]) + "\nCredits: " + str(data["credits"]) + "\n\nTo purchase a subscription or credits use /purchase")
    else:
        data = eval(data)
        context.bot.send_message(chat_id=update.effective_chat.id, text="- Account Status -\n\nSubscribed: " + str(data["subscribed"]) + "\n" + ("Good until: " + data["subscription_date"] + "\n" if data["subscribed"] else "") + "Credits: " + str(data["credits"]) + "\n\n" + ("To unlock a Chegg answer, simply send the link and 1 credit will be deducted from your balance." if not data["subscribed"] else "To unlock a Chegg answer, simply send the link. You have unlimited unlocks."))


def tele_orders(update, context):
    order = update.message.text.replace('/', '').replace('o', '-')
    order_data = orders.get(order)
    if not order_data:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please contact @pixxllated, order not found!")
    else:
        try:
            data = eval(order_data)
            if data["status"] == "unpaid":
                resp = check_venmo_payment(order, float(data["price"]))
                if resp:
                    data["status"] = "paid"
                    username = update.message.from_user.username
                    user_data = users.get(username)
                    if not user_data:
                        user_data = {
                            "subscribed": False,
                            "subscription_date": "",
                            "credits": 0
                        }
                    else:
                        user_data = eval(user_data)
                    if data["type"] == "sub":
                        user_data["subscribed"] = True
                        user_data["subscription_date"] = (datetime.now() + timedelta(days=30)).strftime('%m/%d/%Y')
                    else:
                        user_data["credits"] += int(data["amt"])
                    users.set(username, str(user_data))
                    orders.set(order, str(data))
                    print("paid added credits")
                else:
                    print("not paid")
            context.bot.send_message(chat_id=update.effective_chat.id, text="Payment: " + data["payment"] + "\nType: " + str(data["type"]) + "\nStatus: " + data["status"])
        except Exception:
            print(traceback.format_exc())
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please contact @pixxllated, getting order data failed!")


def tele_start(update, context):
    if not update.message.from_user.username:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You must set a username to use this bot! Settings > Edit > Username")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to PleaseUnlockIt Homework Bot. Use /chegg to get started!")


def tele_venmo(update, context):
    data = {
        "payment": "venmo",
        "type": "",
        "status": "unpaid"
    }
    try:
        amount = int(context.args[0])
        data["type"] = "credit"
        data["amt"] = amount
        data["price"] = (amount * 0.2) - (int((amount / 25)) * 2.0)
    except Exception:
        if "sub" == context.args[0]:
            data["type"] = "sub"
            data["price"] = 5.0
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid argument!\nCredit example: /venmo 50\nSubscription example: /venmo sub")
            return
    order_id = str(random.randint(100,999)) + "-" + str(random.randint(100,999)) + "-" + str(random.randint(100,999))
    orders.set(order_id, str(data))
    context.bot.send_message(chat_id=update.effective_chat.id, text="Venmo $" + str(data["price"]) + " to @pleaseunlockit and set the note to " + order_id + ".\n\n Use /" + order_id.replace("-", "o") + " to check the status of your order.")
    


start_handler = CommandHandler('start', tele_start)
chegg_handler = CommandHandler('chegg', tele_chegg)
purchase_handler = CommandHandler('purchase', tele_purchase)
venmo_handler = CommandHandler('venmo', tele_venmo)
chegg_link_handler = RegexHandler('.*chegg\.com\/homework-help\/questions\-and\-answers.*', check_chegg_link)
order_handler = RegexHandler('[0-9]{3}o[0-9]{3}o[0-9]{3}', tele_orders)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(chegg_handler)
dispatcher.add_handler(purchase_handler)
dispatcher.add_handler(venmo_handler)
dispatcher.add_handler(order_handler)
dispatcher.add_handler(chegg_link_handler)
updater.start_polling()
app = Application()
app.router.add_route('/q/{q_id}', serve_static)
app.run(debug=True, host='127.0.0.1', port=8423)