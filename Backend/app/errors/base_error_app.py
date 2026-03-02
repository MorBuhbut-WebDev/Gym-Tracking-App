from abc import ABC, abstractmethod


class BaseErrorApp(Exception, ABC):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

    @property
    @abstractmethod
    def status_code(self) -> int:
        pass

    def __str__(self) -> str:
        return self.message
