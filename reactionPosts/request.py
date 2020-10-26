import sqlite3
import json
from models import ReactionPost


def get_reactionPosts():
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
           rp.id,
           rp.reaction_id,
           rp.post_id,
           rp.user_id
        FROM reactionPost rp
        """)

        # Initialize an empty list to hold all reactionPost representations
        reactionPosts = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            reactionPost = ReactionPost(row['id'], row['reaction_id'], row['post_id'], row['user_id'])
            reactionPosts.append(reactionPost.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(reactionPosts)


def create_reactionPost(new_reactionPost):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO ReactionPost
            (  reaction_id, post_id, user_id )
        VALUES
            ( ?, ?, ?);
        """, (new_reactionPost['reaction_id'], new_reactionPost['post_id'], new_reactionPost['user_id'] ))

        id = db_cursor.lastrowid

        new_reactionPost['id'] = id


    return json.dumps(new_reactionPost)