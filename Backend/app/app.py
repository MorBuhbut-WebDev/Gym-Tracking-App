from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import BaseExceptionApp
from app.routes import exercises_router, routines_router

app = FastAPI()

app.include_router(exercises_router)
app.include_router(routines_router)


@app.exception_handler(BaseExceptionApp)
async def domain_error_handler(req: Request, exc: BaseExceptionApp) -> JSONResponse:
    print(f"[APP ERROR] {exc.status_code} - {exc.message} | Path: {req.url.path}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(req: Request, exc: SQLAlchemyError) -> JSONResponse:
    print(f"[DB ERROR] {type(exc).__name__}: {exc} | Path: {req.url.path}")
    return JSONResponse(status_code=500, content={"detail": "Database error"})


@app.exception_handler(Exception)
async def generic_error_handler(req: Request, exc: Exception) -> JSONResponse:
    print(f"[UNEXPECTED ERROR] {type(exc).__name__}: {exc} | Path: {req.url.path}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
