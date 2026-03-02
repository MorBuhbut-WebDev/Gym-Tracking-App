from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.routes import exercises_router, routines_router
from app.errors import BaseErrorApp

app = FastAPI()

app.include_router(exercises_router)
app.include_router(routines_router)


@app.exception_handler(BaseErrorApp)
def domain_error_handler(req: Request, exc: BaseErrorApp):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(SQLAlchemyError)
def db_error_handler(req: Request, exc: SQLAlchemyError):
    print(exc)
    return JSONResponse(status_code=500, content={"detail": "Something went wrong!"})
