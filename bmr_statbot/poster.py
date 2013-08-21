"""poster.py

Component for replying and posting to Reddit
"""
from bmr_statbot import importer, database, stats, orm
import bmr_statbot.recommender
from bmr_statbot import config as cfg

import logging
log = logging.getLogger('bmrstatbot')


class Poster(object):
    """Object capable of replying to posts with statistics"""
    
    def __init__(self):
        self.recommender = bmr_statbot.recommender.Recommender()

    def reply_to_post(self, submission):
        """Reply to post with statistics and recommendations
        
        Note that this function will only emit proper recommendations when
        replying to the user's latest post. Otherwise, it will still spit out
        recommendations, but they will be based upon the user's latest post, and
        not the post replied to. 
        
        """
        
        try:
            sess = database.Session()
            log.debug('Attempting to add and then reply: {0}'.format(submission.id))
    
            
            post = importer.scrape_user_post(submission)
            sess.add(post)
            
            if post.user.check_latest_post(post):
                post.user.latest_post = post
            
            sess.commit()
            
        except importer.InvalidMultiredditUrl:
            log.info('Skipping post {0}: Not a multireddit URL.'
                     .format(submission.id))
            return
        except importer.DeletedPost:
            log.error('Skipping post {0}: Appears deleted.'
                      .format(submission.id))
            return
        except importer.PostAlreadyThere:
            # continue with the rest, but update instead of insert
            post = sess.query(orm.Post).filter_by(id=submission.id).one()
        
            
        if post.responded:
            log.info('Skipping post {0}: Already replied.'.format(post.id))
            raise AlreadyReplied
          
        count = len(post.subreddits)
       
        self.recommender.mahout_recommender.refreshRecommender()
        recs = self.recommender.mahout_recommender.getRecommendsFor(post.user.id, cfg.recommend_count)
    
        reply = cfg.reply_template.format(
                    sub_count=count,
                    std_dev_string=self._std_dev_string(count),
                    default_count=stats.number_defaults(post.subreddits),
                    recommendations=self._recommendations_string(recs, sess))
            
        try:         
            submission.add_comment(reply)
        except Exception as e: 
            log.error('Problem while replying to {0}: {1}'.format(post.id, e))
        else:
            post.responded = True
            sess.commit()
            log.info('Replied to post {0} (user: {1})'.format(post.id, post.user.name))    
        finally:
            sess.close()
     
    def _std_dev_string(self, count):
        """Generate the std_dev_string for use in reply_to_post()"""
        
        mean, std_dev = stats.average_subscriptions()
        diff = abs(mean - count)
        
        std_devs = diff / std_dev
        
        return ('{a:g} standard deviations {dir} mean of {mean:g}'
                .format(a=std_devs,
                        dir='below' if count < mean else 'above',
                        mean=mean))
        
    def _recommendations_string(self, recs, sess):
        """Generate a list of recommendations in a string from the proxied Java object
        
        The passed session is used to fetch subreddit names
        
        """
        
        rec_strings = []
        
        for rec in recs:
            rec_val = float(rec.getValue())
            sub = (sess.query(orm.Subreddit)
                   .filter_by(id=bmr_statbot.recommender.to_base36(rec.getItemID()))
                   .one()).name
            
            rec_strings.append('* /r/{0} ({1:g})'.format(sub, rec_val))
            
        return '\n'.join(rec_strings)
    
class AlreadyReplied(Exception):
    pass