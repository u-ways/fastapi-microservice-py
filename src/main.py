from contextlib import asynccontextmanager
from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from endpoints.liveness import router as liveness_router
from endpoints.readiness import router as readiness_router

# Load environment variables from .env file
# See: https://github.com/theskumar/python-dotenv
load_dotenv()


# Lifecycle management for FastAPI is now done with async context managers
# See: https://fastapi.tiangolo.com/advanced/events/#lifespan
@asynccontextmanager
async def lifespan(entrypoint: FastAPI):
    instrumentator.expose(entrypoint)
    yield


# Create a FastAPI instance
# See: https://fastapi.tiangolo.com/reference/fastapi/
app = FastAPI(
    lifespan=lifespan,
    title=getenv("APP_TITLE"),
    version=getenv("APP_VERSION"),
    description=getenv("APP_DESCRIPTION"),
    contact={
        "name": getenv("APP_CONTACT_NAME"),
        "url": getenv("APP_CONTACT_URL"),
        "email": getenv("APP_CONTACT_EMAIL"),
    },
    license_info={
        "name": getenv("APP_LICENCE_NAME"),
        "url": getenv("APP_LICENCE_URL"),
    },
)

# Instrument FastAPI with Prometheus
# See: https://github.com/trallnag/prometheus-fastapi-instrumentator
instrumentator = Instrumentator().instrument(app)

# Enabled Routes
app.include_router(liveness_router)
app.include_router(readiness_router)
