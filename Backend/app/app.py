from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.exceptions import BaseExceptionApp

app = FastAPI()


@app.exception_handler(BaseExceptionApp)
def domain_error_handler(req: Request, exc: BaseExceptionApp):
    print(exc)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
