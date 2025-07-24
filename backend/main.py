from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router

app = FastAPI(title="Fire Detection API")

# CORS settings for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific React URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
