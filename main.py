from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get('/')
def index():
    return({'message':'welcome to fastAPI'})


@app.get('/about')
def about():
    return ({'data':{ 'message': 'The about page'}})


@app.get('/blog/{id}')
def get_post(id : int):
    
    return ({'data':{'message':f'your path param is {id}'}})

@app.get('/test')
def method_name(limit: int = 10, sort : Optional[str] = None):
    if sort:
        return ({'message': f'your sort is {sort}'})
    return({'message': f'your limit is {limit}'})

class Blog_post(BaseModel):
    title : str
    body: str
    published_at : Optional[bool]

@app.post('/podatci')
def podatci(blog : Blog_post):
    return {'message': f'ovo je stranica sa podatcima, vas title je {blog.title}'}
