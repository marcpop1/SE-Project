from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import user_controller
from database import engine
import models.user as user_model
import models.account as account_model
import models.card as card_model
import models.transaction as transaction_model
from controllers import account_controller as account_routes
from controllers import card_controller as card_routes
from controllers import transaction_controller as transaction_routes
from controllers import admin_controller as admin_routes
from controllers import currency_controller as currency_routes
from controllers import account_overview_controller as account_overview_routes

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
app.include_router(account_overview_routes.router)

user_model.Base.metadata.create_all(bind=engine)
account_model.Base.metadata.create_all(bind=engine)
card_model.Base.metadata.create_all(bind=engine)
transaction_model.Base.metadata.create_all(bind=engine)