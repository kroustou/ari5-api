#! /usr/bin/env python
from flask import Flask
import requests
import json
from settings import now_playing_url

app = Flask(__name__)


@app.route("/now-playing/")
def get_current_song():
    response = requests.get(now_playing_url)
    return json.dumps(
        {
            'success': response.ok,
            'result': response.text if response.ok else response.status_code,
        }
    )

if __name__ == "__main__":
    app.run()
