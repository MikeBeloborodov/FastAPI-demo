import sqlite3

def create_db():
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
                CREATE TABLE posts(
                    title text,
                    content text,
                    rating integer
                )
        """)
        connection.commit()
    except Exception as error:
        print("Error!")
        print(error)

def save_post(new_post: dict):
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()
    try:
        cursor.execute(f"""
                INSERT INTO posts VALUES ('{new_post.title}', '{new_post.content}', '{new_post.rating}')
        """)
        connection.commit()
        connection.close()
    except Exception as error:
        print("Error!")
        print(error)
        connection.close()

def get_all_posts() -> list:
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()
    try:
        cursor.execute(f"""
                SELECT rowid, *
                FROM posts
        """)
        posts = cursor.fetchall()
        connection.close()
        return posts
    except Exception as error:
        print("Error!")
        print(error)
        connection.close()

def get_post_by_id(post_id: int) -> list:
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()
    try:
        cursor.execute(f"""
                SELECT rowid, *
                FROM posts
                WHERE rowid = {post_id}
        """)
        posts = cursor.fetchall()
        connection.close()
        return posts
    except Exception as error:
        print("Error!")
        print(error)
        connection.close()

def delete_post_by_id(post_id) -> bool:
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()
    try:
        cursor.execute(f"""
                SELECT rowid, *
                FROM posts
                WHERE rowid = {post_id}
        """)
        if not cursor.fetchall():
            return False
    except Exception as error:
        print("Error!")
        print(error)
        connection.close()
        return False
    try:
        cursor.execute(f"""
                DELETE FROM posts
                WHERE rowid = {post_id}
        """)
        connection.commit()
        connection.close()
        return True
    except Exception as error:
        print("Error!")
        print(error)
        connection.close()
        return False

def update_post_by_id(post_id, updated_post):
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()
    try:
        cursor.execute(f"""
                SELECT rowid, *
                FROM posts
                WHERE rowid = {post_id}
        """)
        if not cursor.fetchall():
            return False
    except Exception as error:
        print("Error!")
        print(error)
        connection.close()
        return False
    try:
        cursor.execute(f"""
                UPDATE posts
                SET 
                    title = '{updated_post.title}',
                    content = '{updated_post.content}',
                    rating = {updated_post.rating}
                WHERE rowid = {post_id}
        """)
        connection.commit()
        connection.close()
        return True
    except Exception as error:
        print("Error!")
        print(error)
        connection.close()
        return False

def convert_to_json(posts: list) -> dict:
    posts_dict = {}
    for post in posts:
        posts_dict.update({f"id_{post[0]}" :{
                                                "title" : post[1],
                                                "content" : post[2],
                                                "rating" : post[3]
        }})

    return posts_dict