import praw
import csv
import sqlite3
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env.local
load_dotenv(dotenv_path='.env.local')

def main():
   
    # Create reddit instance
    reddit = praw.Reddit(
        client_id=os.getenv("client_id"),
        client_secret=os.getenv("client_secret"),
        user_agent=os.getenv("user_agent")
                )
    
    # Define the path to the database
    db_path = '/usr/src/app/data/reddit_comments.db'
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            submission_id TEXT,
            submission_title TEXT,
            comment_id TEXT PRIMARY KEY,
            comment_parent_id TEXT,
            comment_body TEXT,
            comment_score INTEGER,
            comment_author TEXT,
            comment_created_utc REAL,
            comment_edited REAL,
            subreddit_name TEXT,
            query_timestamp REAL
        )
    ''')
    conn.commit()
    subreddit_names = ["learnpython", "math", "memes"]  # Add more subreddits as needed
    
    for subreddit_name in subreddit_names:
        # Create the subreddit object
        subreddit = reddit.subreddit(subreddit_name)
        
        # Retrieve the latest 100 submissions (posts)
        submissions = subreddit.new(limit=100)
        
        query_timestamp = time.time()
        print(f"Query timestamp: {query_timestamp} for subreddit: {subreddit_name}")
        
        for submission in submissions:
            # By default, PRAW may not load all comments, so call replace_more
            submission.comments.replace_more(limit=None)
            
            # Access each comment in the submission
            for comment in submission.comments.list():
                # Some fields
                comment_id = comment.id
                comment_parent_id = comment.parent_id
                comment_body = comment.body
                comment_score = comment.score
                comment_author = str(comment.author) if comment.author else "[deleted]"
                comment_created_utc = comment.created_utc
                comment_edited = comment.edited  # can be False or a timestamp
                
                # Insert comment data into the database
                cursor.execute('''
                    INSERT OR REPLACE INTO comments (
                        submission_id,
                        submission_title,
                        comment_id,
                        comment_parent_id,
                        comment_body,
                        comment_score,
                        comment_author,
                        comment_created_utc,
                        comment_edited,
                        subreddit_name,
                        query_timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    submission.id,
                    submission.title,
                    comment_id,
                    comment_parent_id,
                    comment_body,
                    comment_score,
                    comment_author,
                    comment_created_utc,
                    comment_edited,
                    subreddit_name,
                    query_timestamp
                ))
                conn.commit()
        time.sleep(60)

if __name__ == "__main__":
    main()
