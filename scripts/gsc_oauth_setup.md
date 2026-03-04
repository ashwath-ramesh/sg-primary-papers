# Google Search Console (GSC) – Server OAuth Setup

This setup creates a refresh token (offline access) for the Search Console API.

## 0) Choose the property id
For a **Domain property** for the subdomain, use:

- `sc-domain:sgprimarypapers.millisecondlabs.com`

(If your domain property is instead the apex domain, use `sc-domain:millisecondlabs.com` and filter pages by hostname.)

## 1) Create OAuth credentials (Google Cloud Console)
- Create a Google Cloud project
- Enable **Google Search Console API**
- Configure OAuth consent screen (add yourself as a test user if needed)
- Create **OAuth client ID → Desktop app**
- Download the client JSON

## 2) Put the client JSON on the server
Copy it to (example):

- `~/.openclaw/secrets/gsc-client.json`

Permissions:

```bash
mkdir -p ~/.openclaw/secrets
chmod 700 ~/.openclaw/secrets
chmod 600 ~/.openclaw/secrets/gsc-client.json
```

## 3) Install Python deps (once)
From the OpenClaw workspace:

```bash
cd /home/ash/.openclaw/workspace
python3 -m venv .venv || true
. .venv/bin/activate
pip install -U pip
pip install google-auth google-auth-oauthlib google-api-python-client
```

## 4) Run the console auth flow

```bash
. /home/ash/.openclaw/workspace/.venv/bin/activate
python3 /home/ash/.openclaw/workspace/sg-primary-papers/scripts/gsc_auth_console.py \
  --client /home/ash/.openclaw/secrets/gsc-client.json \
  --scopes https://www.googleapis.com/auth/webmasters.readonly
```

It will print a URL.
- Open it in your browser
- Approve
- Paste the resulting code back into the server terminal

The script will output a **refresh token**.

## 5) Save secrets in ~/.openclaw/.env
Suggested vars:

- `GSC_SITE=sc-domain:sgprimarypapers.millisecondlabs.com`
- `GSC_CLIENT_JSON=/home/ash/.openclaw/secrets/gsc-client.json`
- `GSC_REFRESH_TOKEN=...`

Then restart OpenClaw so env vars load.
