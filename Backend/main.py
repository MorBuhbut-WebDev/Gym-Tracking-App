import logging

import uvicorn

from app.config import settings
from app.logger import setup_logging

setup_logging()

logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


if __name__ == "__main__":
    uvicorn.run(
        app="app.app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "DEV",
        log_config=None,
    )
