"""
stats.py

Calculate various stats from the data in the database
"""

from __future__ import division
from math import sqrt

from sqlalchemy import select, func, desc

from bmr_statbot import orm, database, config

tbl = orm.Base.metadata.tables

def users_per_sub():
    """Count the number of subscribers per each subreddit
    
    This function counts the number of self-reported subscribers per each
    subreddit in the database. This includes latest posts for each user only.
    
    Returns a sorted list of tuples, in (subreddit_name, subscriber_count) format. 
    
    """
    
    conn = database.engine.connect()
    
    subreddits = tbl['subreddits']
    
    query = (select([subreddits, func.count().label('count')])
             .where(subreddits.c.id == orm.pref_view.c.subreddit)
             .group_by(subreddits.c.id)
             .order_by(desc('count')))
    
    result = conn.execute(query)
    
    all_tuples = [(row[1], int(row[2])) for row in result.fetchall()]
    
    conn.close()
    result.close()
    
    return all_tuples
    
def subscription_counts():
    """Count the number of subreddits per each user
    
    This function counts how many subreddits each subscriber is subscribed to
    
    """
    
    conn = database.engine.connect()
    
    users = tbl['users']
    
    query = (select([users, func.count().label('count')])
             .where(users.c.id == orm.pref_view.c.id)
             .group_by(users.c.id)
             .order_by(desc('count')))
    
    result = conn.execute(query)
    
    
    all_tuples = [(row['username'], int(row['count'])) for row in result.fetchall()]
     
    conn.close()
    result.close()
     
    return all_tuples

def average_subscriptions():
    """Calculate the average number of subreddits everyone subscribes to
    
    Returns a tuple of (mean, standard_deviation)
    
    """
    
    sub_counts = [x for (_,x) in subscription_counts()]
    
    mean = sum(sub_counts)/len(sub_counts)
    
    std_dev = sqrt(sum(map(lambda x: (x-mean)**2, sub_counts))
                   /len(sub_counts))
    
    return (mean, std_dev)

def number_defaults(subreddits):
    """Given a list of subreddits, determine how many defaults they are subscribed to"""
    
    count = 0
    
    for subreddit in subreddits:
        if subreddit.name in config.default_subreddits:
            count += 1
    
    return count