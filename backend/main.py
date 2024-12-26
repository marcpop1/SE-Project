from typing import Annotated
from fastapi import Depends, FastAPI
import auth.schemas as schemas
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from auth import auth

app = FastAPI()
app.include_router(auth.router)

schemas.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]