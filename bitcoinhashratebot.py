import tweepy
import requests
import sched
import time
import logging
from bs4 import BeautifulSoup
from os import environnement

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

CONSUMER_KEY = environnement['CONSUMER_KEY']
CONSUMER_SECRET = environnement['CONSUMER_SECRET']
ACCESS_KEY = environnement['ACCESS_KEY']
ACCESS_SECRET = environnement['ACCESS_SECRET']

# Authenticate to Twitter
auth = tweepy.OAuthHandler("CONSUMER_KEY",
    "CONSUMER_SECRET")
auth.set_access_token("ACCESS_KEY",
    "ACCESS_SECRET")

api = tweepy.API(auth)

try:
    api.verify_credentials()
except Exception as e:
    logger.error("Error creating API", exc_info=True)
    raise e
logger.info("API created")

s = sched.scheduler(time.time, time.sleep)

def tweet():

    url = 'https://blockchain.info/q/hashrate'
    response = requests.get(url)
    currentbitcoinahshratebs = BeautifulSoup(response.text, "html.parser")
    # Convert to string to conver to float
    currentbitcoinahshratestring = str(currentbitcoinahshratebs)
    # Convert to float to be able to divie later
    currentbitcoinahshratefloat=float(currentbitcoinahshratestring)
    # Conver to tera and round
    currentbitcoinahshratetera = round(currentbitcoinahshratefloat/10**9)
    # Convert to string to log and tweet
    currentbitcoinahshratestring=str(currentbitcoinahshratetera)

    # Tweet
    logger.info("Current Bitcoinh hashrate is: " + currentbitcoinahshratestring + " TH/s #hashrate #Bitcoin")
    api.update_status("Current Bitcoinh hashrate is: " + currentbitcoinahshratestring + " TH/s #hashrate #Bitcoin")

    logger.info(str(time.time()) + " before tweet() enter")
    s.enter(60, 1, tweet)
    logger.info(str(time.time()) + " end of tweet()")

logger.info(str(time.time()) + " before main enter")
s.enter(60, 1, tweet)
logger.info(str(time.time()) + " after main enter")
s.run()
logger.info(str(time.time()) + " after main run")
