#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

"""Authenticate with crash.checkmk.com via Google OAuth and cache a bearer token.

Usage:
    PYTHONPATH=.claude/skills python3 -m crash_report.authenticate [--force]

This script:
1. Opens a browser for Google Sign-In
2. Receives the OAuth callback on a local HTTP server
3. Exchanges the Google ID token for a crash.checkmk.com bearer token
4. Caches the bearer token locally for use by fetch_crash_data.py

Options:
    --force    Force re-authentication even if a valid token is cached.

Environment:
    CRASH_REPORTING_GOOGLE_CLIENT_ID      - Google OAuth client ID (required)
    CRASH_REPORTING_GOOGLE_CLIENT_SECRET  - Google OAuth client secret (required for
                                            Web Application type OAuth clients)
    CRASH_REPORTING_TOKEN_CACHE           - Override token cache path
                                            (default: ~/.cache/cmk-crash-reporting/token.json)
"""

import dataclasses
import http.server
import json
import os
import secrets
import socket
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path
from typing import Any

BASE_URL = os.environ.get("CRASH_REPORTING_URL", "https://crash.checkmk.com")
TOKEN_ENDPOINT = f"{BASE_URL}/gui/api/v1/statsapi/auth/token"
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

DEFAULT_CACHE_DIR = Path.home() / ".cache" / "cmk-crash-reporting"
DEFAULT_CACHE_FILE = DEFAULT_CACHE_DIR / "token.json"

# Localhost callback port range
CALLBACK_PORT_START = 18520
CALLBACK_PORT_END = 18530


def _get_cache_path() -> Path:
    return Path(os.environ.get("CRASH_REPORTING_TOKEN_CACHE", str(DEFAULT_CACHE_FILE)))


def _load_cached_token() -> dict[str, Any] | None:
    """Load and validate the cached bearer token."""
    cache_path = _get_cache_path()
    if not cache_path.is_file():
        return None

    try:
        data = json.loads(cache_path.read_text())
    except (json.JSONDecodeError, OSError):
        return None

    # Check expiry (with 60s buffer)
    expires_at = data.get("expires_at", 0)
    if time.time() >= expires_at - 60:
        return None

    return dict(data)  # explicit dict to satisfy mypy (json.loads returns Any)


def _save_token(token: str, expires_in: int) -> None:
    """Cache the bearer token to disk."""
    cache_path = _get_cache_path()
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    now = int(time.time())
    data = {
        "token": token,
        "expires_at": now + expires_in,
        "issued_at": now,
    }
    cache_path.write_text(json.dumps(data, indent=2))
    cache_path.chmod(0o600)


def get_cached_bearer_token() -> str | None:
    """Return a valid cached bearer token, or None if unavailable/expired.

    This is the main entry point for fetch_crash_data.py to get a token.
    """
    data = _load_cached_token()
    if data:
        return str(data["token"])
    return None


def _get_google_client_id() -> str:
    client_id = os.environ.get("CRASH_REPORTING_GOOGLE_CLIENT_ID", "")
    if not client_id:
        raise ValueError(
            "CRASH_REPORTING_GOOGLE_CLIENT_ID environment variable is not set.\n"
            "Get the client ID from the crash.checkmk.com Google OAuth configuration."
        )
    return client_id


def _get_google_client_secret() -> str | None:
    """Return the Google OAuth client secret, or None if not set.

    Required for 'Web Application' type OAuth clients. Desktop/CLI clients
    configured as 'Desktop app' in Google Cloud Console may omit this.
    """
    return os.environ.get("CRASH_REPORTING_GOOGLE_CLIENT_SECRET") or None


@dataclasses.dataclass
class _OAuthResult:
    """Mutable container for OAuth callback results, stored on the server instance."""

    expected_state: str = ""
    auth_code: str | None = None
    auth_error: str | None = None


class _OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler that captures the OAuth callback code."""

    server: "_OAuthHTTPServer"  # type: ignore[mutable-override]

    def do_GET(self) -> None:
        result = self.server.oauth_result
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        error = params.get("error", [None])[0]
        if error:
            result.auth_error = error
            self._respond("Authentication failed. You can close this window.")
            return

        state = params.get("state", [None])[0]
        if state != result.expected_state:
            result.auth_error = "State mismatch (possible CSRF)"
            self._respond("State mismatch error. You can close this window.")
            return

        code = params.get("code", [None])[0]
        if code:
            result.auth_code = code
            self._respond(
                "Authentication successful! You can close this window and return to the terminal."
            )
        else:
            result.auth_error = "No authorization code received"
            self._respond("No authorization code received. You can close this window.")

    def _respond(self, message: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        html = f"<html><body><h2>{message}</h2></body></html>"
        self.wfile.write(html.encode())

    def log_message(self, _format: str, *args: Any) -> None:
        pass  # Suppress HTTP server logs


class _OAuthHTTPServer(http.server.HTTPServer):
    """HTTPServer subclass that carries OAuth result state."""

    def __init__(self, address: tuple[str, int], oauth_result: _OAuthResult) -> None:
        super().__init__(address, _OAuthCallbackHandler)
        self.oauth_result = oauth_result


def _find_available_port() -> int:
    """Find an available port for the callback server."""
    for port in range(CALLBACK_PORT_START, CALLBACK_PORT_END):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(("127.0.0.1", port)) != 0:
                return port
    raise RuntimeError(f"No available port in range {CALLBACK_PORT_START}-{CALLBACK_PORT_END}")


def _exchange_code_for_id_token(
    code: str, client_id: str, client_secret: str | None, redirect_uri: str
) -> str:
    """Exchange the authorization code for a Google ID token."""
    params: dict[str, str] = {
        "code": code,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    if client_secret:
        params["client_secret"] = client_secret
    data = urllib.parse.urlencode(params).encode()

    req = urllib.request.Request(
        GOOGLE_TOKEN_URL,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:  # nosec B310
            token_data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        sys.stderr.write(f"Error exchanging code for token: HTTP {e.code}: {body}\n")
        sys.exit(1)

    id_token = token_data.get("id_token")
    if not id_token:
        sys.stderr.write("Error: No id_token in Google token response.\n")
        sys.exit(1)

    return str(id_token)


def _exchange_for_bearer_token(google_id_token: str) -> tuple[str, int]:
    """Exchange a Google ID token for a crash.checkmk.com bearer token."""
    payload = json.dumps({"id_token": google_id_token}).encode()
    req = urllib.request.Request(
        TOKEN_ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:  # nosec B310
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            error_data = json.loads(body)
            message = error_data.get("message", body)
        except json.JSONDecodeError:
            message = body
        sys.stderr.write(f"Error from crash.checkmk.com: {message}\n")
        sys.exit(1)
    except urllib.error.URLError as e:
        sys.stderr.write(f"Error connecting to crash.checkmk.com: {e.reason}\n")
        sys.exit(1)

    token = data.get("token", "")
    expires_in = data.get("expires_in", 3600)
    if not token:
        sys.stderr.write("Error: No token in server response.\n")
        sys.exit(1)

    return token, expires_in


def _authenticate_local(email: str = "dev@localhost") -> str:
    """Authenticate with a local dev server (JWT_MODE=local) — no Google OAuth needed."""
    payload = json.dumps({"email": email}).encode()
    req = urllib.request.Request(
        TOKEN_ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:  # nosec B310
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        sys.stderr.write(f"Error from server: {body}\n")
        sys.exit(1)
    except urllib.error.URLError as e:
        sys.stderr.write(f"Error connecting to {BASE_URL}: {e.reason}\n")
        sys.exit(1)

    token: str = data.get("token", "")
    expires_in: int = data.get("expires_in", 3600)
    if not token:
        sys.stderr.write("Error: No token in server response.\n")
        sys.exit(1)

    _save_token(token, expires_in)
    print(
        f"Authenticated locally as {email}. Token cached (expires in {expires_in // 60} minutes)."
    )
    return token


def authenticate(force: bool = False, local: bool = False, email: str = "dev@localhost") -> str:
    """Run the authentication flow and return a bearer token.

    If a valid cached token exists and force=False, returns it immediately.

    Args:
        force: Force re-authentication even if a valid token is cached.
        local: Use local JWT mode (no Google OAuth, for development servers).
        email: Email to use in local mode (ignored in Google mode).
    """
    if not force:
        cached = get_cached_bearer_token()
        if cached:
            print("Using cached bearer token (still valid).")
            return cached

    if local:
        return _authenticate_local(email)

    client_id = _get_google_client_id()
    client_secret = _get_google_client_secret()
    port = _find_available_port()
    redirect_uri = f"http://127.0.0.1:{port}"

    # Generate CSRF state and result container
    oauth_result = _OAuthResult(expected_state=secrets.token_urlsafe(32))

    # Build Google OAuth URL
    auth_params = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "state": oauth_result.expected_state,
            "access_type": "offline",
            "prompt": "select_account",
        }
    )
    auth_url = f"{GOOGLE_AUTH_URL}?{auth_params}"

    # Start local callback server
    server = _OAuthHTTPServer(("127.0.0.1", port), oauth_result)
    server_thread = threading.Thread(target=server.handle_request, daemon=True)
    server_thread.start()

    print("Opening browser for Google Sign-In...")
    print(f"If the browser doesn't open, visit:\n  {auth_url}\n")
    webbrowser.open(auth_url)

    # Wait for callback
    server_thread.join(timeout=120)
    server.server_close()

    if oauth_result.auth_error:
        sys.stderr.write(f"Authentication error: {oauth_result.auth_error}\n")
        sys.exit(1)

    if not oauth_result.auth_code:
        sys.stderr.write("Authentication timed out (120s).\n")
        sys.exit(1)

    print("Exchanging authorization code for tokens...")
    google_id_token = _exchange_code_for_id_token(
        oauth_result.auth_code, client_id, client_secret, redirect_uri
    )

    print("Requesting bearer token from crash.checkmk.com...")
    bearer_token, expires_in = _exchange_for_bearer_token(google_id_token)

    _save_token(bearer_token, expires_in)
    print(f"Authenticated successfully. Token cached (expires in {expires_in // 60} minutes).")
    return bearer_token


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Authenticate with crash.checkmk.com")
    parser.add_argument("--force", action="store_true", help="Force re-authentication")
    parser.add_argument(
        "--local",
        action="store_true",
        help="Use local JWT mode (no Google OAuth, for development servers)",
    )
    parser.add_argument(
        "--email",
        default="dev@localhost",
        help="Email to use in local mode (default: dev@localhost)",
    )
    args = parser.parse_args()
    authenticate(force=args.force, local=args.local, email=args.email)


if __name__ == "__main__":
    main()
