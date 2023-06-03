import csv
import datetime
import time
import requests

start_date = datetime.datetime(2022, 12, 15)
end_date = datetime.datetime(2023, 5, 20)

subreddits = ['bitcoin',
              'bitcoinmarkets',
              'cryptocurrency',
              'altcoin',
              'cryptomarkets',
              'cryptotrading',
              'bitcoinbeginners',
              'cryptotechnology',
              'bitcoinmining',
              'cryptocurrencytrading',
              'cryptocurrencyinvesting',
              'cryptocurrencies',
              'bitcoinstocks',
              'cryptoinvestor',
              'bitcoinserious',
              'cryptocurrencynews',
              'bitcointrading',
              'cryptosecurity',
              'bitcoinminingpool',
              'cryptohardware',
              'all']

subreddit_index = 0


def get_next_subreddit(index):
    if 0 <= index < len(subreddits):
        return subreddits[index]
    else:
        return None


with open('reddit_bitcoin_posts_part_1.csv', mode='w', newline='') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['post_id', 'title', 'selftext', 'url', 'author', 'score', 'publish_date', 'num_of_comments',
                     'permalink', 'flair'])
    date = 0
    while date <= (end_date - start_date).days:
        date_str = (start_date + datetime.timedelta(date)).strftime("%Y-%m-%d")
        timestamp = int((start_date + datetime.timedelta(date)).timestamp())

        url = f"https://api.pushshift.io/reddit/search/submission/?q=bitcoin&after={timestamp}&before=" \
              f"{timestamp + 86400}&size=100&subreddit=" \
              f"{'bitcoin' if get_next_subreddit(subreddit_index) is None else get_next_subreddit(subreddit_index)}"

        success = False
        while not success:

            try:
                response = requests.get(url, allow_redirects=True)
            except Exception:
                print("Network exception.. waiting 60 seconds until starts again..")
                time.sleep(60)
                continue

            if response.status_code == 200:
                success = True

                try:
                    data = response.json()['data']
                except Exception:
                    subreddit_index += 1
                    print("Something went wrong with the JSON body, will retry in 5 seconds:" + str(response.content))
                    time.sleep(5)
                    continue

                if len(data) == 0 and len(subreddits) > subreddit_index:
                    print(
                        f"No Reddit posts found for {date_str}. Trying with a different subreddit: "
                        f"{get_next_subreddit(subreddit_index)}")
                    subreddit_index += 1
                    continue
                else:
                    subreddit_index = 0

                for post in data:
                    title = post.get('title', '')
                    url = post.get('url', '')
                    flair = post.get('link_flair_text', '')
                    author = post.get('author', '')
                    sub_id = post.get('id', '')
                    score = post.get('score', 0)
                    selftext = post.get('selftext', '')
                    if selftext in ['[removed]', '[deleted]']:
                        selftext = ''
                    created = datetime.datetime.fromtimestamp(post['created_utc']) if 'created_utc' in post else ''
                    numComms = post.get('num_comments', 0)
                    permalink = post.get('permalink', '')

                    try:
                        writer.writerow([sub_id, title, selftext, url, author,
                                         score, created, numComms, permalink, flair])
                    except UnicodeEncodeError as error:
                        subreddit_index += 1
                        print("Error writing the entry. Skipping it so that it can continue.")
                        pass  # Skip the entry if an error occurs

                print(f"Fetched and wrote {len(data)} Reddit posts for {date_str} to the CSV file.")
                date += 1  # Advance to the next date
                if len(data) == 0:
                    print(f"Writing empty entry to the CSV file for this date: {date_str}.")
                    index_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')

                    # Format the datetime object as a string in the desired format
                    formatted_date = index_date.strftime('%Y-%m-%d %H:%M:%S')
                    writer.writerow(['', '', '', '', '',
                                     0, formatted_date, 0, '', ''])
            else:
                print(
                    f"Failed to fetch data from the API for {date_str}. Status code: {response.status_code}."
                    f" Retrying in 1 minute...")
                time.sleep(60)

print("Done! The Download is complete")
