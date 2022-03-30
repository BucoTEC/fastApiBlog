import imp
from .. import schemas, db, models
from ..hashing import hash_password
from sqlalchemy.orm import Session
from fastapi import status ,HTTPException


def add(req : schemas.User, db : Session):
    new_user =  models.User(name=req.name, email=req.email, password=hash_password(req.password) )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all(db:Session):
    all_users = db.query(models.User).all()
    if len(all_users) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No users curently in db')
    return all_users

def find(db:Session, id:int):
    user = db.query(models.User).where(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user of id:{id} not found')
    return user
