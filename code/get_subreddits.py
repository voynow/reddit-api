import requests
import pandas as pd
import time

from code import api_init

# API request vars
headers = api_init.init() 
subreddits_url = 'http://oauth.reddit.com/subreddits/'
params = {'limit':100}

# get request
res = requests.get(subreddits_url, headers=headers, params=params)

# data collection vars
keys = ['url', 'subscribers', 'description']
df = pd.DataFrame()

# iter over all child objects
for child in res.json()['data']['children']:
    subreddit_dict = child['data']

    # collect subreddit url, subs, and description
    df = df.append(
        {key : subreddit_dict[key] for key in keys}, 
        ignore_index=True)

# save to csv
df.to_csv('data/subreddits.csv', index=False)