from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from views import user_view
from database import engine
import models.user as user_model
import models.account as account_model
import models.card as card_model
import models.transaction as transaction_model
from views import account_view
from views import card_view
from views import transaction_view
from views import admin_view
from views import currency_view
from views import account_overview_view


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

app.include_router(user_view.router)
app.include_router(account_view.router)
app.include_router(card_view.router)
app.include_router(transaction_view.router)
app.include_router(admin_view.router)
app.include_router(currency_view.router)
app.include_router(account_overview_view.router)

user_model.Base.metadata.create_all(bind=engine)
account_model.Base.metadata.create_all(bind=engine)
card_model.Base.metadata.create_all(bind=engine)
transaction_model.Base.metadata.create_all(bind=engine)