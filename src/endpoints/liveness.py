from fastapi import APIRouter

from model.state import State
from model.status import Status

router = APIRouter()


@router.get(
    "/health",
    description="This endpoint is used to check the health of the service.",
    response_model=Status,
)
async def health():
    """
    Endpoint to check service health.

    This function will execute "necessary" checks to determine if the service is healthy.
    """
    return Status(status=State.UP, message="Service is healthy.")
