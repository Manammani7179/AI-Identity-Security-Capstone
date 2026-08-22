import os
import secrets
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

import requests
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
CALLBACK_URL = os.getenv(
    "AUTH0_CALLBACK_URL",
    "http://localhost:3000/callback"
)

if not all([DOMAIN, CLIENT_ID, CLIENT_SECRET]):
    raise RuntimeError(
        "Missing AUTH0_DOMAIN, AUTH0_CLIENT_ID, or AUTH0_CLIENT_SECRET in .env"
    )

authorization_code = None
state = secrets.token_urlsafe(24)


class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global authorization_code

        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        returned_state = params.get("state", [None])[0]
        authorization_code = params.get("code", [None])[0]

        if returned_state != state:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"State verification failed.")
            return

        if not authorization_code:
            error = params.get("error", ["unknown"])[0]
            description = params.get("error_description", [""])[0]

            self.send_response(400)
            self.end_headers()
            self.wfile.write(
                f"Auth0 error: {error} {description}".encode()
            )
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(
            b"<h2>Authorization successful.</h2>"
            b"<p>You can close this browser window.</p>"
        )

    def log_message(self, format, *args):
        return


print("=" * 70)
print("SECURENOVA PROJECT 4 - AUTH0 REFRESH TOKEN ROTATION TEST")
print("=" * 70)

server = HTTPServer(("localhost", 3000), CallbackHandler)

thread = threading.Thread(target=server.handle_request)
thread.start()

authorization_url = (
    f"https://{DOMAIN}/authorize"
    f"?response_type=code"
    f"&client_id={CLIENT_ID}"
    f"&redirect_uri={CALLBACK_URL}"
    f"&scope=openid%20profile%20offline_access"
    f"&audience=https%3A%2F%2Fai-chat-api"
    f"&state={state}"
)

print()
print("Opening Auth0 login in your browser...")
webbrowser.open(authorization_url)

thread.join()
server.server_close()

if not authorization_code:
    raise RuntimeError("Authorization code was not received.")

print()
print("Authorization code received successfully.")

token_url = f"https://{DOMAIN}/oauth/token"

token_response = requests.post(
    token_url,
    json={
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": authorization_code,
        "redirect_uri": CALLBACK_URL,
    },
    timeout=30,
)

token_data = token_response.json()

if token_response.status_code != 200:
    print("Token exchange failed:")
    print(token_data)
    raise SystemExit(1)

old_refresh_token = token_data.get("refresh_token")

if not old_refresh_token:
    print()
    print("ERROR: Auth0 did not return a refresh token.")
    print("Check that offline_access and Refresh Token are enabled.")
    raise SystemExit(1)

print()
print("Initial refresh token received successfully.")

# ---------------------------------------------------------
# First refresh-token exchange
# ---------------------------------------------------------

refresh_response = requests.post(
    token_url,
    json={
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": old_refresh_token,
    },
    timeout=30,
)

refresh_data = refresh_response.json()

if refresh_response.status_code != 200:
    print()
    print("First refresh failed:")
    print(refresh_data)
    raise SystemExit(1)

new_refresh_token = refresh_data.get("refresh_token")

print()
print("First refresh-token exchange: SUCCESS")
print("New refresh token issued:", bool(new_refresh_token))

if not new_refresh_token:
    print()
    print("ERROR: Auth0 did not return a replacement refresh token.")
    print("Verify that Refresh Token Rotation is enabled.")
    raise SystemExit(1)

# ---------------------------------------------------------
# Replay the OLD refresh token
# ---------------------------------------------------------

print()
print("Attempting to reuse the OLD refresh token...")
print()

replay_response = requests.post(
    token_url,
    json={
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": old_refresh_token,
    },
    timeout=30,
)

replay_data = replay_response.json()

print("Auth0 HTTP status:", replay_response.status_code)
print("Auth0 response:", replay_data)

if replay_response.status_code != 200:
    print()
    print("REFRESH TOKEN REPLAY DETECTED")
    print("STATUS : REJECTED")
    print("REASON : Old refresh token was rejected by Auth0 after rotation.")
else:
    print()
    print("WARNING: Old refresh token was accepted.")
    print("Rotation/reuse detection is not working as expected.")

print("=" * 70)