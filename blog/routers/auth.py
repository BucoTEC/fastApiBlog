import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, db, models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/login')
def login(req:schemas.Login, db:Session = Depends(db.get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Wrong credentials')
    return {'message':'login succesful','data':user}
