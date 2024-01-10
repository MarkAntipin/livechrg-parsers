import httpx
from utils.logger import create_logger

logger = create_logger()


def make_request(
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
            "Status code %s: %$ while requesting $s",
            exc.response.status_code,
            exc.response.text,
            exc.request.url
        )
