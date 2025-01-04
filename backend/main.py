from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc
from schemas.account_schemas import AccountResponse
from schemas.account_overview_response import AccountOverviewResponse
from controllers import user_controller
from schemas.card_schemas import CardResponse
from schemas.transaction_schemas import TransactionResponse
from database import engine
from starlette import status
import models.user as user_model
import models.account as account_model
import models.card as card_model
import models.transaction as transaction_model
from models.account import Account
from models.card import Card
from models.transaction import Transaction
from controllers import account_controller as account_routes
from controllers import card_controller as card_routes
from controllers import transaction_controller as transaction_routes
from controllers import admin_controller as admin_routes
from controllers import currency_controller as currency_routes
from database import engine
from dependencies import user_dependency, db_dependency

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

app.include_router(user_controller.router)
app.include_router(account_routes.router)
app.include_router(card_routes.router)
app.include_router(transaction_routes.router)
app.include_router(admin_routes.router)
app.include_router(currency_routes.router)

user_model.Base.metadata.create_all(bind=engine)
account_model.Base.metadata.create_all(bind=engine)
card_model.Base.metadata.create_all(bind=engine)
transaction_model.Base.metadata.create_all(bind=engine)

@app.get("/", status_code=status.HTTP_200_OK)
async def get_user_account(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    
    account = db.query(Account).filter(Account.user_id == user.id).first()
    account.balance = round(account.balance, 2)
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
        .order_by(desc(Transaction.created_at))
        .limit(10)
        .all())

    return AccountOverviewResponse(
        user=user,
        account=AccountResponse.model_validate(account),
        cards=[CardResponse.model_validate(card) for card in cards],
        transactions=[TransactionResponse.model_validate(transaction) for transaction in transactions]
    )
