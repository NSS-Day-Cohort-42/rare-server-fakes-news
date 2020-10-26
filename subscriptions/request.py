import sqlite3
import json
from models import Subscription


def get_subscriptions():
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
           s.id,
           s.user_id,
           s.subscribe_id,
           s.begin,
           s.end
        FROM Subscription s
        """)

        subscriptions = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            subscription = Subscription(row['id'], row['user_id'], row['subscribe_id'],
                                        row['begin'], row['end'])
            subscriptions.append(subscription.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(subscriptions)


def create_subscription(new_subscription):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Subscription
            (  user_id, subscribe_id, begin, end )
        VALUES
            ( ?, ?, ?, ?);
        """, (new_subscription['user_id'], new_subscription['subscribe_id'],
                new_subscription['begin'], new_subscription['end'],
               ))

        id = db_cursor.lastrowid

        new_subscription['id'] = id


    return json.dumps(new_subscription)