from japronto import Application


def serve_static(request):
    try:
        q_id = request.match_dict["q_id"]
        if (".png" not in q_id and ".jpg" not in q_id) or ".." in q_id or "/" in q_id:
            # attempted injection
            pass
        with open('/home/autobuy/html/' + q_id + '.html', 'r', encoding="utf-8") as html:
            return request.Response(text=html.read(), mime_type="text/html")
    except Exception:
        return request.Response(headers={"Location": "https://pleaseunlock.it"}, code=302)


app = Application()
app.router.add_route('/q/{q_id}', serve_static)
app.run(debug=True, host='127.0.0.1', port=8423)