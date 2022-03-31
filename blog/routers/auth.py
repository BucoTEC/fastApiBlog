from fastapi import APIRouter, Depends, HTTPException, status
from .. import  db, models, token
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/login')
def login(req:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(db.get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Wrong credentials')
    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}
