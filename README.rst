BrowseMyReddit Statistics Bot (bmr-statbot)
===========================================

The bmr-statbot is a series of scripts meant to scrape data from the subreddit 
`/r/BrowseMyReddit`_ (a board on the social news and discussion website 
Reddit_), and then generate statistics or other useless information.

Dependencies
------------
* SQLAlchemy 0.8.2 (with Postgres)
* PRAW 2.1.4

* Mahout 0.9 (svn)
* Ini4J 0.5.2 
* postgresql-jdbc 9.1 Build 903

Running
-------
The SQLAlchemy objects in ``orm.py`` can be used to generate the requisite tables. 
``/sql/view_user_pref.sql`` can be used to generate the view that the Mahout 
recommender expects to be there. Configuration is done via ``config/config.ini``,
with an example provided in that folder. 

Figuring out the classpath and Mahout is left an exercise to the reader, mostly 
because I don't know anything about Maven. 

The ``misc`` folder contains a csv file with the ids and names for 100 top
subreddits. This may be useful to bootstrap a DB.

See ``bmr_statbot/runner.py`` for an example of how to run the bot. 

.. _/r/BrowseMyReddit: http://www.reddit.com/r/browsemyreddit
.. _Reddit: http://www.reddit.com
