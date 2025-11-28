# Changelog

All notable changes for the project are recorded in this file.

## [v1.0.0] - 2025-11-28

### Added

- Integration with official `gigachat` Python SDK (preferred client path).
- `analysis_service` updated to set `session_id` in `gigachat.context.session_id_cvar` when provided.
- `GIGACHAT_BASE_URL` and `GIGACHAT_OAUTH_URL` configuration support in `app/api/giga_chat.py`.
- `ProxyAPI` support with `PROXY_ENABLED` flag and `PROXY_BASE_URL` environment variables.
- New endpoint `/api/proxy-analyze` that accepts up to 50 rows and returns analysis from Proxy AI.
- Unit test `tests/test_proxy.py` verifying Proxy disabled behavior.
- `README.md` updated with setup and run instructions.

### Changed

- Fallback and token acquisition logic: try SDK token exchange first, then environment token, then OAuth fallback.
- `AnalysisService` prefers official `gigachat` client and falls back to wrapper API when library not available.

### Fixed

- Pass `X-Session-ID` to both SDK and wrapper flows to support GigaChat session caching.
- Skip Proxy calls when disabled by config (clear logging and responses).

### Removed

- Temporary test scripts cleaned up from repo.

### Notes

- Development convenience: `verify_ssl_certs=False` used in SDK initialization to match earlier bot behavior. Disable in production.
- Ensure secrets are stored securely and not pushed to public repos.
