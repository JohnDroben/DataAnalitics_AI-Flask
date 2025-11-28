import os
import pytest

from app.api.proxy_api import ProxyAPI


def test_proxy_disabled(monkeypatch):
    # Ensure PROXY_ENABLED=false causes ProxyAPI to disable calls
    monkeypatch.setenv('PROXY_ENABLED', 'false')
    monkeypatch.setenv('PROXY_API_KEY', 'dummy_key')

    p = ProxyAPI()
    assert p.enabled is False

    with pytest.raises(Exception) as exc:
        p.send_analysis_request('test')

    assert 'disabled' in str(exc.value).lower()
