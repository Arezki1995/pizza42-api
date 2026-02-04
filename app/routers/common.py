from fastapi import APIRouter
from fastapi.responses import RedirectResponse

common_router = APIRouter(tags=["Common"])

@common_router.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
