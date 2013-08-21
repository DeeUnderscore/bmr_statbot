WITH user_pref AS (
 SELECT users.id, post_subs.subreddit
   FROM users, posts, post_subs
  WHERE
       posts.date > DATE '2013-08-13'
       AND users.latest_post::text = posts.id::text 
       AND post_subs.post::text = posts.id::text;
)
SELECT 
 subreddits.name, count(*) AS count
FROM
  subreddits, user_pref, posts
WHERE
  posts.
  subreddits.id = user_pref.subreddit GROUP BY subreddits.id
  ORDER BY count DESC;