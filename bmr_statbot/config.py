"""config.py

Configuration
"""

import ConfigParser

cp = ConfigParser.ConfigParser()
cp.read('config/config.ini')

# database configuration
db_user = cp.get('database', 'user')
db_password = cp.get('database', 'password')
db_address = cp.get('database', 'address')
db_name = cp.get('database', 'name')

bmr_name = cp.get('reddit', 'bmr_name')

# Reddit username and password
reddit_user = cp.get('reddit', 'user')
reddit_pass = cp.get('reddit', 'password')

user_agent = cp.get('reddit', 'user_agent')

# Default subreddits. Could probably use migrating to config.ini, too
default_subreddits = [
    'adviceanimals',
    'AskReddit',
    'aww',
    'bestof',
    'books',
    'earthporn',
    'explainlikeimfive',
    'funny',
    'gaming',
    'gifs',
    'IAmA',
    'movies',
    'music',
    'news',
    'pics',
    'science',
    'technology',
    'television',
    'todayilearned',
    'videos',
    'worldnews',
    'wtf'
]

recommend_count = cp.getint('recommender', 'recommend_count')

# How long to wait for new posts.
sleep_time = cp.getint('scraper', 'sleep_time')  

# Number of submissions to go through before giving up searching 
# In order to find submissions newer or older than submission x, we have to go 
# through the new queue until we find submission x, and then go up or down the 
# list. This setting controls how soon we give up if we can't find submission x.
give_up_search_after = cp.getint('scraper', 'give_up_search_after') 

reply_template ="""Hi, I'm a bot. Here is some stuff:

## This post
* Subreddits subscribed to: **{sub_count}**
    * {std_dev_string}
* **{default_count}** of those are defaults

## Recommendations
Based on your subscriptions, here are some recommendations:

{recommendations}

(for more information on this bot see /r/bmr_statbot)
"""
