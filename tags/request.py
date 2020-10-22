import sqlite3
import json
from models import Tag


def get_tags():
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
           t.id,
           t.tag
        FROM tag t
        """)

        # Initialize an empty list to hold all tag representations
        tags = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a tag instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Post class above.
            tag = Tag(row['id'], row['tag'])
            tags.append(tag.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(tags)


def create_tag(new_tag):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Tag
            ( tag )
        VALUES
            ( ? );
        """, ((new_tag['tag']),))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the tag dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_tag['id'] = id


    return json.dumps(new_tag)