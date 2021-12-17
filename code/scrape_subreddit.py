import requests
import pandas as pd
import time

from code import api_init

# api request vars
headers = api_init.init()
r_python_url = 'http://oauth.reddit.com/r/python/new'
params={'limit':100}

# data collection vars
features = ['subreddit', 'selftext', 'author', 'title', 'created_utc', 'url', 'downs', 'ups', 'num_comments']
df = pd.DataFrame()
n_iter = 80

# init timer and iterate n times
start = time.time()
for i in range(n_iter):
    print(f'Iter {i}: {time.time() - start:.3f}s')

    # get posts from given subreddit
    res = requests.get(r_python_url, headers=headers, params=params)

    # collect data
    for post in res.json()['data']['children']:
        df = df.append({key : post['data'][key] for key in features}, 
                        ignore_index=True)

    # construct id for next api request
    uid = post['kind'] + post['data']['id']
    params['after'] = uid

    # wait to avoid api call limits
    time.sleep(1)

# save data
df.to_csv('data/subreddit_posts.csv', index=False)