from pydantic import BaseModel

from model.state import State


class Status(BaseModel):
    """
    Represents the status of a service.

    This class defines the status of a service, indicating whether the service is operational
    or not. It is used to provide a clear, standardized status in service health checks.

    Attributes:
        status (State): Indicates the operational state of the service.
        message (str): A message providing additional information about the service status.
    """

    status: State
    message: str
