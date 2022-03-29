from fastapi import Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from .schemas import Blog 
from . import models
from .db import engine, SessionLocal

models.Base.metadata.create_all(engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create( req : Blog, db : Session = Depends(get_db)):
    new_blog =  models.Blog(title=req.title, body=req.body )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog')
def all(db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=200)
def  show(id : int,response : Response, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).where(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f'Blog by id of: {id} dose not exist'
    return blog
