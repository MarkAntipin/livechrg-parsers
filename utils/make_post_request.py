import logging

import httpx

from utils.make_get_request import logger
from utils.setup_logger import setup_logger

logger = logging.getLogger(__name__)
setup_logger(logger)


def make_post_request(
        *,
        url: str,
        headers: dict | None = None,
        params: dict | None = None,
        json: dict | None = None,
) -> httpx.Response | None:
    timeout = httpx.Timeout(10, read=60)
    client = httpx.Client(timeout=timeout)

    response = client.post(
        url,
        headers=headers,
        params=params,
        json = json
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
