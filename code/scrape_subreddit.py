import requests
import pandas as pd
import time

import api_init

headers = api_init.init()

r_python_url = 'http://oauth.reddit.com/r/python/new'
params={'limit':100}
n_iter = 80

features = ['subreddit', 'selftext', 'author', 'title', 'created_utc', 'url', 'downs', 'ups', 'num_comments']
df = pd.DataFrame()

start = time.time()
for i in range(n_iter):
    print(f'Iter {i}: {time.time() - start:.3f}s')
    res = requests.get(r_python_url, headers=headers, params=params)
    for post in res.json()['data']['children']:
        df = df.append({key : post['data'][key] for key in features}, 
                        ignore_index=True)
    uid = post['kind'] + post['data']['id']
    params['after'] = uid

    time.sleep(1)

df.to_csv('subreddit_posts.csv', index=False)