"""
importer.py

Code for taking a post in browsemyreddit and shoving it into the database and 
helper functions for importing other Reddit-provided data
"""

import re
import praw
from datetime import datetime

import logging
log = logging.getLogger('bmrstatbot')

from bmr_statbot import database, orm
from bmr_statbot.reddit import reddit

def chop_multireddit_url(url):
    """Given a multireddit URL, return a set of names of all subreddits specified"""
    
    # Apparently, multireddit URLs can contain extraneous slashes
    match = re.search('reddit.com/+r/+(\S+\+[^/]*)/*', url)
    if not match:
        raise InvalidMultiredditUrl
    
    url_list = match.group(1)
    result_set = set(url_list.split('+'))
    
    return result_set

def get_user_object(reddit_user, sess):
    """Given the PRAW user object, return a statbot user object"""
    
    sess = database.Session()
    
    user = (sess.query(orm.User)
                .filter(orm.User.id == reddit_user.id)
                .first())     
    sess.close()
    
    if user is None:
        user = orm.User()
        user.name = reddit_user.name
        user.id = reddit_user.id
        
    return user

def get_subreddit_object(sub_name, sess):
    """Return a subreddit object corresponding to the given name
    
    Subreddits names have canonical capitalization but are otherwise case 
    insensitive in places like URLs. For known subreddits we fetch the
    subreddit object (which contains the canonical name); for unknown subreddits
    we ask Reddit. 
    
    """
    
    subreddit =  (sess.query(orm.Subreddit)
                      .filter(orm.Subreddit.name.ilike(sub_name))
                      .first())
    
    if subreddit is None:
        log.debug('Subreddit miss: {0}'.format(sub_name))
        try:
            reddit_sub = reddit.get_subreddit(sub_name)
            
            subreddit = orm.Subreddit()
            # because of PRAW issue #236 this has to go first
            subreddit.id = reddit_sub.id
            subreddit.name =  reddit_sub.display_name
            
        except praw.errors.InvalidSubreddit:
            log.info('Attempted to fetch invalid subreddit: {0}'.format(sub_name))
            subreddit = None
        except Exception as e:
            # TODO: Figure actual exceptions that can happen here. For now, just
            # log the exception, skip, and hope that it didn't have anything to
            # do with stuff being on fire.
            log.error('Error looking up subreddit {0}: {1}'
                      .format(sub_name, e))
            subreddit = None
    else:
        log.debug('Subreddit hit: {0}'.format(sub_name))
    return subreddit
   
   
    
def scrape_user_post(submission):
    """Imports a user's post into the database"""
       
    sess = database.Session()
    
    # do this first so we raise an exception if URL is wrong and not continue
    sub_names = chop_multireddit_url(submission.url)
    
    # check to see if we don't already have the post
    post = (sess.query(orm.Post)
                      .filter(orm.Post.id == submission.id)
                      .first())
                      
    if post is not None:
        sess.close()
        raise PostAlreadyThere
    
    if submission.author is None:
        # Note that PRAW reports '[deleted]' authors as None
        sess.close()
        raise DeletedPost
    
    # post 
    post = orm.Post()
    post.id = submission.id
    post.date = datetime.utcfromtimestamp(submission.created_utc)
    post.user = get_user_object(submission.author, sess)
    
    # subreddits - this can take a while...
    for sub_name in sub_names:
        subreddit = get_subreddit_object(sub_name, sess)
        if (subreddit is not None
            and subreddit not in post.subreddits):
            
            post.subreddits.append(subreddit)
    
    sess.close()
    return post    
    
class InvalidMultiredditUrl(Exception):
    """Indicates the supplied URL is not a valid multireddit URL
    
    "Multireddit" here refers to the old style urls containing several
    subreddits separated by plus signs: ``/r/example+another_example+3rdexample``.
    It does not refer to the new multireddit feature introduced in July 2013
    
    """
    pass
    
class PostAlreadyThere(Exception):
    pass

class DeletedPost(Exception):
    pass