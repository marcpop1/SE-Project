from fastapi_restful.cbv import cbv
from fastapi import APIRouter, Depends

from schemas.account_overview_response import AccountOverviewResponse
from controllers.account_overview_controller import AccountOverviewController
from dependencies import get_account_overview_controller

router = APIRouter(prefix="/account_overview", tags=["account_overview"])


@cbv(router)
class AccountOverviewView:
    account_overview_controller: AccountOverviewController = Depends(get_account_overview_controller)

    @router.get("/", response_model=AccountOverviewResponse)
    async def get_user_account(self):
        return await self.account_overview_controller.get_user_account_overview()
