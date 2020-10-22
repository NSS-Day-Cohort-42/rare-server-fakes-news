import sqlite3
import json
from models import TagPost


def get_tagPosts():
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
           tp.id,
           tp.tag_id,
           tp.post_id
        FROM tagPost tp
        """)

        # Initialize an empty list to hold all tagPost representations
        tagPosts = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a tagPost instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Post class above.
            tagPost = TagPost(row['id'], row['tag_id'], row['post_id'])
            tagPosts.append(tagPost.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(tagPosts)


def create_tagPost(new_tagPost):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO TagPost
            (  tag_id, post_id )
        VALUES
            ( ?, ?);
        """, (new_tagPost['tag_id'], new_tagPost['post_id']
               ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_tagPost['id'] = id


    return json.dumps(new_tagPost)