from app.errors.base_error_app import BaseErrorApp


class UnauthorizedError(BaseErrorApp):
    @property
    def status_code(self):
        return 401


class ConflictError(BaseErrorApp):
    @property
    def status_code(self):
        return 409


class NotFoundError(BaseErrorApp):
    @property
    def status_code(self):
        return 404


class BadRequestError(BaseErrorApp):
    @property
    def status_code(self):
        return 400
