# Imports
import pandas as pd
import flair
from textblob import TextBlob
from tqdm import tqdm
import os
import datetime
import numpy as np
import nltk

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initializing the sentiment analyzer
flair_sentiment = flair.models.TextClassifier.load('en-sentiment')
fmt = '%Y-%m-%d %H:00:00'
sid = SentimentIntensityAnalyzer()


# This Python method takes a sentiment value in the format of [NEGATIVE (0.928)]
# and returns a positive or negative float value based on the sentiment polarity.
# The method converts the input sentiment value to a string,
# extracts the sentiment score, and returns a float value that is either
# positive or negative based on the sentiment polarity.
def get_sentiment_val_for_flair(sentiments):
    """
    parse input of the format [NEGATIVE (0.9284018874168396)] and return +ve or -ve float value
    :param sentiments:
    :return:
    """
    total_sentiment = str(sentiments)
    neg = 'NEGATIVE' in total_sentiment
    if neg:
        total_sentiment = total_sentiment.replace('NEGATIVE', '')
    else:
        total_sentiment = total_sentiment.replace('POSITIVE', '')

    total_sentiment = total_sentiment.replace('(', '').replace('[', '').replace(')', '').replace(']', '')

    words = total_sentiment.split()

    if len(words) > 0:
        score = words[-1]
    else:
        score = 0
    val = float(score)
    if neg:
        return -val
    return val


# This function that analyzes the sentiment of Reddit posts and saves
# the results to a file. It takes in two file names,
# input_filename and output_filename, both in CSV format.
def get_sentiment_report(input_filename, output_filename):
    df = pd.read_csv(input_filename, encoding='mac_roman')
    df = df[['title', 'selftext', 'publish_date']]
    df = df.fillna('')

    df['text'] = df['title'] + ' ' + df['selftext']
    df.set_index('publish_date', inplace=True)
    df.drop(['title', 'selftext'], axis=1, inplace=True)

    total_rows = len(df)
    progress_bar = tqdm(total=total_rows, unit='row')

    for row_i, row in df.iterrows():
        tb_sentiment_polarity_dict = dict()
        tb_sentiment_subjectivity_dict = dict()
        flair_sentiment_dict = dict()

        sid_pos_dict = dict()
        sid_neg_dict = dict()
        sid_neu_dict = dict()
        sid_com_dict = dict()

        data = row['text']
        flair_s = flair.data.Sentence(data)
        flair_sentiment.predict(flair_s)
        flair_total_sentiment = flair_s.labels
        flair_val = get_sentiment_val_for_flair(flair_total_sentiment)

        flair_sentiment_dict[str(row_i)] = flair_val
        tb_sentiment_polarity_dict[str(row_i)] = TextBlob(data).sentiment[0]
        tb_sentiment_subjectivity_dict[str(row_i)] = TextBlob(data).sentiment[1]

        ss = sid.polarity_scores(data)
        sid_pos_dict[str(row_i)] = ss['pos']
        sid_neg_dict[str(row_i)] = ss['neg']
        sid_neu_dict[str(row_i)] = ss['neu']
        sid_com_dict[str(row_i)] = ss['compound']

        flair_df = pd.DataFrame.from_dict(flair_sentiment_dict, orient='index', columns=['reddit_flair'])
        flair_df.index.name = 'timestamp'

        tb_polarity_df = pd.DataFrame.from_dict(tb_sentiment_polarity_dict, orient='index',
                                                columns=['reddit_tb_polarity'])
        tb_polarity_df.index.name = 'timestamp'

        tb_subjectivity_df = pd.DataFrame.from_dict(tb_sentiment_subjectivity_dict, orient='index',
                                                    columns=['reddit_tb_subjectivity'])
        tb_subjectivity_df.index.name = 'timestamp'

        sid_pos_df = pd.DataFrame.from_dict(sid_pos_dict, orient='index',
                                            columns=['reddit_sid_pos'])
        sid_pos_df.index.name = 'timestamp'

        sid_neg_df = pd.DataFrame.from_dict(sid_neg_dict, orient='index',
                                            columns=['reddit_sid_neg'])
        sid_neg_df.index.name = 'timestamp'

        sid_neu_df = pd.DataFrame.from_dict(sid_neu_dict, orient='index',
                                            columns=['reddit_sid_neu'])
        sid_neu_df.index.name = 'timestamp'

        sid_com_df = pd.DataFrame.from_dict(sid_com_dict, orient='index',
                                            columns=['reddit_sid_com'])
        sid_com_df.index.name = 'timestamp'

        final_senti_df = pd.concat([flair_df, tb_polarity_df, tb_subjectivity_df, sid_pos_df, sid_neg_df, sid_neu_df,
                                    sid_com_df], axis=1)

        if os.path.exists(output_filename):
            keep_header = False
        else:
            keep_header = True

        final_senti_df.to_csv(output_filename, mode='a', header=keep_header)

        progress_bar.update(1)  # Update the progress bar

    progress_bar.close()  # Close the progress bar

    return


def clean_sentiment_report(input_filename, output_filename):
    # drop duplicates and sort
    master_df = pd.read_csv(input_filename, index_col=0)
    master_df.index = pd.to_datetime(master_df.index)
    idx = np.unique(master_df.index, return_index=True)[1]
    master_df = master_df.iloc[idx]
    master_df.to_csv(output_filename)


def bucketize_sentiment_report(input_filename, output_filename):
    start_date_time_obj = datetime.datetime(2010, 7, 17, 0)
    end_date_time_obj = datetime.datetime(2023, 5, 16, 0)
    hr1 = datetime.timedelta(hours=1)
    curr_date_time_obj = start_date_time_obj
    in_df = pd.read_csv(input_filename)

    out_dict = dict()

    while curr_date_time_obj <= end_date_time_obj:
        curr_timestamp = curr_date_time_obj.strftime(format=fmt)
        out_dict[curr_timestamp] = 0
        curr_date_time_obj += hr1

    out_df = pd.DataFrame.from_dict(out_dict, orient='index',
                                    columns=['reddit_flair'])

    out_df.index.name = 'timestamp'
    # Populate more colums
    out_df['reddit_flair_count'] = 0
    out_df['reddit_tb_polarity'] = 0
    out_df['reddit_tb_polarity_count'] = 0
    out_df['reddit_tb_subjectivity'] = 0
    out_df['reddit_tb_subjectivity_count'] = 0
    out_df['reddit_sid_pos'] = 0
    out_df['reddit_sid_neg'] = 0
    out_df['reddit_sid_neu'] = 0
    out_df['reddit_sid_com'] = 0
    out_df['reddit_sid_count'] = 0

    for i in range(len(in_df)):
        timestamp = in_df.loc[i, 'timestamp']
        try:
            out_key = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                out_key = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M')
            except:
                raise ValueError(f"Timestamp '{timestamp}' does not match expected format.")

        # Timestamp is current plus few minutes or seconds, so collect all these data in the bucket of next hour
        out_key += hr1
        out_key = out_key.strftime(format='%Y-%m-%d %H:00:00')
        # Add up all values and count how many values we have added. In next pass we would normalize the values
        try:
            out_df.loc[out_key, 'reddit_flair'] += in_df.loc[i, 'reddit_flair']
            out_df.loc[out_key, 'reddit_flair_count'] += 1
            out_df.loc[out_key, 'reddit_tb_polarity'] += in_df.loc[i, 'reddit_tb_polarity']
            out_df.loc[out_key, 'reddit_tb_polarity_count'] += 1
            out_df.loc[out_key, 'reddit_tb_subjectivity'] += in_df.loc[i, 'reddit_tb_subjectivity']
            out_df.loc[out_key, 'reddit_tb_subjectivity_count'] += 1
            out_df.loc[out_key, 'reddit_sid_pos'] += in_df.loc[i, 'reddit_sid_pos']
            out_df.loc[out_key, 'reddit_sid_neg'] += in_df.loc[i, 'reddit_sid_neg']
            out_df.loc[out_key, 'reddit_sid_neu'] += in_df.loc[i, 'reddit_sid_neu']
            out_df.loc[out_key, 'reddit_sid_com'] += in_df.loc[i, 'reddit_sid_com']
            out_df.loc[out_key, 'reddit_sid_count'] += 1
        except:
            pass

    # <ake timestamp as a column and reindex the dataframe to make loc method happy
    out_df['timestamp'] = out_df.index
    out_df.index = range(len(out_df))

    for i in range(len(out_df)):
        # Normalize the values
        if out_df.loc[i, 'reddit_flair_count'] == 0:
            out_df.loc[i, 'reddit_flair'] = 0
        else:
            out_df.loc[i, 'reddit_flair'] /= out_df.loc[i, 'reddit_flair_count']

        if out_df.loc[i, 'reddit_tb_polarity_count'] == 0:
            out_df.loc[i, 'reddit_tb_polarity'] = 0
        else:
            out_df.loc[i, 'reddit_tb_polarity'] /= out_df.loc[i, 'reddit_tb_polarity_count']

        if out_df.loc[i, 'reddit_tb_subjectivity_count'] == 0:
            out_df.loc[i, 'reddit_tb_subjectivity'] = 0
        else:
            out_df.loc[i, 'reddit_tb_subjectivity'] /= out_df.loc[i, 'reddit_tb_subjectivity_count']

        if out_df.loc[i, 'reddit_sid_count'] == 0:
            out_df.loc[i, 'reddit_sid_pos'] = 0
            out_df.loc[i, 'reddit_sid_neg'] = 0
            out_df.loc[i, 'reddit_sid_neu'] = 0
            out_df.loc[i, 'reddit_sid_com'] = 0
        else:
            out_df.loc[i, 'reddit_sid_pos'] /= out_df.loc[i, 'reddit_sid_count']
            out_df.loc[i, 'reddit_sid_neg'] /= out_df.loc[i, 'reddit_sid_count']
            out_df.loc[i, 'reddit_sid_neu'] /= out_df.loc[i, 'reddit_sid_count']
            out_df.loc[i, 'reddit_sid_com'] /= out_df.loc[i, 'reddit_sid_count']

        if os.path.exists(output_filename):
            keep_header = False
        else:
            keep_header = True

    out_df.drop(['reddit_flair_count', 'reddit_tb_polarity_count', 'reddit_tb_subjectivity_count', 'reddit_sid_count'],
                axis=1,
                inplace=True)
    # Change back index to timestamp to save the data in csv
    out_df.set_index('timestamp', inplace=True)
    out_df.to_csv(output_filename)


def preprocess_reddit_posts():
    input_filename = 'reddit_bitcoin_posts_downloaded.csv'
    output_sentiment_filename = input_filename[0:-4] + '_sentiment.csv'

    # Read input_filename (which can be generated by download_data_from_reddit.py script) and performs
    # Sentiment analyis of the text data
    get_sentiment_report(input_filename, output_sentiment_filename)
    output_sentiment_bucketize_filename = output_sentiment_filename[0:-4] + '_bucketized.csv'

    # Reddit posts can land anytime. Collect all the posts (and its sentiment reports) landed on a given hour (0 to 59
    # minutes) And bucketize them all into the corresponding hour
    bucketize_sentiment_report(output_sentiment_filename, output_sentiment_bucketize_filename)


preprocess_reddit_posts()
