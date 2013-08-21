-- View: view_user_pref
-- This is used to generate a pairs of users and their subscriptions for use with Mahout

CREATE OR REPLACE VIEW view_user_pref AS 
 SELECT users.id, post_subs.subreddit
   FROM users, posts, post_subs
  WHERE users.latest_post::text = posts.id::text AND post_subs.post::text = posts.id::text;

ALTER TABLE view_user_pref
  OWNER TO bmrstatbot;

