from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from .. import schemas, db, models
from ..hashing import hash_password
from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/user', status_code=status.HTTP_201_CREATED , tags=['user'])
def create_user( req : schemas.User, db : Session = Depends(db.get_db)):
    new_user =  models.User(name=req.name, email=req.email, password=hash_password(req.password) )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/users', status_code=200, response_model=List[schemas.ShowUser], tags=['user'])
def all_users(db:Session = Depends(db.get_db)):
    all_users = db.query(models.User).all()
    if len(all_users) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No users curently in db')
    return all_users

@router.get('/users{id}', status_code=200, response_model=schemas.ShowUser, tags=['user'])
def all_users(id: int, db:Session = Depends(db.get_db)):
    user = db.query(models.User).where(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user of id:{id} not found')
    return user
