#!/usr/bin/env python3
"""Console OAuth flow to obtain a refresh token for Google Search Console API.

Usage:
  python3 gsc_auth_console.py --client /path/to/client.json \
    --scopes https://www.googleapis.com/auth/webmasters.readonly

Outputs:
  Prints refresh_token to stdout.
"""

import argparse
import json
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client", required=True, help="Path to OAuth client JSON (Desktop app)")
    ap.add_argument(
        "--scopes",
        default="https://www.googleapis.com/auth/webmasters.readonly",
        help="OAuth scopes (space-separated or repeatable)",
    )
    args = ap.parse_args()

    client_path = Path(args.client).expanduser()
    if not client_path.exists():
        raise SystemExit(f"Client JSON not found: {client_path}")

    scopes = args.scopes.split()

    # Use console flow (works on headless servers).
    flow = InstalledAppFlow.from_client_secrets_file(str(client_path), scopes=scopes)
    creds = flow.run_console()

    if not creds.refresh_token:
        raise SystemExit(
            "No refresh token returned. Common causes: you previously authorized this client; "
            "try deleting prior grants at https://myaccount.google.com/permissions and re-run."
        )

    print(creds.refresh_token)


if __name__ == "__main__":
    main()
