import sqlite3
import json
from models import User

def get_all_users():
    # Open a connection to the database
    with sqlite3.connect("rare.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            u.id,
            u.avatar,
            u.display_name,
            u.password,
            u.email,
            u.creation,
            u.active
        FROM User u
        """)

        # Initialize an empty list to hold all animal representations
        users = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        for row in dataset:

            user = User(row['id'], row['avatar'], row['display_name'], row['password'],
                    row['email'], row['creation'], row['active'])

            users.append(user.__dict__)

    return json.dumps(users)

def get_user_by_email(email):

    with sqlite3.connect("rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            u.id,
            u.avatar,
            u.display_name,
            u.password,
            u.email,
            u.creation,
            u.active
        from User u
        WHERE u.email = ?
        """, ( email, ))

        data = db_cursor.fetchone()

        user = User(data['id'], data['avatar'], data['display_name'], 
                    data['password'], data['email'], data['creation'],data['active'])

        # Return the JSON serialized user object
        return json.dumps(user.__dict__)

def create_user(new_user):
    with sqlite3.connect("rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO User
            ( avatar, display_name, password, email, creation, active )
        VALUES
            ( ?, ?, ?, ?, ?, ?);
        """, (new_user['avatar'], new_user['display_name'],
              new_user['password'], new_user['email'],
              new_user['creation'], new_user['active'] ))

        id = db_cursor.lastrowid

        new_user['id'] = id


    return json.dumps(new_user)