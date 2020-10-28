import sqlite3
import json
from models import TagPost, Post, User, Category, Tag


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

def get_tagPosts_by_tag_id(tag_id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
           tp.id,
           tp.tag_id,
           tp.post_id,
           t.tag,
           p.title, 
           u.display_name, 
           c.type
        FROM TagPost tp 
        JOIN Tag t ON t.id = tp.tag_id
        JOIN Post p ON p.id = tp.post_id
        JOIN User u ON u.id = p.user_id
        JOIN Category c ON c.id = p.category_id
        WHERE tp.tag_id = ?
        """, ( tag_id, ))

        tagPosts = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            tagPost = TagPost(row['id'], row['tag_id'], row['post_id'])

            tag = Tag("", row['tag'])
            post = Post("", row['title'], "", "", "", "", "")
            user = User("", "", "", "", row['display_name'], "", "", "", "")
            category = Category("", row['type'])

            tagPost.tag = tag.__dict__
            tagPost.post = post.__dict__
            tagPost.user = user.__dict__
            tagPost.category = category.__dict__
            tagPosts.append(tagPost.__dict__)


    return json.dumps(tagPosts)


def create_tagPost(new_tagPost):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO TagPost
            (  tag_id, post_id )
        VALUES
            ( ?, ?);
        """, (new_tagPost['tag_id'], new_tagPost['post_id'], ))

        id = db_cursor.lastrowid

        new_tagPost['id'] = id


    return json.dumps(new_tagPost)