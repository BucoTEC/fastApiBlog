from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def all(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs

def add(req:schemas.Blog, db:Session):
    new_blog =  models.Blog(title=req.title, body=req.body )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def find(id:int,db:Session):
    blog = db.query(models.Blog).where(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog of id:{id} not found')
    return blog


def remove(id:int, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id: {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

def update(req:schemas.Blog, db:Session, id:int):
    blog =  db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id: {id} not found')
    blog.update(dict(req))
    db.commit()
    return 'successful update'
