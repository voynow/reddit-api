import requests
import json
import pandas as pd
import time


def api_init():

    auth_json = json.load(open('auth_data.json'))

    CLIENT_ID = auth_json["CLIENT_ID"]
    SECRET_KEY = auth_json["SECRET_KEY"]

    data = {
        'grant_type': 'password',
        'username': auth_json["username"],
        'password': auth_json['password']
    }

    headers = {'User-Agent': 'MyAPI/0.0.1'}

    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

    res = requests.post(
        'https://www.reddit.com/api/v1/access_token',
        auth=auth, 
        data=data, 
        headers=headers)

    TOKEN = res.json()['access_token']
    headers['Authorization'] = f'bearer {TOKEN}'

    return headers


def get_subreddits():
        
    # API request vars
    headers = api_init() 
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


def scrape_subreddit(name):

    # api request vars
    headers = api_init()
    r_python_url = f'http://oauth.reddit.com/{name}/new'
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


get_subreddits()
scrape_subreddit("r/python")