from abc import ABC, abstractmethod


class IMiddleware(ABC):

    """
    Interface for creating middlewares
    """

    def __init__(self) -> None: ...
    
    @abstractmethod
    def __call__(self) -> callable: ...
