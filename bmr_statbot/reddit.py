"""reddit.py

The shared praw object
"""

import praw 

from bmr_statbot import config

reddit = praw.Reddit(config.user_agent)

if config.reddit_user is not None:
    reddit.login(config.reddit_user, config.reddit_pass)

# reddit.config.log_requests = 1
