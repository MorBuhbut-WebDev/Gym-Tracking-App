from app.exceptions.base_exception_app import BaseExceptionApp


class UnauthorizedException(BaseExceptionApp):
    @property
    def status_code(self):
        return 401


class ConflictException(BaseExceptionApp):
    @property
    def status_code(self):
        return 409


class NotFoundException(BaseExceptionApp):
    @property
    def status_code(self):
        return 404


class BadRequestException(BaseExceptionApp):
    @property
    def status_code(self):
        return 400
