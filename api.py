#! /usr/bin/env python
from flask import Flask
import requests
import json
from settings import now_playing_url, discogs_token

app = Flask(__name__)

def get_current_song():
    response = requests.get(now_playing_url)
    if response.ok:
        image_response = requests.get(
            "https://api.discogs.com/database/search?q=%s&token=%s" % (
                response.text,
                discogs_token
            )
        )
        try:
            image = json.loads(image_response.text).get(
                'results'
            )[0].get('thumb')
        except:
            image = None
    app.current = {
        'success': response.ok,
        'result': response.text if response.ok else response.status_code,
        'image': image
    }
    return app.current

@app.route("/now-playing/")
def now_playing():
    return json.dumps(get_current_song())

if __name__ == "__main__":
    app.run()
    app.current = None
