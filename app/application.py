import os
import sys
sys.path.insert(1, os.path.join(os.path.abspath('.'), 'lib'))

import logging
from google.appengine.api import memcache
from flask import Flask
from flask import render_template
import ical

app = Flask(__name__)


@app.route('/')
def home():
    upcoming_events = memcache.get("upcoming_events")
    if not upcoming_events:
        upcoming_events = ical.upcoming_events()
        if not memcache.add("upcoming_events", upcoming_events, 60 * 10):  # 10 minutes
            logging.error("Memcache 'upcoming_events' store failed.")

    return render_template('home.html', upcoming_events=upcoming_events)


app.secret_key = 'efunys87f6bd8s7yb8ds7vfbv7ybd8b7faynd7sif 6ibc87nubtdc8b'