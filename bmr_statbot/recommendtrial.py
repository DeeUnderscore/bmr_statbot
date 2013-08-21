""" 
recommendtrial.py

A simple script that spits out recommendations for a randomly selected user in
the database. Mainly useful for testing. 
"""

from bmr_statbot import recommender, orm, database
from  sqlalchemy.sql.expression import func

rec = recommender.Recommender()
mr = rec.mahout_recommender

sess = database.Session()

result = sess.query(orm.User).order_by(func.random()).first()

print 'user: {0}'.format(result.name)

print '-- current subs:'

for subreddit in result.latest_post.subreddits:
    print subreddit.name
    
recs = mr.getRecommendsFor(result.id, 5)

print '-- Recommendations:'

for rec in recs:
    rec_id = recommender.to_base36(rec.getItemID())
    rec_val = str(rec.getValue())
    sub = sess.query(orm.Subreddit).filter_by(id=rec_id).one()
    print sub.name + ' ' + rec_val
