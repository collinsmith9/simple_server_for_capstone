import sqlite3
import json
from models import User

def get_all_users():
    with sqlite3.connect("./capstone_server.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            u.id,
            u.name,
            u.email,
            u.partner
        FROM users u
        """)
        users = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            partner = False
            if row['partner'] == 1:
                partner = True
            user = User(row['id'], row['name'], row['email'], partner)
            users.append(user.__dict__) #python __ is dunder
    return json.dumps(users)


def get_users_partner():
    with sqlite3.connect("./capstone_server.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            u.id,
            u.name,
            u.email,
            u.partner
        FROM users u
        WHERE u.partner = 1
        """,)
        users = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            partner = True
            user = User(row['id'], row['name'], row['email'], partner)
            users.append(user.__dict__) #python __ is dunder
    return json.dumps(users)

def get_user_by_email(email):
    with sqlite3.connect("./capstone_server.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            u.id,
            u.name,
            u.email,
            u.partner
        from users u
        WHERE u.email = ?
        """, ( email, ))

        users = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            partner = False
            if row['partner'] == 1:
                partner = True
            user = User(row['id'], row['name'], row['email'] , partner)
            users.append(user.__dict__)

    return json.dumps(users)

def get_user_by_id(id):
    with sqlite3.connect("./capstone_server.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            u.id,
            u.name,
            u.email,
            u.partner
        FROM users u
        WHERE u.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()
        partner = False
        if data['partner'] == 1:
            partner = True

        # Create an animal instance from the current row
        user = User(data['id'], data['name'], data['email'], partner)

        return json.dumps(user.__dict__)
