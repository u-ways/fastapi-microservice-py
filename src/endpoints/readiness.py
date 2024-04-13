from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/",
    description="This endpoint is used to check if the service is ready to receive requests.",
)
async def ready():
    """
    Endpoint to check service readiness.

    This does not return any content in the response body, only HTTP status codes
    and headers are sent back to indicate the state of the service.
    """
    pass
