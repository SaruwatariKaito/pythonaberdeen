import re
import urllib

from django.utils import simplejson
from django.utils.html import urlize
from google.appengine.api import memcache

from flask import Flask
from flask import render_template
from jinja2 import Markup

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', );

def twitterfy(tweet):

    # find hashtags
    pattern = re.compile(r"(?P<start>.?)#(?P<hashtag>[A-Za-z0-9_]+)(?P<end>.?)")

    # replace with link to search
    link = r'\g<start>#<a href="http://search.twitter.com/search?q=\g<hashtag>"  title="#\g<hashtag> search Twitter">\g<hashtag></a>\g<end>'
    text = pattern.sub(link,tweet)

    # find usernames
    pattern = re.compile(r"(?P<start>.?)@(?P<user>[A-Za-z0-9_]+)(?P<end>.?)")

    # replace with link to profile
    link = r'\g<start>@<a href="http://twitter.com/\g<user>"  title="#\g<user> on Twitter">\g<user></a>\g<end>'
    text = pattern.sub(link,text)

    return Markup(urlize(text))

@app.context_processor
def get_tweets():
    
    tweets = memcache.get("tweets")
    
    if tweets is None:
        
        url = "http://search.twitter.com/search.json?q=from:pythonedinburgh"
        f = urllib.urlopen(url)
        content = f.read()
        json = simplejson.loads(content)
        json_tweets = json['results']
        
        tweets = {'tweets': [twitterfy(tweet['text']) for tweet in json_tweets],}
        
        if not memcache.add("tweets", tweets, 60 * 10): # 10 mins.
            logging.error("Memcache set failed.")
        
    return tweets

app.secret_key = '7%@0g6y!hu^flbmkcfb$@zxs9ftmh=t0blgnog-ibh52za$6nu'

if __name__ == '__main__':
    app.run()
