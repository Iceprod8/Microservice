from fastapi import FastAPI
from .database import engine, Base
from .routers import users, preferences

app = FastAPI()

# Crée les tables dans la base de données
Base.metadata.create_all(bind=engine)

# Enregistre les routes
app.include_router(users.router, prefix="/users")
app.include_router(preferences.router, prefix="/preferences")