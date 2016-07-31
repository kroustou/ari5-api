#! /usr/bin/env python
from flask import Flask
import requests
import json
from bs4 import BeautifulSoup
from settings import now_playing_url, discogs_token, history_url

app = Flask(__name__)

def get_details(title):
    image_response = requests.get(
        "https://api.discogs.com/database/search?q=%s&token=%s" % (
            title,
            discogs_token
        )
    )
    try:
        image = json.loads(image_response.text).get(
            'results'
        )[0].get('thumb')
    except:
        image = None
    return {
        'result': title,
        'image': image
    }


def get_current_song():
    response = requests.get(now_playing_url)
    if response.ok:
        app.current = get_details(response.text)
    app.current['status'] = response.ok
    return app.current

@app.route("/history/")
def get_history():
    response = requests.get(history_url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        tr = soup.findAll('table')[2].findAll('tr')[2:]

        titles = []
        for row in tr:
            titles.append(get_details(row.findAll('td')[1].text))
        return json.dumps(titles)


@app.route("/now-playing/")
def now_playing():
    return json.dumps(get_current_song())

if __name__ == "__main__":
    app.run()
    app.current = None
