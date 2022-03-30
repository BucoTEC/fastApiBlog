from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from .. import schemas, db, models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)


@router.get('/', response_model=List[schemas.ShowBlog])
def all(db : Session = Depends(db.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post('/', status_code=status.HTTP_201_CREATED,)
def create( req : schemas.Blog, db : Session = Depends(db.get_db)):
    new_blog =  models.Blog(title=req.title, body=req.body )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog



@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def  show(id : int, db : Session = Depends(db.get_db)):
    blog = db.query(models.Blog).where(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog of id:{id} not found')
    return blog


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT,)
def  destroy(id : int, db : Session = Depends(db.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id: {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED,)
def  update(id : int, req : schemas.Blog, db : Session = Depends(db.get_db)):
    blog =  db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id: {id} not found')
    blog.update(dict(req))
    db.commit()
    return 'successful update'
