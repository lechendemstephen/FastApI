from fastapi import FastAPI, Response, status, HTTPException # type: ignore # type: ignore'
from .schema import Post, User, UserOut

import psycopg2  # type: ignore
from psycopg2.extras import RealDictCursor # type: ignore
import time

from passlib.context import CryptContext

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# connecting to the postgres database 
while True: 

    try: 
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Finalbaba1', cursor_factory=RealDictCursor) # type: ignore
        cursor = conn.cursor()
        print('Database connection was successfull')
        break
    except Exception as error:
        print('Connecting to databse successful')
        print('Erorr:', error)
        time.sleep(2)
# end of database connection



@app.get("/")
def root(): 
    return {"message": "welcome to my api"}


# getting all the posts

@app.get("/post")
def get_post():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {
        "data": posts
    }

# creating a post
@app.post("/posts")
def create_posts(post: Post, status_code=status.HTTP_201_CREATED):  # type: ignore
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    # saving data into the database
    conn.commit()
    return {
        "data": new_post
    }

# getting a particular posts using id
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id=%s""", (str(id)))
    post = cursor.fetchone()

    if not post: 
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"post with id: {id} not found")
    

    return {
        "post detail": post
    }

# deleting a post 
@app.delete("/posts/{id}")
def delete_post(id: int, status_code=status.HTTP_204_NO_CONTENT): 
    cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING * """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='post with index {id} not found')
    return {
        "deleted posts": deleted_post
    }

# updating a post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title=%s, content=%s WHERE id=%s RETURNING * """, (post.title, post.content, str(id)))
    updated_posts = cursor.fetchone()
    conn.commit()
    if updated_posts == None: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='post with index {id} not found')
    
    return {'updated posts is': updated_posts}


#  creating a user table and insertind data

# getting all users from the database
@app.get('/users')
def get_users(): 
    cursor.execute(""" SELECT * FROM users """)
    all_users = cursor.fetchall()

    return {
        "all users": all_users
    }


# creating a new user 
@app.post("/create_user", status_code=status.HTTP_201_CREATED, response_model_exclude_none=UserOut)
def create_user(user: User): 
    # hash the password
    hashed_password= pwd_context.hash(user.password)
    user.password = hashed_password
    
    cursor.execute(""" INSERT INTO users (email, password) VALUES (%s, %s) RETURNING * """, (user.email, user.password))
    created_user = cursor.fetchone()
    conn.commit()

    return {
        "Newly created user": created_user
        
    }
    
