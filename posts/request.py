from sqlite3.dbapi2 import Row
from models.category import Category
import sqlite3
import json
from models import Post, User, Tag, TagPost

def get_all_posts():
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
           p.id,
           p.title,
           p.content,
           p.category_id,
           p.date,
           p.user_id,
           p.approved,
           c.type,
           u.display_name
        FROM Post p
        JOIN Category c ON c.id = p.category_id
        JOIN User u ON u.id = p.user_id
        """)

        # Initialize an empty list to hold all post representations
        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            post = Post(row['id'], row['title'], row['content'], row['category_id'], row['date'], row['user_id'], row['approved'])

            user = User("", "", "", "", row['display_name'], "", "", "", "")
            

            category = Category("", row['type'])

            post.user = user.__dict__
            post.category = category.__dict__

            posts.append(post.__dict__)


    return json.dumps(posts)



def get_single_post(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.title,
            p.content,
            p.category_id,
            p.date,
            p.user_id,
            p.approved,
            c.type,
            u.display_name,
            u.id user_obj_id
        FROM post p
        JOIN Category c ON c.id = p.category_id
        JOIN User u ON u.id = p.user_id 
        WHERE p.id = ?;
            """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an post instance from the current row
        post = Post(data['id'], data['title'], data['content'], data['category_id'], data['date'], data['user_id'], data['approved'])
        category = Category("", data['type'])
        user = User("", "", "", "", data['display_name'], "", "", "", "")
        
        post.user = user.__dict__
        post.category = category.__dict__
        post.user = user.__dict__

        return json.dumps(post.__dict__)

def get_single_post_tags(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            t.id,
            t.tag,
            tp.id tagPostId
        FROM TagPost tp
        JOIN Tag t on t.id = tp.tag_id 
        JOIN post p on p.id = tp.post_id
        WHERE p.id = ?;
            """, ( id, ))

        # Initialize an empty list to hold all post representations
        tags = []

        # Load the single result into memory
        dataset = db_cursor.fetchall()

        for row in dataset:
            # Create an post instance from the current row
            tag = Tag(row['id'], row['tag'])
            tagPost = TagPost(row['tagPostId'], "", "")
            tag.tagPost = tagPost.__dict__
            
            tags.append(tag.__dict__)

        return json.dumps(tags)

def get_posts_by_user_id(user_id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.title,
            p.content,
            p.category_id,
            p.date,
            p.user_id,
            p.approved,
            c.type,
            u.display_name
        FROM post p
        JOIN Category c ON c.id = p.category_id
        JOIN User u ON u.id = p.user_id       
        WHERE p.user_id = ?;

        """, ( user_id, ))

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            # Create an post instance from the current row
            post = Post(row['id'], row['title'], row['content'], row['category_id'], row['date'], row['user_id'], row['approved'])
            user = User("", "", "", "", row['display_name'], "", "", "", "")
            category = Category("", row['type'])

            post.user = user.__dict__
            post.category = category.__dict__            
            posts.append(post.__dict__)
            

        # Return the JSON serialized Customer object
        return json.dumps(posts)

# # get_posts_by_tag_id

def get_posts_by_category_id(category_id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.title,
            p.content,
            p.category_id,
            p.date,
            p.user_id,
            p.approved,
            c.type,
            u.display_name
        FROM POST p
        JOIN Category c ON c.id = p.category_id
        JOIN User u ON u.id = p.user_id
        WHERE p.category_id = ?
        """, ( category_id, ))

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            # Create an post instance from the current row
            post = Post(row['id'], row['title'], row['content'], row['category_id'], row['date'], row['user_id'], row['approved'])
            
            user = User("", "", "", "", row['display_name'], "", "", "", "")
            
            category = Category("", row['type'])

            post.user = user.__dict__
            post.category = category.__dict__
            
            posts.append(post.__dict__)
            

        # Return the JSON serialized Customer object
        return json.dumps(posts)

# # get_posts_by_subscription

def create_post(new_post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Post
            ( title, content, category_id, date, user_id, approved )
        VALUES
            ( ?, ?, ?, ?, ?, ?);
        """, (new_post['title'], new_post['content'],
              new_post['category_id'], new_post['date'], new_post['user_id'], new_post['approved'], ))

        id = db_cursor.lastrowid

        new_post['id'] = id


    return json.dumps(new_post)


def delete_post(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM post
        WHERE id = ?
        """, (id, ))

# def edit_post(id, new_post):
#     with sqlite3.connect("./rare.db") as conn:
#         db_cursor = conn.cursor()

#         db_cursor.execute("""
#         UPDATE Post
#             SET
    # #           p.id,
    #             p.title,
    #             p.content,
    #             p.category_id,
    #             p.datetime,
    #             p.user_id,
    #             p.approved            
#         WHERE id = ?
#         """, (new_post['title'], new_post['content'],
            #   new_post['category_id'], new_post['datetime'], new_post['user_id'], new_post['approved']))

#         # Were any rows affected?
#         # Did the client send an `id` that exists?
#         rows_affected = db_cursor.rowcount

#     if rows_affected == 0:
#         # Forces 404 response by main module
#         return False
#     else:
#         # Forces 204 response by main module
#         return True

