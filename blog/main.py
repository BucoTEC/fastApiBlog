from fastapi import FastAPI
from .schemas import Blog 
from . import models
from .db import engine

models.Base.metadata.create_all(engine)
app = FastAPI()



@app.post('/blog')
def create( body : Blog):
    return {'data':{'title': body.title, 'body':body.body}}
