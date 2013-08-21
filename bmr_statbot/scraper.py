"""scraper.py

Code for crawling through BrowseMyReddit in what looks like organized fashion
"""

from sqlalchemy import MetaData, Table, String, Column
from sqlalchemy import select, update

import logging
log = logging.getLogger('bmrstatbot')

from bmr_statbot import database, importer, config, poster
from bmr_statbot.reddit import reddit

metadata = MetaData()

kvstore = Table('kvstore', metadata,
                Column('key', String, primary_key=True),
                Column('value', String))

class BMRScraper(object):
    """Allows for persisting and resuming BMR scraping state"""
       
    def __init__(self, init_poster=True):
        """Create a new Scraper object
        
        If *init_poster* is set to False, the Poster object will not be 
        initialized. If that is the case, the Recommender object will not be 
        initialized either, which is convenient if the Java portion of the bot
        isn't running.  
        
        """
        self._head = None
        self._tail = None 
        self.writethrough = True 
        
        if init_poster:
            self.poster = poster.Poster()
        else:
            self.poster = None
        
    
    def _database_getter(attr):  # @NoSelf
        def get(self):
            requested =  getattr(self, '_{}'.format(attr))
            
            if requested is None:
                query = (select([kvstore])
                         .where(kvstore.c.key == 'scrape_{0}'.format(attr)))
                
                conn = database.engine.connect()
                result_set = conn.execute(query)
                result = result_set.fetchone()
                result_set.close()
                conn.close()
                
                setattr(self, '_{}'.format(attr), result[kvstore.c.value])
                
                requested = result[kvstore.c.value]
                
            return requested
            
        return get
           
    def _database_setter(attr):  # @NoSelf
        def set_(self, value):            
            setattr(self, '_{}'.format(attr), value)
            
            if self.writethrough:
                self.persist(attr)
                
        return set_
    
    
    # The newest (by date) post scraped
    head = property(_database_getter('head'), _database_setter('head')) 
    # The oldest (by date) post scraped
    tail = property(_database_getter('tail'), _database_setter('tail')) 
            
    def persist(self, what):
        """Writes the value of head or tail back to the db"""
        
        value = getattr(self, '_{0}'.format(what))

        query = (kvstore.update()
                        .where(kvstore.c.key == 'scrape_{0}'.format(what))
                        .values(value=value))
        
        conn = database.engine.connect() 
        result = conn.execute(query)
        result.close()
        conn.close()          
                
    def scrape_posts_down(self, limit=None):
        """Go downwards through the post list and scrape posts one by one
        
        This function goes down the list - from newer towards older posts
        
        limit - stop scraping after this many submissions
        
        """                     
        
        sub_iter = iter(reddit.get_subreddit(config.bmr_name)
                        .get_new(limit=None))
        current = sub_iter.next()
        
        # if we don't have a head set, we start from the very top 
        if self.tail is None:
            self.head = current.id
            log.debug('Scraping down. Starting at first post seen: {0}'.format(current.id)) 
        else:
            number_seen = 0
            log.debug('Scraping down. Looking for tail: {0}'.format(self.tail))
            while current.id != self.tail:
                
                try:
                    current = sub_iter.next()
                except StopIteration:
                    log.info('Reached end of list without finding tail.')
                    raise UnableToFindSubmission

                number_seen += 1
                
                if number_seen >= config.give_up_search_after:
                    raise UnableToFindSubmission
            try:
                current = sub_iter.next()
            except StopIteration:
                log.info('No more posts after tail.')
                raise UnableToFindSubmission
        
        number_seen = 0 
           
        while True:
            if limit is not None and number_seen >= limit:
                log.info('Limit reached, stopping.')
                break
        
            scrape_one_post(current)
            
            self.tail = current.id 
            
            try:
                current = sub_iter.next()
            except StopIteration:
                log.info('Ran out of posts to parse, stopping')
                return

            number_seen += 1
            
    def scrape_posts_up(self, reply=False):
        """Go upwards through the post list and scrape posts one by one
        
        This function goes up the list - from older towards newer posts. This 
        function does not take a limit, and instead the amount of submissions
        which will be parsed depends on config.give_up_search_after. If reply is
        set to True, it will also reply to the posts as it scrapes them. 
        
        """    
        
        # Since we scrape up from head, if we have no head we got nothing
        # to scrape
        if self.head is None:
            return
        
        # If we haven't initialized the poster, and were asked to reply, we have
        # to initialize it at this point
        if reply and self.poster is None:
            self.poster = poster.Poster()
        
        log.debug('Scraping up. Looking for head: {0}'.format(self.head))                 
     
        sub_iter = iter(reddit.get_subreddit(config.bmr_name)
                        .get_new(limit=None))
        submissions = [sub_iter.next()]   
        
        number_seen = 0
        
        while submissions[-1].id != self.head:
                
            try:
                submissions.append(sub_iter.next())
            except StopIteration:
                log.info('Reached end of list without finding head.')
                raise UnableToFindSubmission
    
            number_seen += 1
            
            if number_seen >= config.give_up_search_after:
                raise UnableToFindSubmission
            
        del submissions[-1] # don't scrape head again 
        
        submissions.reverse()
        
        for submission in submissions:
            if reply:
                try:
                    self.poster.reply_to_post(submission)
                except poster.AlreadyReplied:
                    log.error('Attempted to reply to {0} twice.'.format(submission.id))
            else:
                scrape_one_post(submission)
        
            self.head = submission.id


def scrape_one_post(submission):
    """Scrape one post"""
    
    try:
        sess = database.Session()
        
        log.debug('Attempting to scrape post {0}'.format(submission.id))
        post = importer.scrape_user_post(submission)
        
        sess.add(post)
        if post.user.check_latest_post(post):
            post.user.latest_post = post
        
        sess.commit()
        
        log.info('Imported post {0}.'.format(submission.id))
    except importer.InvalidMultiredditUrl:
        log.info('Skipping post {0}: Not a multireddit URL.'
                 .format(submission.id))
    except importer.PostAlreadyThere:
        log.error('Skipping post {0}: Post already in database'
                  .format(submission.id))
    except importer.DeletedPost:
        log.error('Skipping post {0}: Appears deleted.'
                  .format(submission.id))
        
    sess.close()


class UnableToFindSubmission(Exception):
    pass           