from fastapi import FastAPI
from . import schemas
from . import models, db

models.Base.metadata.create_all(db.engine)
app = FastAPI()



@app.post('/blog')
def create( body : schemas.Blog):
    return {'data':{'title': body.title, 'body':body.body}}
