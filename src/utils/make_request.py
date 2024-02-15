import logging

import httpx

from src.utils.setup_logger import setup_logger

logger = logging.getLogger(__name__)
setup_logger(logger)


def make_request(
        *,
        url: str,
        method: str = 'GET',
        json: dict | None = None,
        headers: dict | None = None,
        params: dict | None = None,
) -> httpx.Response | None:
    response = httpx.request(
        method=method,
        url=url,
        headers=headers,
        params=params,
        json=json,
    )
    logger.info('Request %s %s', method, url)
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        logger.error(
            'Status code %s: %s while requesting %s',
            exc.response.status_code,
            exc.response.text,
            exc.request.url
        )
        return None
    logger.info('Response %d', response.status_code)
    return response
