from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

import account.models as account_models
import auth.models as auth_models
import cards.models as card_models
import transactions.models as transaction_models
from auth import auth
from database import engine
from dependecies import user_dependency

load_dotenv()

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


@app.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    return {"User": user}
