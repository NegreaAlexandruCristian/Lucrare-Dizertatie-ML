"""
This script is used to get 100 tweets about bitcoin for today.
It will return a DataFrame so that it can be feed to the model.
"""

import pandas as pd
import snscrape.modules.twitter as sn_twitter
import datetime
from datetime import timedelta
from tqdm.notebook import tqdm_notebook


def search(text, username, since, until, retweet, replies, language):
    q = text
    if username != '':
        q += f" from:{username}"
    if until == '':
        until = datetime.datetime.strftime(datetime.date.today(), '%Y-%m-%d')
    q += f" until:{until}"
    if since == '':
        since = datetime.datetime.strftime(datetime.datetime.strptime(until, '%Y-%m-%d') -
                                           datetime.timedelta(days=7), '%Y-%m-%d')
    q += f" since:{since}"
    if retweet == 'y':
        q += f" exclude:retweets"
    if replies == 'y':
        q += f" exclude:replies"
    if username != '' and text != '':
        filename = f"{since}_{until}_{username}_{text}.csv"
    elif username != "":
        filename = f"{since}_{until}_{username}.csv"
    else:
        filename = f"{since}_{until}_{text}.csv"
    if language != '':
        q += f" lang:{language}"
    print(filename)
    return q


def get_tweets():
    text = 'bitcoin'  # what to search for
    username = ''
    since = datetime.date.today().strftime("%Y-%m-%d")
    until = (datetime.date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    count = 100  # number of tweets per day
    retweet = 'y'
    replies = 'y'
    language = 'en'  # language of the tweet
    # If no language is provided then the default will take every language it can find
    # Creating list to append tweet data
    tweets_list1 = []
    start_date = datetime.datetime.strptime(since, '%Y-%m-%d').replace(
        hour=0, minute=0, second=0, microsecond=0)  # start date
    end_date = datetime.datetime.strptime(until, '%Y-%m-%d').replace(
        hour=0, minute=0, second=0, microsecond=0)  # end date
    for n in range((end_date - start_date).days + 1):
        date = start_date + timedelta(n)  # Take the first day that is from since
        date_plus_one_day = date + timedelta(days=1)  # Add one day to it
        q = search(text, username, date.strftime('%Y-%m-%d'),
                   date_plus_one_day.strftime('%Y-%m-%d'), retweet, replies,
                   language)
        with tqdm_notebook(total=count) as pbar:
            for i, tweet in enumerate(sn_twitter.TwitterSearchScraper(q).get_items()):  # Declare a username
                if i >= count:  # Number of tweets you want to scrape
                    break
                tweets_list1.append([tweet.date, tweet.rawContent, tweet.lang,
                                     tweet.replyCount, tweet.retweetCount,
                                     tweet.likeCount, tweet.quoteCount])
                pbar.update(1)

    # Creating a dataframe from the tweets list above
    tweets_df1 = pd.DataFrame(tweets_list1, columns=['DateTime', 'Text', 'Language',
                                                     'ReplyCount', 'RetweetCount', 'LikeCount', 'QuoteCount'])
    tweets_df1.sort_values(by='DateTime', ascending=False)

    return tweets_df1


print(get_tweets())
