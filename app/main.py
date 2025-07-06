from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging

from app.api.proxy import router as proxy_router
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title="Recall API Gateway",
    description="A gateway to forward requests to different channels.",
    version="1.0.0",
)

logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

app.include_router(proxy_router)

@app.get("/")
async def read_root():
    logger.info('测试日志记录是否正常')
    return {"message": "API Gateway is running."}
