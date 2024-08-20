
from fastapi import FastApi # type: ignore


app = FastApi()




@app.get('/posts')
def get_post():

    return 