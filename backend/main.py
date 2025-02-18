from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from backend.config import settings
from backend.database import db_helper
from backend.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # Clean up the ML models and release the resources
    db_helper.dispose()


main_app = FastAPI()

main_app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
