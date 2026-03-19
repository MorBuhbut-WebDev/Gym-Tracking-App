from typing import Literal

from app.exceptions.base_exception_app import BaseExceptionApp


class UnauthorizedException(BaseExceptionApp):
    @property
    def status_code(self) -> Literal[401]:
        return 401


class ConflictException(BaseExceptionApp):
    @property
    def status_code(self) -> Literal[409]:
        return 409


class NotFoundException(BaseExceptionApp):
    @property
    def status_code(self) -> Literal[404]:
        return 404


class BadRequestException(BaseExceptionApp):
    @property
    def status_code(self) -> Literal[400]:
        return 400


class UnprocessableException(BaseExceptionApp):
    @property
    def status_code(self) -> Literal[422]:
        return 422
