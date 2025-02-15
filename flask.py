from flask import  request, jsonify
import sqlite3


@app.route('/query', methods=['GET'])
def run_query():
    sql_query = request.args.get('query')
    if not sql_query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('reddit_comments.db')
        cursor = conn.cursor()

        # Execute the query
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # Close the connection
        conn.close()

        # Return the results as JSON
        return jsonify(rows)

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
