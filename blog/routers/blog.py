from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from .. import schemas, db, models
from sqlalchemy.orm import Session
from ..controllers import blog

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)


@router.get('/', response_model=List[schemas.ShowBlog])
def all(db : Session = Depends(db.get_db)):
    return blog.all(db)
    


@router.post('/', status_code=status.HTTP_201_CREATED,)
def create( req : schemas.Blog, db : Session = Depends(db.get_db)):
    return blog.add(req,db)



@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def  show(id : int, db : Session = Depends(db.get_db)):
    return blog.find(id,db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT,)
def  destroy(id : int, db : Session = Depends(db.get_db)):
    return blog.remove(id,db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED,)
def  update(id : int, req : schemas.Blog, db : Session = Depends(db.get_db)):
    return blog.update(req,db,id)
