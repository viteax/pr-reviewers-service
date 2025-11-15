from fastapi import FastAPI

from app.api.main import api_router

app = FastAPI(title="PR Reviewers Service")
app.include_router(api_router)
