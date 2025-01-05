from fastapi import HTTPException
from controllers.transaction_serializer_controller import TransactionSerializerController
from schemas.account_response import AccountResponse
from schemas.card_response import CardResponse
from repositories.account_repository import AccountRepository
from repositories.card_repository import CardRepository
from repositories.transaction_repository import TransactionRepository
from schemas.account_overview_response import AccountOverviewResponse
from schemas.user_details_response import UserDetailsResponse


class AccountOverviewController:
    def __init__(
        self,
        user: UserDetailsResponse,
        account_repository: AccountRepository,
        transaction_repository: TransactionRepository,
        card_repository: CardRepository,
        transaction_serializer: TransactionSerializerController
    ):
        self.user = user
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository
        self.card_repository = card_repository
        self.transaction_serializer = transaction_serializer

    async def get_user_account_overview(self) -> AccountOverviewResponse:
        if self.user is None:
            raise HTTPException(status_code=401, detail="Authentication failed")

        account = self.account_repository.find_one_by_user_id(self.user.id)
        account.balance = round(account.balance, 2)

        cards = self.card_repository.find_all_by_user_id(self.user.id, 5)
        transactions = self.transaction_repository.find_all_by_user_id(self.user.id, 10)

        return AccountOverviewResponse(
            user=UserDetailsResponse.model_validate(self.user),
            account=AccountResponse.model_validate(account),
            cards=[CardResponse.model_validate(card) for card in cards],
            transactions=[self.transaction_serializer.serialize_transaction(t, self.user.id) for t in transactions]
        )
