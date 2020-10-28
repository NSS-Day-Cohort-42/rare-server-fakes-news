import sqlite3
import json
from models import Reaction


def get_reactions():
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
           r.id,
           r.reaction,
           r.reaction_description
        FROM reaction r
        """)

        # Initialize an empty list to hold all reaction representations
        reactions = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a reaction instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # reaction class above.
            reaction = Reaction(row['id'], row['reaction'], row['reaction_description'])
            reactions.append(reaction.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(reactions)


def get_reactions_by_post_id(post_id):

    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            r.id,
            r.reaction,
            r.reaction_description 
        FROM reaction r
        WHERE r.post_id = ?
        """, ( post_id, ))

        reactions = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            # Create a reaction instance from the current row
            reaction = Reaction(row['id'], row['reaction'], row['reaction_description'])
            reactions.append(reaction.__dict__)

        # Return the JSON serialized reaction object
        return json.dumps(reactions)

def create_reaction(new_reaction):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Reaction
            ( reaction, reaction_description )
        VALUES
            ( ?, ?);
        """, (new_reaction['reaction'], new_reaction['reaction_description']
               ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_reaction['id'] = id


    return json.dumps(new_reaction)