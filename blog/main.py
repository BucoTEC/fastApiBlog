from typing import List
from fastapi import Depends, FastAPI, status, HTTPException
from sqlalchemy.orm import Session
from . import schemas, models
from .db import engine, SessionLocal
from .hashing import hash_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create( req : schemas.Blog, db : Session = Depends(get_db)):
    new_blog =  models.Blog(title=req.title, body=req.body )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', response_model=List[schemas.ShowBlog])
def all(db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog)
def  show(id : int, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).where(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog of id:{id} not found')
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def  destroy(id : int, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id: {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def  update(id : int, req : schemas.Blog, db : Session = Depends(get_db)):
    blog =  db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id: {id} not found')
    blog.update(dict(req))
    db.commit()
    return 'successful update'



# user routes 



@app.post('/user', status_code=status.HTTP_201_CREATED)
def create_user( req : schemas.User, db : Session = Depends(get_db)):
    new_user =  models.User(name=req.name, email=req.email, password=hash_password(req.password) )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users', status_code=200, response_model=List[schemas.ShowUser])
def all_users(db:Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users

