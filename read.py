import sqlite3

def read_last_10_comments():
    # Connect to the SQLite database
    conn = sqlite3.connect('reddit_comments.db')
    cursor = conn.cursor()

    # Query the last 10 rows from the comments table
    cursor.execute('''
        SELECT * FROM comments
        ORDER BY query_timestamp DESC
        LIMIT 10
    ''')
    
    # Fetch and print the results
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    read_last_10_comments()
