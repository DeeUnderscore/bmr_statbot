"""objects.py

Classes representing subreddits, users, etc.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

post_subs = Table('post_subs', Base.metadata,
    Column('post', String, ForeignKey('posts.id'), primary_key=True),
    Column('subreddit', String, ForeignKey('subreddits.id'), primary_key=True)
)

# just shoving this in here, although it's not really used by the ORM
pref_view = Table('view_user_pref', Base.metadata,
    Column('id', String, ForeignKey('users.id')),
    Column('subreddit', String, ForeignKey('subreddits.id')))


class Subreddit(Base):
    """A subreddit
    
    The name is the subreddit's display_name as seen in about.json for it, with 
    capitalization. Subreddit names are generally case-insensitive. 
    
    """
    
    __tablename__ = 'subreddits'
    
    id = Column('id', String, primary_key=True) # use Reddit's id
    name = Column('name', String, index=True, unique=True)
    
    def __repr__(self):
        return "Subreddit(id={0}, name='{1}')".format(self.id, self.name)
    
class Post(Base):
    """A single post listing subreddits
    
    A user may have more than one post, meaning more than one set of
    subscriptions. "Post" here means one self-reported set of subscriptions.
    
    """
    
    __tablename__ = 'posts'
    
    id = Column('id', String, primary_key=True) # use Reddit's id 
    date = Column('date', DateTime)
    user_id = Column('user', ForeignKey('users.id'))
    responded = Column('responded', Boolean, default=False) # True if we posted here
    
    subreddits = relationship('Subreddit', secondary=post_subs)
    
    def __repr__(self):
        return "Post(id={0})".format(self.id)
    
class User(Base):
    """A single user and their posts"""
    
    __tablename__ = 'users'
    
    id = Column('id', String, primary_key=True) # use Reddit's id
    name = Column('username', String, index=True, unique=True) 
    latest_post_id = Column('latest_post', String,
                            ForeignKey('posts.id',
                                       use_alter=True,
                                       name='users_latest_post_fkey'))
    
    # For the sake of simplicity and making this whole ORM way harder than it 
    # has to be, we keep a latest_post column in User. This could otherwise be
    # retrieved by  ordering user's posts by date
    latest_post = relationship(Post,
                               primaryjoin=(latest_post_id == Post.id),
                               post_update=True)
    
    posts = relationship(Post, primaryjoin=
                                    (id == Post.user_id),
                         backref='user',
                         order_by=Post.date.desc())
    
    def __repr__(self):
        return "User(id={0}, username='{1}')".format(self.id, self.name)
    
    def check_latest_post(self, post):
        """Checks if the given post is the user's latest post"""
        
        if post.user is not self:
            # other user's post is never going to be this user's latest
            return False 
        
        if self.latest_post is None:
            return True 
        
        # TODO: Use SQL sorting
        for old_post in self.posts:
            if old_post is post:
                continue
            
            if (post.date <= old_post.date):
                # if one of the existing posts is newer
                return False
        
        return True

    
    