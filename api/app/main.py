from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging # Import logging
import time # For request timing
import random # For request ID
import string # For request ID

from app.core.config import settings
from app.core.logging_config import setup_logging # Import setup
from app.api.v1.router import api_router

# Call setup_logging to configure application loggers
# This should ideally be done once. Uvicorn might also configure logging.
# If using Uvicorn's --log-config, this might be redundant or conflict.
# For now, let's assume we want our app logger configured.
setup_logging()
logger = logging.getLogger("app.main")


# Placeholder for database initialization (Alembic handles schema)
# from app.database import engine, Base
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    # version="0.1.0", # Optional: Add version
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path} method={request.method}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code} path={request.url.path}")

    return response

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Hello World from FastAPI Backend!"}

# Placeholder for startup/shutdown events if needed
# @app.on_event("startup")
# async def startup_event():
#     pass

# @app.on_event("shutdown")
# async def shutdown_event():
#     pass
