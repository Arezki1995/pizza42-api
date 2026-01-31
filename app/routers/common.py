from fastapi import APIRouter
from fastapi.responses import FileResponse, RedirectResponse


common_router = APIRouter(tags=["Common"])

@common_router.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@common_router.get("/health")
def health_check():
    return {"status": "ok"}


