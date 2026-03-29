from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import BaseExceptionApp
from app.logger import get_logger
from app.routes import exercises_router, routines_router, workouts_router

app = FastAPI()

app.include_router(exercises_router)
app.include_router(routines_router)
app.include_router(workouts_router)


logger = get_logger(__name__)


@app.exception_handler(RequestValidationError)
async def request_validation_handler(
    req: Request, exc: RequestValidationError
) -> JSONResponse:
    error_details = " | ".join(err["msg"] for err in exc.errors())

    logger.warning(f"[VALIDATION ERROR] on {req.url.path}: {error_details}")
    return JSONResponse(
        status_code=422,
        content={"detail": error_details},
    )


@app.exception_handler(BaseExceptionApp)
async def domain_error_handler(req: Request, exc: BaseExceptionApp) -> JSONResponse:
    logger.warning(
        f"[APP ERROR] {exc.status_code} - {exc.message} | Path: {req.url.path}"
    )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(req: Request, exc: SQLAlchemyError) -> JSONResponse:
    logger.error(
        f"[DB ERROR] {type(exc).__name__}: {exc} | Path: {req.url.path}", exc_info=True
    )
    return JSONResponse(status_code=500, content={"detail": "Database error"})


@app.exception_handler(Exception)
async def generic_error_handler(req: Request, exc: Exception) -> JSONResponse:
    logger.error(
        f"[UNEXPECTED ERROR] {type(exc).__name__}: {exc} | Path: {req.url.path}",
        exc_info=True,
    )
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
