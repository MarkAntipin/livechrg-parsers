import logging

import httpx

from utils.make_get_request import logger
from utils.setup_logger import setup_logger

logger = logging.getLogger(__name__)
setup_logger(logger)


def make_post_request(
        *,
        url: str,
        json_arg: dict | None = None,
        params: dict | None = None,
        timeout: httpx.Timeout | None = None,
        headers: dict | None = None,
) -> httpx.Response | None:
    client = httpx.Client(timeout=timeout)

    response = client.post(
        url,
        headers=headers,
        params=params,
        json = json_arg,
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
