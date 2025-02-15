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
    
    # Define the subreddit you want to scrape
    subreddit_name = "learnpython"  # Change this to the subreddit of your choice
    
    # Create the subreddit object
    subreddit = reddit.subreddit(subreddit_name)
    
    # Retrieve the latest 100 submissions (posts)
    submissions = subreddit.new(limit=100)
    
    db_path = '/usr/src/app/reddit_comments.db'
    if not os.path.exists(db_path):
        open(db_path, 'a').close()
    db_exists = os.path.exists(db_path)
    
    # Ensure the directory for the database exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table only if the database didn't exist
    if not db_exists:
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
    query_timestamp = time.time()
    print(f"Query timestamp: {query_timestamp}")
    
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

    print(f"Comments for the latest 100 posts on r/{subreddit_name} saved to reddit_comments.db")
    conn.close()

if __name__ == "__main__":
    main()
