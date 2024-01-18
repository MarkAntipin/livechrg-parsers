import logging

import httpx
from utils.setup_logger import setup_logger

logger = logging.getLogger(__name__)
setup_logger(logger)


def make_get_request(
        *,
        url: str,
        headers: dict | None = None,
        params: dict | None = None,
) -> httpx.Response | None:
    response = httpx.get(
        url,
        headers=headers,
        params=params
    )

    try:
        response.raise_for_status()
        return response
    except httpx.HTTPStatusError as exc:
        logger.error(
            "Status code %s: %s while requesting %s",
            exc.response.status_code,
            exc.response.text,
            exc.request.url
        )
