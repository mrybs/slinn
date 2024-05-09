from typing import Protocol

class BaseMiddleware(Protocol):
    def __init__(self) -> None:
        raise NotImplementedError('Called virtual method BaseMiddleware.__init__')
    
    def __call__(self) -> callable:
        raise NotImplementedError('Called virtual method BaseMiddleware.__call__')
