from sqlalchemy.orm import Session
from . import models, schemas
from passlib.hash import bcrypt

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        password=hashed_password,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user_preference(db: Session, uid: int, preference: schemas.UserPreferenceCreate):
    db_preference = models.UserPreference(id_user=uid, id_genre=preference.id_genre)
    db.add(db_preference)
    db.commit()
    db.refresh(db_preference)
    return db_preference
