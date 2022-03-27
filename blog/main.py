from fastapi import FastAPI
from . import schemas

app = FastAPI()



@app.post('/blog')
def create( body : schemas.Blog):
    return {'data':{'title': body.title, 'body':body.body}}
