from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from auth import auth
from starlette import status
from auth.auth import get_current_user
import auth.models as auth_models
import account.models as account_models
import cards.models as card_models
import transactions.models as transaction_models

app = FastAPI()

origins = [
    "http://localhost:5173",  # Frontend running on localhost
    "http://localhost:8000",  # Backend running on localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(auth.router)

auth_models.Base.metadata.create_all(bind=engine)
account_models.Base.metadata.create_all(bind=engine)
card_models.Base.metadata.create_all(bind=engine)
transaction_models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    return {"User": user} 
