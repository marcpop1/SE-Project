from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc
from auth.schemas import UserDetailsResponse
from accounts.schemas import AccountOverviewResponse, AccountResponse
from cards.schemas import CardResponse
from transactions.schemas import TransactionResponse
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from auth import auth
from starlette import status
from auth.auth import get_current_user
import auth.models as auth_models
import accounts.models as account_models
import cards.models as card_models
import transactions.models as transaction_models
from accounts.models import Account
from cards.models import Card
from transactions.models import Transaction

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
user_dependency = Annotated[UserDetailsResponse, Depends(get_current_user)]

@app.get("/", status_code=status.HTTP_200_OK)
async def get_user_account(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    
    account = db.query(Account).filter(Account.user_id == user.id).first()
    if not account:
        create_account_model = Account(
            user_id = user.id,
            balance = 0.0,
            currency = 'RON'
        )
        db.add(create_account_model)
        db.commit()
        db.refresh(create_account_model)
        account = create_account_model
    
    cards = db.query(Card).filter(Card.account_id == account.id).limit(5).all()
    transactions = (db.query(Transaction)
        .filter((Transaction.account_from_id == account.id) | (Transaction.account_to_id == account.id))
        .order_by(desc(Transaction.datetime))
        .limit(10)
        .all())

    return AccountOverviewResponse(
        user=user,
        account=AccountResponse.model_validate(account),
        cards=[CardResponse.model_validate(card) for card in cards],
        transactions=[TransactionResponse.model_validate(transaction) for transaction in transactions]
    )
