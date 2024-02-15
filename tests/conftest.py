import json
from pathlib import Path

import pytest

LIVE_CHARGE_BASE_URL = 'https://livechrg.com'
CHARGE_POINT_BASE_URL = 'https://chargepoint.com'
CHARGE_POINT_COMMENTS_URL = 'https://chargepoint.comments.com'
CHARGE_POINT_AUTH_TOKEN = 'TOKEN'
PLUG_SHARE_BASE_URL = 'https://plugshare.com'


@pytest.fixture
def charge_point_api(respx_mock):
    def _inner(method: str, uri: str):
        return respx_mock.request(f'{CHARGE_POINT_BASE_URL}{uri}', method=method)
    return _inner


@pytest.fixture
def charge_point_comments_api(respx_mock):
    def _inner(method: str, uri: str):
        return respx_mock.request(f'{CHARGE_POINT_COMMENTS_URL}{uri}', method=method)
    return _inner


@pytest.fixture
def live_charge_api(respx_mock):
    def _inner(method: str, uri: str):
        return respx_mock.request(f'{LIVE_CHARGE_BASE_URL}{uri}', method=method)
    return _inner


@pytest.fixture
def plug_share_api(respx_mock):
    def _inner(method: str, uri: str):
        return respx_mock.request(f'{PLUG_SHARE_BASE_URL}{uri}', method=method)
    return _inner


@pytest.fixture
def plug_share_info() -> dict:
    with open(Path('tests', 'data', 'plug_share_info.json'), 'r') as f:
        data = json.load(f)
    return data


@pytest.fixture
def plug_share_comments() -> dict:
    with open(Path('tests', 'data', 'plug_share_comments.json'), 'r') as f:
        data = json.load(f)
    return data


@pytest.fixture
def charge_point_info() -> dict:
    with open(Path('tests', 'data', 'charge_point_info.json'), 'r') as f:
        data = json.load(f)
    return data


@pytest.fixture(autouse=True)
async def env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv('LIVE_CHARGE_BASE_URL', LIVE_CHARGE_BASE_URL)
    monkeypatch.setenv('CHARGE_POINT_BASE_URL', CHARGE_POINT_BASE_URL)
    monkeypatch.setenv('CHARGE_POINT_AUTH_TOKEN', CHARGE_POINT_AUTH_TOKEN)
    monkeypatch.setenv('PLUG_SHARE_BASE_URL', PLUG_SHARE_BASE_URL)
    monkeypatch.setenv('CHARGE_POINT_COMMENTS_URL', CHARGE_POINT_COMMENTS_URL)
