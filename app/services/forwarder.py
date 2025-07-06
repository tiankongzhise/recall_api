import httpx
import logging
from fastapi import Request, Response
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from app.core.config import settings

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(settings.RETRY_COUNT),
    wait=wait_fixed(settings.RETRY_DELAY),
    retry=retry_if_exception_type(httpx.RequestError),
    before_sleep=lambda retry_state: logger.warning(f"Retrying request, attempt {retry_state.attempt_number}")
)
async def forward_request(channel: str, request: Request) -> Response:
    logger.info(f'forward is running,channel:{channel},request:{request}')
    base_url = settings.FORWARD_RULES.get(channel)
    if not base_url:
        logger.error(f"Unknown channel: {channel}")
        return Response(content=f"Unknown channel: {channel}", status_code=400)

    async with httpx.AsyncClient() as client:
        url = f"{base_url}{request.url.path}"
        headers = dict(request.headers)
        headers.pop("host", None)

        logger.info(f"Forwarding request to {url}")

        try:
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                params=request.query_params,
                content=await request.body(),
                timeout=30.0,
            )

            logger.info(f"Received response with status code {response.status_code}")
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
            )
        except httpx.RequestError as e:
            logger.error(f"Request to {url} failed: {e}")
            raise
