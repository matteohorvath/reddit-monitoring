import praw
import csv
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
    
    # Build a timestamped CSV filename
    timestamp_str = time.strftime("%Y%m%d-%H%M%S")
    csv_filename = f"reddit_comments_{timestamp_str}.csv"
    
    # Define the CSV headers
    fieldnames = [
        "submission_id",
        "submission_title",
        "comment_id",
        "comment_parent_id",
        "comment_body",
        "comment_score",
        "comment_author",
        "comment_created_utc",
        "comment_edited"
    ]
    
    # Ensure we write to a valid file path
    # (This script writes to the current working directory)
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
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
                
                writer.writerow({
                    "submission_id": submission.id,
                    "submission_title": submission.title,
                    "comment_id": comment_id,
                    "comment_parent_id": comment_parent_id,
                    "comment_body": comment_body,
                    "comment_score": comment_score,
                    "comment_author": comment_author,
                    "comment_created_utc": comment_created_utc,
                    "comment_edited": comment_edited
                })

    print(f"Comments for the latest 100 posts on r/{subreddit_name} saved to {csv_filename}")

if __name__ == "__main__":
    main()
