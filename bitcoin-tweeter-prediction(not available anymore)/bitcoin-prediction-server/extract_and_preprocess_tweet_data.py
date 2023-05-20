# Imports
import pandas as pd
import datetime as date_time


def get_tweet_data():
    # Load Twitter dataset
    df_tweets = pd.read_csv(
        'C:\\Master Anul 2\\Lucrare-Dizertatie-ML\\bitcoin-prediction-server\\dataset\\bitcoin_tweets.csv',
        on_bad_lines='warn',
        lineterminator='\n')
    # Choose a date randomly
    return df_tweets.sample()


def process_data():
    tweet_data = get_tweet_data()
    # Preprocess the dataframe
    tweet_data['DateTime'] = tweet_data['DateTime'].astype(str)
    tweet_data = tweet_data.drop(['Language', 'ReplyCount', 'RetweetCount',
                                  'LikeCount', 'QuoteCount', 'Unnamed: 0'], axis=1)
    # Convert the 'date' column to datetime format
    tweet_data['DateTime'] = pd.to_datetime(tweet_data['DateTime'])

    # Format the datetime object as a string with the 'yyyy-mm-dd' format
    tweet_data['DateTime'] = tweet_data['DateTime'].dt.strftime('%Y-%m-%d')
    tweet_data = tweet_data.rename(columns={'DateTime': 'Date', 'Text': 'tweet_content'})
    tweet_data['Date'] = date_time.date.today().strftime('%Y-%m-%d')
    return tweet_data


print(process_data())
