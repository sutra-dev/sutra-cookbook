import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth as auth_router
from .routers import transactions as transactions_router
from .routers import ai_advisor as ai_router
from .database import engine, Base

app = FastAPI(title="Multilingual Budget Backend")

# CORS configuration - allow frontend origin during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router.router)
app.include_router(transactions_router.router)
app.include_router(ai_router.router)


@app.on_event("startup")
async def on_startup():
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run("fastapi_backend.main:app", host="0.0.0.0", port=8000, reload=True) 