import sqlite3
import json
import subscriptions
# from models import Subscription


def get_subscriptions():
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
           s.id,
           s.user_id,
           s.subscribe_id
        FROM subscription s
        """)

        # Initialize an empty list to hold all subscription representations
        subscriptions = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a reaction instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Post class above.
            subscription = Subscription(row['id'], row['user_id'], row['subscribe_id'])
            subscriptions.append(subscription.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(subscriptions)


def create_subscription(new_subscription):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Subscription
            (  user_id, subscribe_id )
        VALUES
            ( ?, ?);
        """, (new_subscription['user_id'], new_subscription['subscribe_id']
               ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_subscription['id'] = id


    return json.dumps(new_subscription)