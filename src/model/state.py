from enum import Enum


class State(Enum):
    """
    Represents the operational states of a service.

    This enumeration defines the possible states of a service, indicating whether the
    service is operational ('UP') or not operational ('DOWN'). It is used to provide
    a clear, standardized status in service health checks.

    Attributes:
        UP (str): Indicates the service is operational.
        DOWN (str): Indicates the service is not operational.
    """

    UP = "UP"
    DOWN = "DOWN"
