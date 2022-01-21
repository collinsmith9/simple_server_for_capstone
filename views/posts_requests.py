import sqlite3
import json
from models import Post, User


def get_posts_expand_user():
    with sqlite3.connect("./capstone_server.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            p.id,
            p.problemDescription,
            p.problem,
            p.userId,
            u.id u_id,
            u.name,
            u.email,
            u.partner 
        FROM posts p
        JOIN users u
            ON u.id = p.userId
        """)
        posts = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            partner = False
            if row['partner'] == 1:
                partner = True
            post = Post(row['id'], row['problemDescription'], row['problem'], row['userId'])
            user = User(row['u_id'], row['name'], row['email'], partner)
            post.user = user.__dict__
            posts.append(post.__dict__) #python __ is dunder
    return json.dumps(posts)