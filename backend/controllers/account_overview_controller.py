from fastapi_restful.cbv import cbv
from fastapi import APIRouter, Depends

from schemas.account_overview_response import AccountOverviewResponse
from services.account_overview_service import AccountOverviewService
from dependencies import get_account_overview_service

router = APIRouter(prefix="/account_overview", tags=["account_overview"])


@cbv(router)
class AccountOverviewController:
    account_overview_service: AccountOverviewService = Depends(get_account_overview_service)

    @router.get("/", response_model=AccountOverviewResponse)
    async def get_user_account(self):
        return await self.account_overview_service.get_user_account_overview()
