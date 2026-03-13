from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.exceptions import BaseExceptionApp
from app.routes import exercises_router

app = FastAPI()

app.include_router(exercises_router)


@app.exception_handler(BaseExceptionApp)
def domain_error_handler(req: Request, exc: BaseExceptionApp) -> JSONResponse:
    print(exc)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
