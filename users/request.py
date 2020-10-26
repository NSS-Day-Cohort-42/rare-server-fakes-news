import sqlite3
import json
from models import User


def get_all_users():
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name, 
            u.last_name,
            u.display_name,
            u.email,
            u.password,
            u.avatar,
            u.creation,
            u.active
        FROM User u
        """)

        # Initialize an empty list to hold all user representations
        users = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a user instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Post class above.
            user = User(row['id'], row['avatar'], row['first_name'], row['last_name'], row['display_name'], 
                        row['password'], row['email'], row['creation'], row['active'])
            users.append(user.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(users)


def get_user_by_email(email):

    with sqlite3.connect("rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            u.id,
            u.first_name, 
            u.last_name,
            u.display_name,
            u.email,
            u.password,
            u.avatar,
            u.creation,
            u.active
        from User u
        WHERE u.email = ?
        """, ( email, ))

        data = db_cursor.fetchone()

        user = User(data['id'], data['avatar'], data['first_name'], data['last_name'], data['display_name'], 
                    data['password'], data['email'], data['creation'],data['active'])

        # Return the JSON serialized user object
        return json.dumps(user.__dict__)

def create_user(new_user):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO User
            ( avatar, first_name, last_name, display_name, password, email, creation, active )
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?, ? );
        """, (new_user['avatar'], new_user['first_name'], new_user['last_name'], new_user['display_name'], 
                    new_user['password'], new_user['email'], new_user['creation'],new_user['active']))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_user['id'] = id


    return json.dumps(new_user)