import logging 
from fastapi import APIRouter, Request, Response
from app.services.forwarder import forward_request

router = APIRouter()
logger = logging.getLogger(__name__)

@router.api_route("/{channel}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy(channel: str, path: str, request: Request) -> Response:
    logger.info(f'测试proxy是否被正常记录,channel:{channel},path:{path},request:{request}')
    return await forward_request(channel, request)
