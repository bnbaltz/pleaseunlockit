import pickledb
import random
import re
import requests
import telegram
import time
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
ch_db = pickledb.load('ch_ids.db', True)
mathway_db = pickledb.load('mathway_data.db', True)
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
mathway_sesh = requests.Session()
mathway_sesh.cookies = requests.utils.cookiejar_from_dict({
    'Mathway.IncomingCulture': 'en-US',
    'Mathway.Culture': 'en-US',
    'Mathway.GDPR': '1',
    'usprivacy': '1YNY',
    'al_cell': 'rio-3-test',
    '_ga': 'GA1.2.1404776111.1615004282',
    '_gid': 'GA1.2.1688984718.1615004282',
    'language': 'en_US',
    'amazon-pay-connectedAuth': 'connectedAuth_general',
    '_gd1615004282036': '1',
    'sbm_country': 'US',
    'Mathway.AnonUserId': '553849910',
    'Mathway.UpgradeGuaranteeTestVariant': '{%22testId%22:22%2C%22testVariantId%22:121}',
    'Mathway.QuarterlyTestVariant': '{%22testId%22:12%2C%22testVariantId%22:120}',
    'Mathway.OneOffPurchaseTestVariant': '{%22testId%22:13%2C%22testVariantId%22:101}',
    'Mathway.PlancodeTestVariant': '{%22testId%22:1%2C%22testVariantId%22:116}',
    'Mathway.StaticAdsTest': '{%22testId%22:33%2C%22testVariantId%22:151}',
    'Mathway.AnonymousPurchasing': '{%22testId%22:29%2C%22testVariantId%22:133}',
    'Mathway.CreditPackPurchasingTestVariant': '{%22testId%22:18%2C%22testVariantId%22:129}',
    'mcid': '36179880738755767140875923447029603383',
    '_gd1615004294789': '1',
    'G_ENABLED_IDPS': 'google',
    '_gd1615004390172': '1',
    '_gd1615090060012': '1',
    'Mathway.Location': 'US',
    '_gd1615091451594': '1',
    'apay-session-set': 'MoHhZJkrcsy7RyX7fzvgCSajpFgpfGt6vQGbXT2VVmXzXfKncC0wv%2BRNdFVo5m8%3D',
    'Mathway.LastSubject': 'BasicMath',
    '_gd1615091715278': '1',
    '_gd1615093630032': '1',
    'OptanonConsent': 'isIABGlobal=false&datestamp=Sun+Mar+07+2021+00%3A07%3A10+GMT-0500+(Eastern+Standard+Time)&version=6.13.0&hosts=&consentId=698f4873-88bd-4662-84a7-79c93989b461&interactionCount=1&landingPath=NotLandingPage&groups=snc%3A1%2Cfnc%3A1%2Cprf%3A1%2CSPD_BG%3A1%2Ctrg%3A1%2Cgoog%3A1&AwaitingReconsent=false',
}
)
ch_sesh = requests.Session()
ch_sesh.headers = {
    'Authorization': 'Bearer MWI0NGFhZTJkMGM0MWNmOTlkMmMzZGEyN2Y3N2VhNDM4ZTNmOGM4MDAxMjUxMTBlZDUwMTQxMWQ5ZWNkZjhmOQ',
    'CH-DEVICE-ID': '3DF1F68C-1C1C-4FD0-8AEC-5A9CEEE62ECA',
    'Accept': '*/*',
    'User-Agent': 'Course Hero/1.9.88 (iPhone; iOS 14.1; Scale/3.00)',
    'Accept-Language': 'en-US;q=1',
    'Accept-Encoding': 'gzip, deflate'
}
venmo_sesh = requests.Session()
csite_sesh = requests.Session()
csite_sesh.cookies = requests.utils.cookiejar_from_dict({
    '_scid': '1b70a5f6-676c-4b63-a461-f220d7168646',
    'sbm_mcid': '36179880738755767140875923447029603383',
    'sbm_dma': '592',
    'sbm_sbm_id': '0100007F3045665F3E00244B021FDF09',
    'sbm_country': 'US',
    'sbm_gaid': '1504791017.1586974241',
    'bc.visitorToken': '6713556041797529600',
    'C': '0',
    'O': '0',
    'U': '0',
    'V': '4183c8c9020254b290daafa343bef49a6036ec438da5e1.23463641',
    's_ecid': 'MCMID%7C36179880738755767140875923447029603383',
    'usprivacy': '1YNY',
    'optimizelyEndUserId': 'oeu1614212164613r0.354684859863007',
    '_pxvid': 'a6364472-76fe-11eb-aee5-0242ac120007',
    '_omappvp': 'UfBknmOtzxdRSdxqpXOr0wmWgcChq1dh8orxbC0dCMh4L67haYriio54OqBe5XnbGatgHh8YjQ2Ia9Hxlz5yWisQxhGwmawz',
    'aam_tnt': 'aam%3D2053348',
    'aam_uuid': '36196819364072191200876507352774590477',
    '_ga': 'GA1.2.1092619508.1614212165',
    '_cs_c': '1',
    '_rdt_uuid': '1614212165608.e6e43793-7fa2-4fc2-aab9-7b7c1a6c0680',
    '_fbp': 'fb.1.1614212165661.1693932998',
    '_gcl_au': '1.1.484559615.1614212166',
    'adobeujs-optin': '%7B%22aam%22%3Atrue%2C%22adcloud%22%3Atrue%2C%22aa%22%3Atrue%2C%22campaign%22%3Atrue%2C%22ecid%22%3Atrue%2C%22livefyre%22%3Atrue%2C%22target%22%3Atrue%2C%22mediaaa%22%3Atrue%7D',
    'WRUID': '3180818695455217',
    '_ym_uid': '1614212166458184490',
    '_ym_d': '1614212166',
    'LPVID': 'I5NjJhM2E0ODU1NGMyMjYx',
    'aamsc': 'aam%3D2053348%2Caam%3D2756555%2Caam%3D5674360',
    '_sctr': '1|1614574800000',
    'exp': 'A184B%7CA311C%7CA803B%7CC024A%7CA560B%7CA294A',
    'PHPSESSID': '03721aeb2c00c0dba89a2eeff77313fe',
    'user_geo_location': '%7B%22country_iso_code%22%3A%22US%22%2C%22country_name%22%3A%22United+States%22%2C%22region%22%3A%22FL%22%2C%22region_full%22%3A%22Florida%22%2C%22city_name%22%3A%22Gainesville%22%2C%22postal_code%22%3A%2232601%22%2C%22locale%22%3A%7B%22localeCode%22%3A%5B%22en-US%22%5D%7D%7D',
    'AMCVS_3FE7CBC1556605A77F000101%40AdobeOrg': '1',
    'mcid': '36179880738755767140875923447029603383',
    '_sdsat_authState': 'Logged%20Out',
    'expkey': 'C698D12BFA7D742172BAEEF05F5A7E7E',
    'CSessionID': '471a1e7b-75c4-4838-8a46-63f63c260b7f',
    '_gid': 'GA1.2.463715929.1615160397',
    'intlPaQExitIntentModal': 'hide',
    '_CT_RS_': 'Recording',
    'AMCV_3FE7CBC1556605A77F000101%40AdobeOrg': '-408604571%7CMCIDTS%7C18694%7CMCMID%7C36179880738755767140875923447029603383%7CMCAAMLH-1615779159%7C7%7CMCAAMB-1615779159%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1615181559s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.6.0',
    'LPSID-51961742': 'scTs80_FRT-ODiUtemtp_g',
    'schoolapi': 'd4237307-b516-450d-b621-528a65e8a462|0.901408451',
    '_cs_cvars': '%7B%221%22%3A%5B%22Page%20Name%22%2C%22Question%20Page%22%5D%2C%222%22%3A%5B%22Experience%22%2C%22desktop%22%5D%2C%223%22%3A%5B%22Page%20Type%22%2C%22pdp%22%5D%2C%224%22%3A%5B%22Auth%20Status%22%2C%22Logged%20Out%22%5D%7D',
    '_pxff_cc': 'U2FtZVNpdGU9TGF4Ow==',
    '_sdsat_highestContentConfidence': '{%22course_uuid%22:%2214e46fb9-e09e-406c-ac7d-3e332a35052f%22%2C%22course_name%22:%22heat-transfer-thermodynamics%22%2C%22confidence%22:0.7698%2C%22year_in_school%22:%22college-year-3%22%2C%22subject%22:[{%22uuid%22:%22ed065c84-79f2-4813-bbcf-13b75dda2abc%22%2C%22name%22:%22mechanical-engineering%22}]}',
    'OptanonConsent': 'isIABGlobal=false&datestamp=Sun+Mar+07+2021+23%3A52%3A51+GMT-0500+(Eastern+Standard+Time)&version=6.10.0&hosts=&consentId=6f97243c-b4c1-43e2-baba-45f3bd0010b8&interactionCount=1&landingPath=NotLandingPage&groups=snc%3A1%2Cfnc%3A1%2Cprf%3A1%2CSPD_BG%3A1%2Ctrg%3A1&AwaitingReconsent=false',
    '_uetsid': '6c98acd07f9e11eba363e1153a0c1368',
    '_uetvid': 'a6a730d076fe11ebab8ccb32cc5566d9',
    '_gat': '1',
    '_cs_id': '68673973-392f-ac1c-cebf-78dce8e86d3b.1614212165.17.1615179171.1615177013.1.1648376165840.Lax.0',
    '_cs_s': '9.1',
    '__CT_Data': 'gpv=42&ckp=tld&dm=chegg.com&apv_79_www33=42&cpv_79_www33=42&rpv_79_www33=4',
    's_pers': '%20buFirstVisit%3Dcore%252Ccs%252Chelp%7C1772770846520%3B%20gpv_v6%3Dchegg%257Cweb%257Ccs%257Cqa%257Cquestion%2520page%7C1615180973193%3B',
    's_sess': '%20buVisited%3Dcs%252Chelp%3B%20s_sq%3D%3B%20s_ptc%3D%3B%20cheggCTALink%3Dfalse%3B%20SDID%3D683335B142F74F2B-388BF20B8E8A0868%3B%20s_cc%3Dtrue%3B',
    '_pxff_rf': '1',
    '_pxff_fp': '1',
    '_px3': 'a8cfb872af9f38b30ea18cdbba55b436fc57623064e0c49229ee8d51e09571b7:ADyzIPpJVee90+OUqyZjXPDyYHhn9fIZzLB12fiTe+vNN6w91BJlpxtZJRsIiDuc5iXVdDnvQJjITqqGVjhhKg==:1000:eN8N4YPn14M2ldlNxWP7bFwDTl/2dge7B42liO4ojsaJU4E84vo1PGb8PXKkdoHu9/0jrARl2IkNPhuP8LwLqhheUHmhn+TnJ0WDzuHWJgH0825Flm3EhfQKKZ4L2JB/zj+ycFOnFerzhozhnHmyzPYA6jkqI5Iozm7UGBxWE+k=',
    '_px': 'ADyzIPpJVee90+OUqyZjXPDyYHhn9fIZzLB12fiTe+vNN6w91BJlpxtZJRsIiDuc5iXVdDnvQJjITqqGVjhhKg==:1000:LJIbAmkpApvTZnsQZlgUwDAmze9YObPfOqUMe7qT0Ck9721R3rV1bcbzaHbfGWq+g1aCVE3UBWfm+d274V0ZoyBkFirv44umuBQ5BmFT6seqRz03X2VJWrBX9GBj56oJEmPYtPzvmwhQCanfiCv1g37GutfkAN6gFTqz21EitEdGcF+h0NeiFKxjyzb8WGVlywUJG4YLL16jvPUzKWaxGji62rXtjClMvIfgzrwgfrIkPzuHGwZgAbwt/VMD2fOdwVuf1fUM5N+AEzv7qbqzOw==',
}
)
csite_sesh.headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'en-US,en;q=0.9',
}
sesh_id = str(uuid.uuid4())


def check_chegg_link(update, context):
    link = update.message.text
    username = update.message.from_user.username
    if not username:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You must set a username to use this bot! Settings > Edit > Username")
        return
    data = users.get(username)
    gator = False
    if not data:
        data = {
            "subscribed": False,
            "subscription_date": "",
            "credits": 0,
            "chat_id": update.effective_chat.id
        }
        users.set(username, str(data))
    else:
        data = eval(data)
    credit_used = False
    if not data["subscribed"]:
        if (data["credits"]) > 0:
            data["credits"] = int(data["credits"]) - 1
            data["chat_id"] = update.effective_chat.id
            users.set(username, str(data))
            credit_used = True
        else:
            try:
                data["go"]
                gator = True
                minutes_ago = data["last_unlock"]
                if minutes_ago != "never":
                    last_unlock = datetime.strptime(minutes_ago, "%Y-%m-%d %H:%M")
                    now = datetime.now()
                    minutes_ago = round((now - last_unlock).total_seconds() / 60.0)
                    if minutes_ago < 30:
                        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry you need to wait " + str(30 - minutes_ago) + " more minute(s) or consider /purchase.")
                        data["chat_id"] = update.effective_chat.id
                        users.set(username, str(data))
                        return
            except Exception:
                context.bot.send_message(chat_id=update.effective_chat.id, text="No active subscription or not enough credits to unlock! View /purchase to get started.")
                return
    else:
        expired = datetime.strptime(data["subscription_date"], '%m/%d/%Y') < datetime.now()
        if expired:
            data["subscribed"] = False
            data["subscription_date"] = ""
            data["chat_id"] = update.effective_chat.id
            users.set(username, str(data))
            context.bot.send_message(chat_id=update.effective_chat.id, text="No active subscription or not enough credits to unlock! View /purchase to renew or get started.")
            return
        else:
            data["chat_id"] = update.effective_chat.id
            users.set(username, str(data))
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
        if question_id == "no_answer":
            context.bot.send_message(chat_id=update.effective_chat.id, text="No answer available for this question! Did not burn an unlock.")
            if credit_used:
                data["credits"] = int(data["credits"]) + 1
                users.set(username, str(data))
            return
        while True:
            try:
                formatted_html = get_question(question_id)
            except Exception:
                time.sleep(1)
                context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to get answer, trying again..")
            else:
                break
        if formatted_html == "answer_html":
            i += 1
            continue
        if not formatted_html or i == 2:
            return False
        order_id = str(uuid.uuid4())
        with open("/home/autobuy/html/" + order_id + ".html", "w+", encoding="utf-8") as html:
            html.write(formatted_html)
        if gator:
            data["last_unlock"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            users.set(username, str(data))
            context.bot.send_message(chat_id=update.effective_chat.id, text="Go gators!")
        context.bot.send_message(chat_id=update.effective_chat.id, text="View here: https://pleaseunlock.it/q/" + order_id)
        return


def check_coursehero_unlocks():
    response = ch_sesh.get("https://www.coursehero.com/api/v1/users/unlocks/uploads/")
    try:
        return response.json()["unlocks_remaining"] > 0
    except Exception:
        print("prob expired auth")
        return False


def check_coursehero_link(update, context):
    link = update.message.text
    _id = re.search('file/(.*?)/', link).group(1)
    username = update.message.from_user.username
    if not username:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You must set a username to use this bot! Settings > Edit > Username")
        return
    data = users.get(username)
    gator = False
    if not check_coursehero_unlocks():
        context.bot.send_message(chat_id=update.effective_chat.id, text="Out of Coursehero unlocks, contact @pixxllated. You were not charged.")
        return
    if not data:
        data = {
            "subscribed": False,
            "subscription_date": "",
            "credits": 0,
            "chat_id": update.effective_chat.id
        }
        users.set(username, str(data))
    else:
        data = eval(data)
    if (data["credits"]) > 9:
        data["credits"] = int(data["credits"]) - 10
        data["chat_id"] = update.effective_chat.id
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Not enough credits to unlock! View /purchase to get started.")
        return
    response = ch_sesh.post("https://www.coursehero.com/api/v1/users/unlocks/content/document/id/" + _id + "/")
    if response.json()["success"] == "true":
        response = ch_sesh.get("https://www.coursehero.com/api/v2/documents/" + _id + "/pdf/")
        pdf = requests.get(response.json()["url"])
        file_name = str(uuid.uuid4()) + ".pdf"
        output_file = open("/home/autobuy/html/" + file_name, "wb")
        output_file.write(pdf.content)
        output_file.close()
        ch_db.set(_id, file_name)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to get your document, please contact @pixxllated. You were not charged.")
        return
    response = ch_sesh.post("https://www.coursehero.com/api/v1/documents/" + _id + "/like/")
    print(response.text)
    users.set(username, str(data))
    context.bot.send_message(chat_id=update.effective_chat.id, text="Download here: https://pleaseunlock.it/ch/" + file_name)


def check_question(url):
    cleaned_url = url.split("/")[-1].split("?")[0].split("#")[0]
    already_found = urls.get(cleaned_url)
    if not already_found:
        print("fetching url")
        response = csite_sesh.get(url)
        if "this question hasn" in response.text:
            return "no_answer"
        try:
            question_id = re.search('pageNameDetailed":"(.*?)"', response.text).group(1) # suprisingly works for textbook & regular
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


def check_textbook_link(update, context):
    link = update.message.text
    username = update.message.from_user.username
    if not username:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You must set a username to use this bot! Settings > Edit > Username")
        return
    data = users.get(username)
    gator = False
    if not data:
        data = {
            "subscribed": False,
            "subscription_date": "",
            "credits": 0
        }
        users.set(username, str(data))
    else:
        data = eval(data)
    if not data["subscribed"]:
        if (data["credits"]) > 0:
            data["credits"] = int(data["credits"]) - 1
            users.set(username, str(data))
        else:
            try:
                data["go"]
                gator = True
                minutes_ago = data["last_unlock"]
                if minutes_ago != "never":
                    last_unlock = datetime.strptime(minutes_ago, "%Y-%m-%d %H:%M")
                    now = datetime.now()
                    minutes_ago = round((now - last_unlock).total_seconds() / 60.0)
                    if minutes_ago < 30:
                        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry you need to wait " + str(30 - minutes_ago) + " more minute(s) or consider /purchase.")
                        return
            except Exception:
                context.bot.send_message(chat_id=update.effective_chat.id, text="No active subscription or not enough credits to unlock! View /purchase to get started.")
                return
    else:
        expired = datetime.strptime(data["subscription_date"], '%m/%d/%Y') < datetime.now()
        if expired:
            data["subscribed"] = False
            data["subscription_date"] = ""
            users.set(username, str(data))
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
        formatted_html = get_question_textbook(question_id)
        order_id = str(uuid.uuid4())
        with open("/home/autobuy/html/" + order_id + ".html", "w+", encoding="utf-8") as html:
            html.write(formatted_html)
        if gator:
            data["last_unlock"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            users.set(username, str(data))
            context.bot.send_message(chat_id=update.effective_chat.id, text="Go gators!")
        context.bot.send_message(chat_id=update.effective_chat.id, text="View here: https://pleaseunlock.it/q/" + order_id)
        return


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


def clean_headers(h):
    h["Host"] = None
    h["Cf-Ipcountry"] = None
    h["X-Forwarded-For"] = None
    h["Cf-Ray"] = None
    h["Cf-Visitor"] = None
    h["Origin"] = "https://mathway.com"
    h["Referer"] = "https://mathay.com/BasicMath"
    h["Cf-Connecting-Ip"] = None
    h["Cf-Request-Id"] = None
    h["Cdn-Loop"] = None
    return h


def get_question(_id):
    already_found = questions.get(_id)
    refresh_globals()
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


def get_question_textbook(_id):
    already_found = questions.get(_id)
    refresh_globals()
    if not already_found:
        isbn, problem_id = _id.split("-")
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
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "X-NewRelic-ID": "UQYGUlNVGwQCVFJTBwcD"
        }
        data = {
            "problemId": problem_id,
            "isbn13": isbn,
            "userAgent": "Mobile"
        }
        response = chegg_sesh.post("https://proxy.chegg.com/v1/tbs/_/solution", headers=headers, json=data)
        try:
            print(response.text)
        except Exception:
            print("unicode error")
        print(data)
        question_data = response.json()
        steps = question_data["result"]["solutions"][0]["steps"]
        step_html = []
        for step in steps:
            headers = {
                "x-chegg-dfid": "mobile|d0dd873f-70de-3f60-8994-2647e3133c75",
                "x-chegg-auth-mfa-supported": "true",
                "Accept-Encoding": "gzip, deflate",
                "User-Agent": "okhttp/4.4.0",
                "X-NewRelic-ID": "UQYGUlNVGwQCVFJTBwcD"
            }
            response = chegg_sesh.get(step["link"], headers=headers)
            step_html.append(response.text)
        questions.set(_id, question_data)
        answers.set(_id, step_html)
    else:
        step_html = answers.get(_id)
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
                                    Question ID: ''' + _id + '''
                                </div>

                            </div>
                            </div>
                            <div class="mt-3 invoice-card">

                            <div id="details" class="mt-4 info">
                                <h4>
                                    <b>ANSWER:</b>
                                    <br>
                                </h4>
                                <div class="row"> '''
    for step in step_html:
        html += '''<div class="col">''' + step + '''</div>'''
    html += '''</div>
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


def load_images(request):
    file_name = request.match_dict["file"]
    if (".png" not in file_name and ".jpg" not in file_name) or ".." in file_name or "/" in file_name:
        # attempted injection
        pass
    try:
        with open('/home/autobuy/images/' + file_name, 'rb') as img:
            return request.Response(body=img.read(), mime_type='image/png')
    except Exception:
        return request.Response(headers={"Location": "https://pleaseunlock.it"}, code=302)


def load_css(request):
    file_name = request.match_dict["file"]
    if (".css" not in file_name and ".js" not in file_name) or ".." in file_name or "/" in file_name:
        # attempted injection
        pass
    try:
        with open('/home/autobuy/css/' + file_name) as stylesheet:
            return request.Response(text=stylesheet.read(), mime_type='text/css')
    except Exception:
        return request.Response(headers={"Location": "https://pleaseunlock.it"}, code=302)


def load_js(request):
    file_name = request.match_dict["file"]
    if ".js" not in file_name or ".." in file_name or "/" in file_name:
        # attempted injection
        pass
    try:
        with open('/home/autobuy/js/' + file_name, encoding="utf-8") as script:
            return request.Response(text=script.read(), mime_type='text/javascript')
    except Exception:
        print(traceback.format_exc())
        return request.Response(headers={"Location": "https://pleaseunlock.it"}, code=302)


def load_fonts(request):
    file_name = request.match_dict["file"]
    if ".otf" not in file_name or ".." in file_name or "/" in file_name:
        # attempted injection
        pass
    try:
        with open('/home/autobuy/fonts/' + file_name.split("?")[0], 'rb') as font:
            return request.Response(body=font.read(), mime_type='font/opentype')
    except Exception:
        print(traceback.format_exc())
        return request.Response(headers={"Location": "https://pleaseunlock.it"}, code=302)


def mathway_request(url, json, headers):
    print(url)
    print(json)
    new_headers = headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'tok': headers["Tok"],
        'X-Requested-With': 'XMLHttpRequest',
        'Authorization': 'null',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Content-Type': 'application/json',
        'Origin': 'https://www.mathway.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.mathway.com/BasicMath',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    response = mathway_sesh.post(url, headers=new_headers, json=json)
    print(response.text)
    return response.text


def refresh_globals():
    global access_token
    global refresh_token
    chegg_data._loaddb()
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


def serve_clicksteps(request):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Content-Type': 'application/json',
        'Origin': 'https://www.mathway.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.mathway.com/BasicMath',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    response = mathway_sesh.post("https://www.mathway.com/chat/clickViewSteps", headers=headers, json=request.json)
    print(response.text)
    return request.Response(text=response.text)


def serve_editor(request):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Content-Type': 'application/json',
        'Origin': 'https://www.mathway.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.mathway.com/BasicMath',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    response = mathway_sesh.post("https://www.mathway.com/chat/editor", headers=headers, json=request.json)
    unlocks = int(mathway_db.get("unlocks"))
    unlocks += 1
    mathway_db.set("unlocks", str(unlocks))
    print(response.text)
    return request.Response(text=response.text)


def serve_greeting(request):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Content-Type': 'application/json',
        'Origin': 'https://www.mathway.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.mathway.com/BasicMath',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    print(request.json)
    response = mathway_sesh.post("https://www.mathway.com/chat/greeting", headers=headers, json=request.json)
    print(response.text)
    return request.Response(text=response.text)


def serve_inject(request):
    token = mathway_db.get("token")
    with open('/home/autobuy/js/inject.js', 'r', encoding="utf-8") as script:
        return request.Response(text=script.read().replace("REPLACETOKEN", token), mime_type='text/javascript')


def serve_keyboards(request):
    print(request.match_dict["board"])
    response = mathway_sesh.get('https://www.mathway.com/json/keyboard/' + request.match_dict["board"])
    print(response.text)
    return request.Response(text=response.text)


def serve_localapi(request):
    path = request.match_dict["path"]
    json  = {"tests":[{"testId":1,"testVariantId":116,"value":"monthly-premium-5|9.99","value2":"annual-premium-4|39.99","value3":"monthly-premium-tutoring-5|29.99","value4":"annual-premium-tutoring|149.99","value5":"quarterly-premium|19.99","value6":"quarterly-premium-tutoring|79.99","value7":"monthly-premium-expertqa|14.99","value8":"quarterly-premium-expertqa|29.99","value9":"annual-premium-expertqa|59.90"},{"testId":13,"testVariantId":101,"value":"off","value2":"","value3":"","value4":"","value5":"","value6":"","value7":"","value8":"","value9":""},{"testId":12,"testVariantId":120,"value":"off","value2":"","value3":"","value4":"","value5":"","value6":"","value7":"","value8":"","value9":""},{"testId":22,"testVariantId":121,"value":"off","value2":"","value3":"","value4":"","value5":"","value6":"","value7":"","value8":"","value9":""},{"testId":18,"testVariantId":129,"value":"off","value2":"","value3":"","value4":"","value5":"","value6":"","value7":"","value8":"","value9":""},{"testId":29,"testVariantId":133,"value":"off","value2":"","value3":"","value4":"","value5":"","value6":"","value7":"","value8":"","value9":""},{"testId":33,"testVariantId":151,"value":"p4-chat-and-left","value2":"","value3":"","value4":"","value5":"","value6":"","value7":"","value8":"","value9":""}],"status":1,"message":"Success","messageId":0}
    return request.Response(text=str(json))


def serve_localapiuser(request):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'tok': request.headers["Tok"],
        'X-Requested-With': 'XMLHttpRequest',
        'Authorization': 'null',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Content-Type': 'application/json',
        'Origin': 'https://www.mathway.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.mathway.com/BasicMath',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    response = mathway_sesh.post("https://www.mathway.com/localapiuser/rest/refreshUserStateAuth/", headers=headers, json=request.json)
    mathway_db.set("token", response.json()["userState"]["token"])
    print(response.text)
    return request.Response(text=response.text)


def serve_mathway_landing(request):
    return request.Response(headers={"Location": "https://pleaseunlock.it/mathway/BasicMath"}, code=302)


def serve_topics(request):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Content-Type': 'application/json',
        'Origin': 'https://www.mathway.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.mathway.com/BasicMath',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    response = mathway_sesh.post("https://www.mathway.com/chat/topics", headers=headers, json=request.json)
    print(response.text)
    return request.Response(text=response.text)


def serve_viewsteps(request):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Authorization': request.headers["Authorization"],
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Content-Type': 'application/json',
        'Origin': 'https://www.mathway.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Tok': request.headers["Tok"],
        'Referer': 'https://www.mathway.com/BasicMath',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    response = mathway_sesh.post("https://www.mathway.com/chat/viewSteps", headers=headers, json=request.json)
    print(response.text)
    return request.Response(text=response.text)


def serve_mathway(request):
    try:
        kind = request.match_dict["kind"]
    except Exception:
        kind = "BasicMath"
    with open('/home/autobuy/mathway/' + kind + '.html', 'r', encoding="utf-8") as html:
        return request.Response(text=html.read(), mime_type="text/html")


def serve_pdf(request):
    try:
        q_id = request.match_dict["q_id"]
        if ".." in q_id or "/" in q_id or ".pdf" not in q_id:
            return request.Response(headers={"Location": "https://pleaseunlock.it"}, code=302)
        with open('/home/autobuy/html/' + q_id, 'rb') as pdf:
            return request.Response(body=pdf.read())
    except Exception:
        return request.Response(headers={"Location": "https://pleaseunlock.it"}, code=302)


def serve_static(request):
    try:
        q_id = request.match_dict["q_id"]
        if ".." in q_id or "/" in q_id:
            return request.Response(headers={"Location": "https://pleaseunlock.it"}, code=302)
        with open('/home/autobuy/html/' + q_id + '.html', 'r', encoding="utf-8") as html:
            return request.Response(text=html.read(), mime_type="text/html")
    except Exception:
        return request.Response(headers={"Location": "https://pleaseunlock.it"}, code=302)


def tele_add(update, context):
    username = context.args[0]
    data = users.get(username)
    if not data:
        data = {
            "subscribed": False,
            "subscription_date": "",
            "credits": 0
        }
    else:
        data = eval(data)
    type_ = context.args[1]
    if type_ == "credit":
        data["credits"] = int(data["credits"]) + int(context.args[2])
    elif type_ == "sub":
        data["subscribed"] = True
        data["subscription_date"] = (datetime.now() + timedelta(days=30)).strftime('%m/%d/%Y')
    users.set(username, str(data))
    context.bot.send_message(chat_id=update.effective_chat.id, text="Operation success!")


def tele_chegg(update, context):
    username = update.message.from_user.username
    data = users.get(username)
    if not data:
        data = {
            "subscribed": False,
            "subscription_date": "",
            "credits": 0,
            "chat_id": update.effective_chat.id
        }
        users.set(username, str(data))
        context.bot.send_message(chat_id=update.effective_chat.id, text="- Account Status -\n\nSubscribed: " + str(data["subscribed"]) + "\nCredits: " + str(data["credits"]) + "\n\nTo purchase a subscription or credits use /purchase or contact @pixxllated for 1 free unlock.")
    else:
        data = eval(data)
        try:
            data["go"]
            minutes_ago = data["last_unlock"]
            if minutes_ago != "never":
                last_unlock = datetime.strptime(minutes_ago, "%Y-%m-%d %H:%M")
                now = datetime.now()
                minutes_ago = round((now - last_unlock).total_seconds() / 60.0)
            context.bot.send_message(chat_id=update.effective_chat.id, text="- Account Status -\n\nSubscribed: " + str(data["subscribed"]) + "\nLast unlock: " + str(minutes_ago) + (" min ago" if minutes_ago != "never" else "") + "\nCredits: " + str(data["credits"]) + "\n\nTo unlock a Chegg simply send the link, you have one unlock every 30 minutes.")
        except Exception:
            context.bot.send_message(chat_id=update.effective_chat.id, text="- Account Status -\n\nSubscribed: " + str(data["subscribed"]) + "\n" + ("Good until: " + data["subscription_date"] + "\n" if data["subscribed"] else "") + "Credits: " + str(data["credits"]) + "\n\n" + ("To unlock a Chegg answer, simply send the link and 1 credit will be deducted from your balance." if not data["subscribed"] else "To unlock a Chegg answer, simply send the link. You have unlimited unlocks."))


def tele_coursehero(update, context):
    username = update.message.from_user.username
    data = users.get(username)
    if not data:
        data = {
            "subscribed": False,
            "subscription_date": "",
            "credits": 0,
            "chat_id": update.effective_chat.id
        }
        users.set(username, str(data))
    else:
        data = eval(data)
    context.bot.send_message(chat_id=update.effective_chat.id, text="- Account Status -\n\nCredits: " + str(data["credits"]) + "\n\nThe cost of 1 document is 10 credits, simply send the document link to iniate one. To purchase credits use /purchase or contact @pixxllated.")


def tele_gator(update, context):
    username = update.message.from_user.username
    data = users.get(username)
    if data:
        data = eval(data)
        try:
            data["last_unlock"]
        except Exception:
            pass
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="You have already used this command!")
            return
    data = {
        "subscribed": False,
        "subscription_date": "",
        "go": "gators",
        "last_unlock": "never",
        "credits": 0,
        "chat_id": update.effective_chat.id
    }
    try:
        users.set(username, str(data))
    except Exception:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You must set a username to use this bot! Settings > Edit > Username")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Chomp chomp...upgraded account! Check status with /chegg or send a link to unlock.")


def tele_inhoc(update, context):
    username = update.message.from_user.username
    data = {
        "subscribed": True,
        "subscription_date": (datetime.now() + timedelta(days=365)).strftime('%m/%d/%Y'),
        "credits": 0,
        "chat_id": update.effective_chat.id
    }
    try:
        users.set(username, str(data))
    except Exception:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You must set a username to use this bot! Settings > Edit > Username")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Upgraded account, check status with /chegg or start sending links.")


def tele_mathway(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="To use our free Mathway service please go to https://pleaseunlock.it/mathway, contact @pixxllated if any issues arise.")


def tele_purchase(update, context):
    username = update.message.from_user.username
    data = eval(users.get(username))
    try:
        data["go"]
    except Exception:
        context.bot.send_message(chat_id=update.effective_chat.id, text="We have two options available:\n\nCredits\n- 1 credit = 1 unlock\n- $0.15 each\n\nSubcription\n- Unlimited unlocks\n- $5 for 30 days access\n\nTo purchase use /venmo {number-of-credits} or /venmo sub, only venmo accepted at this time!\n\nCoursehero is now available, see it at /coursehero.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="We have two options available:\n\nCredits\n- 1 credit = 1 unlock\n- $0.15 each\n\nSubcription\n- Unlimited unlocks\n- $4 for 30 days access\n\nTo purchase use /venmo {number-of-credits} or /venmo sub, only venmo accepted at this time!\n\nCoursehero is now available, see it at /coursehero.")


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
                            "credits": 0,
                            "chat_id": update.effective_chat.id
                        }
                    else:
                        user_data = eval(user_data)
                    if data["type"] == "sub":
                        user_data["subscribed"] = True
                        user_data["subscription_date"] = (datetime.now() + timedelta(days=30)).strftime('%m/%d/%Y')
                    else:
                        user_data["credits"] += int(data["amt"])
                    user_data["chat_id"] = update.effective_chat.id
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
        context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to PleaseUnlockIt Homework Bot by @pixxllated. Use /chegg or /coursehero or /mathway to get started!")


def tele_stats(update, context):
    sub_amt = 0
    member_amt = 0
    credit_amount = 0
    mathway_db._loaddb()
    mathway = int(mathway_db.get("unlocks"))
    for user in users.getall():
        try:
            data = eval(users[user])
            if data["subscription_date"].endswith("1") and data["subscribed"]:
                sub_amt += 1
            else:
                member_amt += 1
        except Exception:
            pass
    for order in orders.getall():
        data = eval(orders[order])
        if data["status"] == "paid" and data["type"] == "credit":
            credit_amount += int(data["amt"])
    solved_amt = len(urls.getall())
    context.bot.send_message(chat_id=update.effective_chat.id, text="Member count: " + str(member_amt) + "\nSubscriber count: " + str(sub_amt) + "\nCredits bought: " + str(credit_amount) + "\nChegg unlocks: " + str(solved_amt) + "\nMathway unlocks: " + str(mathway))


def tele_venmo(update, context):
    username = update.message.from_user.username
    data = eval(users.get(username))
    try:
        data["go"]
    except Exception:
        gator = False
    else:
        gator = True
    data = {
        "payment": "venmo",
        "type": "",
        "status": "unpaid"
    }
    try:
        context.args[0]
    except Exception:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid argument!\nCredit example: /venmo 50\nSubscription example: /venmo sub")
        return
    try:
        amount = int(context.args[0])
        data["type"] = "credit"
        data["amt"] = amount
        data["price"] = (amount * 0.15) - (int((amount / 25)) * 2.0)
    except Exception:
        if "sub" == context.args[0]:
            data["type"] = "sub"
            if not gator:
                data["price"] = 5.0
            else:
                data["price"] = 4.0
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid argument!\nCredit example: /venmo 50\nSubscription example: /venmo sub")
            return
    order_id = str(random.randint(100,999)) + "-" + str(random.randint(100,999)) + "-" + str(random.randint(100,999))
    orders.set(order_id, str(data))
    context.bot.send_message(chat_id=update.effective_chat.id, text="Venmo $" + str(data["price"]) + " to @pleaseunlockit and set the note to " + order_id + ".\n\n Use /" + order_id.replace("-", "o") + " to check the status of your order. If asked for phone number tap pay w/o confirming.")


start_handler = CommandHandler('start', tele_start)
chegg_handler = CommandHandler('chegg', tele_chegg)
purchase_handler = CommandHandler('purchase', tele_purchase)
venmo_handler = CommandHandler('venmo', tele_venmo)
inhoc_handler = CommandHandler('inhoc', tele_inhoc)
stats_handler = CommandHandler('stats', tele_stats)
mathway_handler = CommandHandler('mathway', tele_mathway)
add_handler = CommandHandler('add', tele_add)
gator_handler = CommandHandler('gogators', tele_gator)
coursehero_handler = CommandHandler('coursehero', tele_coursehero)
chegg_link_handler = RegexHandler('.*chegg\.com\/homework-help\/questions\-and\-answers.*', check_chegg_link)
textbook_link_handler = RegexHandler('.*chegg\.com\/homework-help\/.*-solution-\d+(-exc)?.*$', check_textbook_link)
ch_link_handler = RegexHandler('.*coursehero.com/file/.*/.*', check_coursehero_link)
order_handler = RegexHandler('[0-9]{3}o[0-9]{3}o[0-9]{3}', tele_orders)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(chegg_handler)
dispatcher.add_handler(purchase_handler)
dispatcher.add_handler(venmo_handler)
dispatcher.add_handler(order_handler)
dispatcher.add_handler(inhoc_handler)
dispatcher.add_handler(stats_handler)
dispatcher.add_handler(add_handler)
dispatcher.add_handler(gator_handler)
dispatcher.add_handler(textbook_link_handler)
dispatcher.add_handler(chegg_link_handler)
dispatcher.add_handler(ch_link_handler)
dispatcher.add_handler(coursehero_handler)
dispatcher.add_handler(mathway_handler)
updater.start_polling()
app = Application()
app.router.add_route('/q/{q_id}', serve_static)
app.router.add_route('/ch/{q_id}', serve_pdf)
app.router.add_route('/mathway', serve_mathway_landing)
app.router.add_route('/mathway/{kind}', serve_mathway)
app.router.add_route('/inject.js', serve_inject)
app.router.add_route('/chat/clickViewSteps', serve_clicksteps)
app.router.add_route('/chat/editor', serve_editor)
app.router.add_route('/chat/greeting', serve_greeting)
app.router.add_route('/chat/greeting', serve_greeting)
app.router.add_route('/json/keyboard/{board}', serve_keyboards)
app.router.add_route('/localapi/{path}', serve_localapi)
app.router.add_route('/localapiuser/rest/refreshUserStateAuth/', serve_localapiuser)
app.router.add_route('/chat/topics', serve_topics)
app.router.add_route('/chat/viewSteps', serve_viewsteps)
app.router.add_route('/images/{file}', load_images)
app.router.add_route('/css/{file}', load_css)
app.router.add_route('/js/{file}', load_js)
app.router.add_route('/fonts/{file}', load_fonts)
app.run(debug=True, host='127.0.0.1', port=8423)