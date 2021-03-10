import dbm.gnu
import requests

brainly_sesh = requests.Session()
brainly_data = dbm.open("brainly.db", "c")
_id = 1102585
while True:
    headers = {"Accept": "application/json", "X-APOLLO-EXPIRE-AFTER-READ": "true", "X-APOLLO-PREFETCH": "false", "X-APOLLO-CACHE-DO-NOT-STORE": "true", "Accept": "application/json", "Accept": "application/json", "X-B-Token-Guest": "5940934491e7150dfa15925729ddc1539475cd9a", "User-Agent": "Android-App 5.29.0 Android-App 5.29.0", "Content-Type": "application/json; charset=utf-8", "Connection": "keep-alive", "Accept-Encoding": "gzip, deflate"}
    json={"operationName": "QuestionByIdQuery", "query": "query QuestionByIdQuery($id: Int!) { questionById(id: $id) { __typename databaseId content points grade { __typename databaseId } subject { __typename databaseId name slug } author { __typename ...AuthorFragment } canBeAnswered attachments { __typename ...AttachmentFragment } answers { __typename hasVerified nodes { __typename databaseId content author { __typename ...AuthorFragment } thanksCount isBest created attachments { __typename ...AttachmentFragment } verification { __typename hasAccess approval { __typename approvedTime } } comments(last: 0) { __typename count } rating ratesCount } } } } fragment AuthorFragment on User { __typename databaseId nick rank { __typename name } avatar { __typename thumbnailUrl } } fragment AttachmentFragment on Attachment { __typename databaseId url extension }", "variables": {"id": _id}}
    response = brainly_sesh.post("https://brainly.com/graphql/us", headers=headers, json=json)
    if 'questionById":null' not in response.text:
        brainly_data[str(_id)] = response.text
        print("success: " + str(_id))
    else:
        print("fail: " + str(_id))
    _id += 1