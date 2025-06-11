from fastapi import FastAPI
from src.api.routes.text_analyzer import router

app = FastAPI(title="Text Analyzer API")
app.include_router(router)