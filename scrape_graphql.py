import pickledb
import requests
import uuid


def refresh_sesh():
    headers = {
        "Authorization": "Basic aGxEcFpBUEYwNW1xakFtZzdjcXRJS0xPaFVyeUI4cDE6dUJqemFrbXhHeDZXdHFBcg==",
        "X-PX-AUTHORIZATION": "3",
        "X-PX-ORIGINAL-TOKEN": "3:f2f9cdae11aa972fea6fc75e177675552bb1eb1dbc5790a5d83cc2abeef0bcd7:txp8Stqk5ZX66+YIF8wg1ijngHmjJ/L4jBbBk87k9Nh2b85H1SUgqO4GuB3aIo2ieJeIr/Xtu+unau6H3Kxalg==:1000:WpFdWU+3bbPVC0xUM3kF7KYL9a7ra7OKfI2xLWJA1hijWLVEVR4OAEmslF42uDxBR1xl6Y2L9Mna9TCDJN0ZiU+7UeN7YXQ833vlOviEi0iVzeIF66c+Ag30xFyazRXvM9pUCsrJVehr//lVQOBw6UUSJsN+iVFlclR8m8ZVC/4=",
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
    chegg_data._loaddb()
    refresh_token = chegg_data.get("refresh_token")
    data = {
        "refresh_token": refresh_token,
        "source_page": "android Study 9.8.2|cs",
        "grant_type": "refresh_token",
        "source_product": "android|cs"
    }
    response = chegg_sesh.post("https://proxy.chegg.com/oidc/token", headers=headers, data=data)
    print(response.text)
    return response.json()


sesh_id = str(uuid.uuid4())
chegg_data = pickledb.load('chegg_data.db', True)
chegg_sesh = requests.Session()
#data = {'id': 'searchApiTbsAndStudy', 'operationName': 'searchApiTbsAndStudy', 'variables': {'page': 1, 'query': 'query allSchemaTypes {\n    __schema {\n        types {\n            name \n            kind\n            description\n        }\n    }\n}'}}
bips = [x.strip() for x in open("elements.txt", "r").readlines()]
for bip in bips:
    data = {'id': 'searchApiTbsAndStudy', 'operationName': 'searchApiTbsAndStudy', 'variables': {'page': 1, 'query': bip}}
    page = 1
    while True:
        chegg_data._loaddb()
        access_token = chegg_data.get("access_token")
        data["variables"]["page"] = page
        headers = {'Authorization': 'Basic aGxEcFpBUEYwNW1xakFtZzdjcXRJS0xPaFVyeUI4cDE6dUJqemFrbXhHeDZXdHFBcg==', 'X-CHEGG-DEVICEID': '33c3f20d242f5bccfaea8993283dd8102e37ebd2', 'X-CHEGG-SESSIONID': 'ee03efd5-f7ad-4139-8df8-29606ca11379', 'User-Agent': 'Chegg Study/10.0.4 (Linux; U; Android 10; Pixel 3 XL Build/QQ1A.200105.003)', 'X-ADOBE-MC-ID': '43643259243231378820218592977822332436', 'x-chegg-dfid': 'mobile|d0dd873f-70de-3f60-8994-2647e3133c75', 'x-chegg-auth-mfa-supported': 'true', 'Content-Type': 'application/json', 'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'X-NewRelic-ID': 'UQYGUlNVGwQCVFJTBwcD', 'access_token': access_token}
        while True:
            response = chegg_sesh.post("https://proxy.chegg.com/mobile-study-bff/graphql", headers=headers, json=data)
            if "Invalid Access Token" in response.text:
                response = requests.get("https://pleaseunlock.it/refresh_sesh")
                print(response.text)
                chegg_data._loaddb()
                access_token = chegg_data.get("access_token")
            break
        output_file = open("scraped_chegg_" + data["variables"]["query"] + ".txt", "a+")
        try:
            resp = response.json()
            for q in resp["data"]["studySearch"]["study"]["docs"]:
                if q["__typename"] == "SearchResultQna":
                    print(q["url"] + ":" + q["uuid"])
                    output_file.write(q["url"] + ":" + q["uuid"] + "\n")
            big = (resp["data"]["studySearch"]["study"]["numFound"] / 8)
            if page > big:
                print("finished")
                break
            # if big > 10000:
            #     break
            print(str(page) + "/" + str(big))
        except Exception:
            print(response.text)
        output_file.close()
        page += 1