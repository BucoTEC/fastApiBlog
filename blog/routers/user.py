from fastapi import APIRouter, Depends, status
from typing import List
from .. import schemas, db
from sqlalchemy.orm import Session
from ..controllers import user

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('/', status_code=status.HTTP_201_CREATED , )
def create_user( req : schemas.User, db : Session = Depends(db.get_db)):
    return user.add(req,db)
    

@router.get('/', status_code=200, response_model=List[schemas.ShowUser], )
def all_users(db:Session = Depends(db.get_db)):
    return user.get_all(db)

@router.get('/{id}', status_code=200, response_model=schemas.ShowUser, )
def find_users(id: int, db:Session = Depends(db.get_db)):
    return user.find(db, id)
