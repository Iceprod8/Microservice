from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter()

@router.post("/users/{uid}/preferences", response_model=schemas.UserPreferenceCreate)
def add_user_preference(uid: int, preference: schemas.UserPreferenceCreate, db: Session = Depends(database.get_db)):
    return crud.create_user_preference(db=db, uid=uid, preference=preference)
