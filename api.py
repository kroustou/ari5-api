#! /usr/bin/env python
from flask import Flask
import requests
import json
from bs4 import BeautifulSoup
from settings import now_playing_url, discogs_token, history_url, listeners_url

app = Flask(__name__)


def get_details(title):
    # fake headers because discogs was dropping requests
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    try:
        image_response = requests.get(
            "https://api.discogs.com/database/search?q=%s&token=%s" % (
                title,
                discogs_token
            ),
            headers=headers
        )
        image = json.loads(image_response.text).get(
            'results'
        )[0].get('thumb')
    except:
        image = 'http://placehold.it/150x150/2c3e50/?text=no+image'
    return {
        'result': title,
        'image': image
    }


def get_current_song():
    response = requests.get(now_playing_url)
    if response.ok:
        app.current = get_details(
            response.text.replace('+', ' ').replace('-', ' ')
        )
    app.current['success'] = response.ok
    return app.current


@app.route("/history/")
def get_history():
    response = requests.get(history_url)
    titles = []
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        tr = soup.findAll('table')[2].findAll('tr')[2:]
        for row in tr:
            titles.append(
                get_details(
                    row.findAll('td')[1].text.replace('+', '').replace('-', '')
                )
            )
    return json.dumps({'songs': titles, 'success': response.ok})


@app.route("/listeners/")
def get_listeners():
    response = requests.get(listeners_url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        listeners = soup.findAll('table')[3].findAll('tr')[1].text.split()[9]
    return json.dumps({'listeners': listeners})


@app.route("/now-playing/")
def now_playing():
    return json.dumps(get_current_song())

if __name__ == "__main__":
    app.run()
    app.current = None
