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
ch_db = pickledb.load('ch_ids.db', True)
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
ch_sesh = requests.Session()
ch_sesh.cookies = requests.utils.cookiejar_from_dict({
    'root_session_id': '3i7b6imf3b4u77togg9an3n333',
    'visid_incap_987752': '3xsisvwbSbO13TZtgJixjd5Lol4AAAAAQUIPAAAAAACE+aM4s+3VR6Py73Wjt/NW',
    '_ga': 'GA1.2.410662598.1587694561',
    '__qca': 'P0-1201088568-1587694561953',
    '_scid': 'd597db49-db65-492d-b803-ed53223390ab',
    'G_ENABLED_IDPS': 'google',
    'has_successfully_logged_in_the_past': '1',
    'fs_uid': 'rs.fullstory.com#K1C9K#5801996828819456:4754563625664512#4f64d2c6#/1619230823',
    '_pxvid': 'd59251a1-fb90-11ea-adf3-8b734cd74a10',
    'ki_u': '43fb787a-dac0-7e82-a5dd-b618',
    '_mibhv': 'anon-1575062618161-1039038976_6196',
    'ki_s': '208270%3A0.0.0.0.0%3B208738%3A0.0.0.0.0%3B210456%3A1.0.0.0.2',
    '_pin_unauth': 'dWlkPVlXWmtNV1l4WXpjdE56azRNeTAwTkRjMUxUa3lOek10TlRsak0yTTRNRGRoTUdJMQ',
    'ki_r': '',
    '_derived_epik': 'dj0yJnU9bGlVWkZXdFNWQ3hBVDBRZXd6N185aGtUQTBBbEs3Y3Umbj1FeWY0aDhubUJLdjVwNXlMM2pxTVB3Jm09NyZ0PUFBQUFBRi0wVGVj',
    'device_view': 'full',
    '_gcl_au': '1.1.1451615099.1613014062',
    '__gads': 'ID=ab3538d9f9d1afde-22e0accaabb80026:T=1613014063:RT=1613014063:S=ALNI_MbRCMw26RWbPPNQoG6xHiKbsfAFsQ',
    'tq771_amazon_bucket': '0',
    'qualaroo_doc_visited': 'true',
    'qualaroo_loggedin': 'true',
    'qualaroo_register_visited': 'false',
    '__cfduid': 'd17b421d97ec7af10fb25808fc5cce9741613014151',
    'tq819_amazon_v2_bucket': '2',
    '_sctr': '1|1614488400000',
    'incap_ses_1286_987752': 'dor0R9TFukFwCDRqUMrYEeOkPmAAAAAAgT+0l5Kc3iF2WJFU8BGpvQ==',
    '_gid': 'GA1.2.1685591465.1614718181',
    'has_called_TBM': '1',
    'nlbi_987752': 'cHGNRU2nZAh3YVOF5Tz1lQAAAAARqkqG7d2Jl2xbc1I4KjmG',
    'sc.ASP.NET_SESSIONID': '',
    'sc.Status': '2',
    'incap_ses_890_987752': 'LC4wOKuEqmV8iwZ4jOpZDCmlPmAAAAAA63tB2wtZcZgqnpVEYGq8Gw==',
    'incap_ses_8216_987752': 'MinkRtnIxnHIWVdLlBgFcj6lPmAAAAAAvWZZUSQb/0LzJy/smQpa7A==',
    'userID': '100000790267562',
    'ch_logged_in': '1',
    'userEmail': 'bnbaltz%40gmail.com',
    'supportEmail': 'bnbaltz%40gmail.com',
    'incap_ses_486_987752': 'ttAuYdVahlj07qFMxZ6+BiemPmAAAAAABNxsEMsFC0pmTdU9sJs1lQ==',
    'incap_ses_1348_987752': 'jhqaE1WSJzgcb8tS/A61Ev+nPmAAAAAA3DteaLaM36dOB734auxqoA==',
    'incap_ses_209_987752': 'PFdec3eqdCAOaCAujITmAiWrPmAAAAAAlocvwUOGX9PwK0ujZ8mVQQ==',
    'incap_ses_237_987752': 'Y+fhFt6qX2BaeFQ5X/5JA0auPmAAAAAAtYV2Xk/tJ4BI/fg2f5JFBw==',
    'incap_ses_236_987752': 'khx1XcksKRTQgOiV4HBGA0auPmAAAAAAGfhnCnUcacpgYiT21vp/ww==',
    'incap_ses_1353_987752': 'ep83P4syE0V+xCFDc9LGEkeuPmAAAAAAbPkAtaWLmQ9jVIyKzwQvJA==',
    'incap_ses_517_987752': 'LXMyaIfmlFoJvwtQFMEsB0euPmAAAAAArjJ2XKxtK0M6+EBXK1Zkkg==',
    'incap_ses_7222_987752': 'gY38UdD//Ushn4Rx37I5ZEeuPmAAAAAAE6QQ+/X3tgyf7tnUtb/Oqg==',
    'incap_ses_620_987752': 'gF8jGwbHC04jZyM4Da+aCEeuPmAAAAAAGHGm4wynnHPxbmFL1oyorg==',
    'incap_ses_995_987752': 'jjapQOR4fU2uKohJgPPODXa9PmAAAAAAYtzL9Es/M0AW7ek6YUz5Lg==',
    'PHPSESSID': 'e6313bf9-04f6-408f-87cd-5efc8c89e4da',
    'remember_me': '100000790267562%7C%7CH2y2H2PssUAL7qPxXYaWOyvJIJDW7H',
    'incap_ses_988_987752': 'UJyZSa85HxPQ7EIVGhW2DcC+PmAAAAAApiDcZKC7rs8Nib0L2RUI+w==',
    'incap_ses_1307_987752': '84F+Z/OAzDmcuEpItmUjEsC+PmAAAAAAfJHXcnRuco9UgiwIrXoc6A==',
    'incap_ses_1181_987752': 'NTs0GIU1Bg9hmWtkhsFjEMC+PmAAAAAAnfcrPvDaaECKa4xB1igYTw==',
    'incap_ses_1178_987752': 'q9AhQB2VaUzgYVvh4hhZEMC+PmAAAAAA+/j0TkPvNi5RignpQt91yA==',
    'incap_ses_470_987752': '5R1xTecJ7BAAXxZf1saFBsC+PmAAAAAAAF+oU9n5/710TrMAdXxTWg==',
    'incap_ses_1344_987752': '6cnwc8cxZQDDIspt/9imEsG+PmAAAAAADEjzDGnLheMcESV2dXHV7A==',
    'incap_ses_8079_987752': 'SubXKOQypg+z4nsUx18ecMC+PmAAAAAAbxOirCzs4Jm4vRQTGny14Q==',
    'lux_uid': '161472480127121762',
    'incap_ses_1373_987752': 'PvCsSSRFWyfViu+9TuANE8G+PmAAAAAAg5mJyq7LNINL+qIMGf2XRQ==',
    'incap_ses_1180_987752': 'wa8bPxvFIXLCD6ba3TNgEMC+PmAAAAAAgcNL8tHRscHzWQLPQy9cHA==',
    'incap_ses_1352_987752': 'IWEwapcLu1bqoXGR9ETDEsG+PmAAAAAAupmxL+v0zX+6puWgRAS1YQ==',
    'incap_ses_1343_987752': 'laZmXwTQhXmFOjDLgEujEsG+PmAAAAAAeQslr7HUrAZp8aKmtkBq0g==',
    'incap_ses_118_987752': 'sgx4LZmXqmz0X4HNpTijAcG+PmAAAAAAqjBY1k6KWz1QTdC82KhEKQ==',
    'incap_ses_1213_987752': 'V3BIVKmAOir7jn1dT3HVEMG+PmAAAAAAIbuer5XK6S1YOhw2CBJ1/Q==',
    'incap_ses_1318_987752': 'rAQhRFnq/GiiTXQOEHpKEsG+PmAAAAAAONuU2RxyrIE7DnASLw0OKA==',
    'incap_ses_8221_987752': 'd4zkDLVIe2bWbWYmBNwWcsG+PmAAAAAA++vXVJYjZ3hGOCHbm/z4AA==',
    'outbrain_cid_fetch': 'true',
    'incap_ses_516_987752': 'Gvk2fFMYzwiBu/T/lzMpB8G+PmAAAAAAi+oQ29ARBRct+OzCIaP+bg==',
    'incap_ses_1370_987752': '5q0GSwZ7ECX53GN70DcDE8W+PmAAAAAAYTZqnMjkMaopyapaJwXFEQ==',
    'incap_ses_7226_987752': '786VekwO2QgmyprDwuhHZMW+PmAAAAAAXTY9j0IhpnJb4PD0KapqaQ==',
    'incap_ses_891_987752': 'Z+F7FKglCWZ0EydwBnhdDMa+PmAAAAAAPRly23qr9xSmulWXhtCMtA==',
    'incap_ses_989_987752': 'zR82Mcnr5ETp4TJmlqK5Dca+PmAAAAAAMZKuxzkWzMtWJx6VZ94VCA==',
    'incap_ses_1310_987752': 'OOZ7Qgim2mUbk3l+NA4uEsa+PmAAAAAA9jzWgAUNIDIEEpHlKqmxyA==',
    'incap_ses_223_987752': 'cbWoEFdANR4m7YTcaEEYA9K+PmAAAAAAhI7LgJskOAkTMsjh7K51yw==',
    'incap_ses_1374_987752': 'bXeEV7PBmmIfiVpd1G0RE9K+PmAAAAAAqDn2RpOkraCz69XU7xo3LA==',
    'incap_ses_482_987752': 'wf2CHgtLogZiwM5xyGiwBtK+PmAAAAAAqzoCwdlx0UN9BF8MZn3xEg==',
    'incap_ses_9219_987752': 'MvfaKpSRPA7vxMGHunfwf9K+PmAAAAAAmW2Ocqm6rxdzx8Gx64eewQ==',
    'incap_ses_978_987752': 'pfZob+NddRbD/3T9Io6SDdK+PmAAAAAA1nsTFjvoMk98mQr+C2JjMw==',
    'incap_ses_1182_987752': 'F6KwdSFnJkecV6299E5nENO+PmAAAAAAq70dTFoXM8iwHy21jS0cxw==',
    'incap_ses_1342_987752': 'pUq+bW4VPEu90g0mAr6fEtO+PmAAAAAAbCI4JEPLlHxtIE83YVIrZQ==',
    'incap_ses_480_987752': '1JkCDgjcLl7UgaPSz02pBtO+PmAAAAAA4J6g0ZT8gvQpdnwq1nVprA==',
    'incap_ses_117_987752': '51fZXgauY0EzJM98KaufAda+PmAAAAAAOb2LidbkknYd4xX/lEoujQ==',
    'incap_ses_993_987752': 'JNWpZiV4knQY/zZQjNjHDda+PmAAAAAA/MpZ/1vIS3xhh1e1DU7F2g==',
    'incap_ses_1340_987752': 'gcSFMlQ9Zkb8gRfZBKOYEta+PmAAAAAAzdu04DOtFyVTeA5khqu6dg==',
    'qualaroo_doc_unlocked': 'false',
    'incap_ses_980_987752': 'CnUaX2FYJxDfuwb2FqmZDdq+PmAAAAAA139dIj3JaFX2GtW/93fdtg==',
    'incap_ses_991_987752': '6UdDGuwlLBp9q6uyjL3ADdu+PmAAAAAA9wgAcmnSNM0JQaz+YHacOg==',
    'incap_ses_623_987752': '1lsBMiImgGgXsoCBfVelCNu+PmAAAAAAoThLHSkw3ekhaGzwwskDDw==',
    '_gat': '1',
    'incap_ses_515_987752': 'y/TbDWxn+R/ocvtcGaYlBy+/PmAAAAAAZ9bBtvqnAEycmbvb8yseDQ==',
    'recently_viewed_docs': '10711040%2C17354188%2C69755589%2C',
    'has_seen_mcq': 'yes',
    'incap_ses_986_987752': 'ukBdAtlwjEt5ObaDE/quDTa/PmAAAAAAN0udXXDHeVolzjzIWLN+cg==',
    'last_viewed_question': '28330709',
    'ki_t': '1587695722015%3B1614718200408%3B1614724932670%3B14%3B101',
    '_px3': '90d71f49fb1e6f47540883aac8fe1db5abcf6e71641d249c5c5f24dd704fa6c1:34z4+0R1P3EO6cc3MKFg2IEOQ8htNQ1om+pRTlbrhb0WnRJwtFxublmpA8YbFmLlsWIqWoW7n7fz2vQauqx9fg==:1000:6zaJbaRZDKmwJ7pTGAIg+OYa03vAThwz/r1RYuO1nSczxShySd6AhjtLSCqJ8r6t9Qrm5owIb/g+5BFksNhe0pRYcdsHqO8ZkK+1fIVUcSXCjF/AI+hwCsdou/egXikg7YjNTfgw5qTRo0C6bdWFMQxmebaHxceulNF6KKBBOlk=',
    'amplitude_id_ee857825ebc317614f56e416919c1844coursehero.com': 'eyJkZXZpY2VJZCI6ImQwZWNmODM0YWNhODNiZTEyZDlhZTlmMGMzNTUwZjk0Njk0Mjc1ODQiLCJ1c2VySWQiOiIxMDAwMDA3OTAyNjc1NjIiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE2MTQ3MjQ4MDAsImxhc3RFdmVudFRpbWUiOjE2MTQ3MjQ5NDI0NDUsImV2ZW50SWQiOjQxOSwiaWRlbnRpZnlJZCI6NjIsInNlcXVlbmNlTnVtYmVyIjo0ODF9',
    '_uetsid': 'cf97e7807b9811eb873063e4b6442eea',
    '_uetvid': '13a1fd407a3411eb8ea737d45dda3c8a',
    'nlbi_987752_2147483646': 'hR2iXQRNA0MC1RSr5Tz1lQAAAACNRB4H/k5XBNqBa/SmS6Lj',
    'reese84': '3:iq7XYbLy3PN8Juc2zEMvnA==:rkGb6G4z6ImgwgotSSBf9CNiXnErdUD72klP1zF6woeQomqVIxRpVFkyncVjCY/+S6T8ISfVTVT61IObCgQCEPTvmNXYOjuPAS2QEt0mMfocXPtwAIkq9WiuLOIEd9xpNrR7WLFqVC2zQP1lBL9o/nmVF1zquizNCU/PIiAubexF37W/kqZjcfZArbZVgHjZ7CRhNs0yU1XenDHo+qBOTiPJgAJyDRnAcZIXsACKdKjWIcs0KVKmhEZrE19Eic7lGgbHyuo9s3V1tpyybM98lqHLkEk4GoogWP5BfOi4+R9EyRShFnAT2ahOjESneiwqg2BPSe/ZZmnPPiBpZuNUrLbNk58leFBVI/Q7CAGl6w0d1PW3cx8448wSR7nd5I1bJu+r+KFL56MQE7YJulNqd3ALRWTOIw9+5gccaxEdr+I=:q+xMMUrD5BYf35b8+tqt9VbJcvdH2TKNneCt4nt5TgE=',
})
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


def ch_pdf(_id):
    headers = {
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://www.coursehero.com/pdfjs/build/pdf.worker.js',
        'Sec-Fetch-Dest': 'empty',
        'Connection': 'keep-alive',
    }
    response = ch_sesh.get('https://www.coursehero.com/pdf/document/' + _id + '/', headers=headers)
    if "Something is broken." in response.text:
        return False
    file_name = str(uuid.uuid4()) + ".pdf"
    output_file = open("/home/autobuy/html/" + file_name, "wb")
    output_file.write(response.content)
    output_file.close()
    ch_db.set(_id, file_name)
    return file_name


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
    if not data["subscribed"]:
        if (data["credits"]) > 0:
            data["credits"] = int(data["credits"]) - 1
            data["chat_id"] = update.effective_chat.id
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
        formatted_html = get_question(question_id)
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


def check_coursehero_link(update, context):
    link = update.message.text
    _id = re.search('file/(.*?)/', link).group(1)
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
    if (data["credits"]) > 9:
        data["credits"] = int(data["credits"]) - 10
        data["chat_id"] = update.effective_chat.id
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Not enough credits to unlock! View /purchase to get started.")
        return
    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    response = ch_sesh.get(link, headers=headers)
    full_url = response.url
    if 'u/file/' in response.text:
        dl_id = ch_pdf(_id)
        users.set(username, str(data))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Download here: https://pleaseunlock.it/ch/" + dl_id)
        return
    post_data = {
        "dbFilename": _id
    }
    main_url = response.url
    headers["Referer"] = main_url
    response = ch_sesh.post("https://www.coursehero.com/api/v1/unlock-doc-action/", headers=headers, json=post_data)
    print(response.text)
    response = ch_sesh.get(main_url.replace("file", "unlock-document"), headers=headers)
    dl_id = ch_pdf(_id)
    if not dl_id:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to get your document, please contact @pixxllated. You were not charged.")
        return
    post_data = {
        "contentType": "document",
        "typeId": _id,
        "sourceName": "null"
    }
    response = ch_sesh.post('https://www.coursehero.com/api/v1/document/' + _id + '/like/', headers=headers, json=post_data)
    print(response.text)
    users.set(username, str(data))
    context.bot.send_message(chat_id=update.effective_chat.id, text="Download here: https://pleaseunlock.it/ch/" + dl_id)


def check_question(url):
    cleaned_url = url.split("/")[-1].split("?")[0].split("#")[0]
    already_found = urls.get(cleaned_url)
    if not already_found:
        print("fetching url")
        response = csite_sesh.get(url)
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
        data["subscription_date"] = (datetime.now() + timedelta(days=365)).strftime('%m/%d/%Y')
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
        context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to PleaseUnlockIt Homework Bot by @pixxllated. Use /chegg or /coursehero to get started!")


def tele_stats(update, context):
    sub_amt = 0
    member_amt = 0
    for user in users.getall():
        try:
            data = eval(users[user])
            if data["subscription_date"].endswith("1") and data["subscribed"]:
                sub_amt += 1
            else:
                member_amt += 1
        except Exception:
            pass
    solved_amt = len(urls.getall())
    context.bot.send_message(chat_id=update.effective_chat.id, text="Member count: " + str(member_amt) + "\nSubscriber count: " + str(sub_amt) + "\nTotal unlocks: " + str(solved_amt))


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
add_handler = CommandHandler('add', tele_add)
gator_handler = CommandHandler('gogators', tele_gator)
coursehero_handler = CommandHandler('coursehero', tele_coursehero)
chegg_link_handler = RegexHandler('.*chegg\.com\/homework-help\/questions\-and\-answers.*', check_chegg_link)
textbook_link_handler = RegexHandler('.*chegg\.com\/homework-help\/.*-exc$', check_textbook_link)
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
updater.start_polling()
app = Application()
app.router.add_route('/q/{q_id}', serve_static)
app.router.add_route('/ch/{q_id}', serve_pdf)
app.run(debug=True, host='127.0.0.1', port=8423)