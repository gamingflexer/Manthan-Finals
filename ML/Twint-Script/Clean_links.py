import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import collections

import tweepy as tw
import nltk
from nltk.corpus import stopwords
import re
import networkx
import warnings



search_term = "ISIS"

tweets = tw.Cursor(api.search,
                   q=search_term).items(1000)

all_tweets = [tweet.text for tweet in tweets]

all_tweets[:5]
# remove all the links to ""

def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

all_tweets_no_urls = [remove_url(tweet) for tweet in all_tweets]
all_tweets_no_urls[:5]


# Normalize all words

twitter_list=['tweets']
lower_case = [twitter_list.lower() for twitter in twitter_list]

#calling it again to do

lower_case
