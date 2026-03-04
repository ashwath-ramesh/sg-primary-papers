#!/usr/bin/env bash
set -euo pipefail

# Load OpenClaw/Umami secrets if present (UMAMI_* vars).
# NOTE: This script does NOT echo secrets.
ENV_FILE="$HOME/.openclaw/.env"
if [ -f "$ENV_FILE" ]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

CHAT_TARGET=${UMAMI_REPORT_TARGET:-"telegram:7675806783"}
BASE=${UMAMI_BASE:-"https://analytics.millisecondlabs.com"}
WID=${UMAMI_WEBSITE_ID:-"620b5939-4f56-49f3-9eac-0141f805d3a5"}
SITE_NAME=${UMAMI_SITE_NAME:-"SG Primary Papers"}
SITE_DOMAIN=${UMAMI_WEBSITE_DOMAIN:-"sgprimarypapers.millisecondlabs.com"}

REPORT=$(python3 - <<'PY'
import os, json, urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

BASE=(os.environ.get('UMAMI_BASE') or 'https://analytics.millisecondlabs.com').rstrip('/')
USER=os.environ.get('UMAMI_USERNAME')
PW=os.environ.get('UMAMI_PASSWORD')
WID=os.environ.get('UMAMI_WEBSITE_ID','620b5939-4f56-49f3-9eac-0141f805d3a5')
SITE_NAME=os.environ.get('UMAMI_SITE_NAME','SG Primary Papers')
SITE_DOMAIN=os.environ.get('UMAMI_WEBSITE_DOMAIN','sgprimarypapers.millisecondlabs.com')

if not USER or not PW:
    raise SystemExit('Missing UMAMI_USERNAME/UMAMI_PASSWORD')

H={'Content-Type':'application/json','Accept':'application/json','User-Agent':'openclaw-cron/1.0'}

def jreq(method, url, data=None, headers=None):
    h=dict(H)
    if headers: h.update(headers)
    body=None
    if data is not None:
        body=json.dumps(data).encode('utf-8')
    req=urllib.request.Request(url, data=body, headers=h, method=method)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

# Login
login=jreq('POST', BASE+'/api/auth/login', {'username':USER,'password':PW})
token=login.get('token')
if not token:
    raise SystemExit('Login ok but token missing')
auth={'Authorization':f'Bearer {token}'}

# Windows: last 24h vs previous 24h (rolling)
end=datetime.now(tz=ZoneInfo('Asia/Singapore'))
start_24=end-timedelta(hours=24)
start_prev=end-timedelta(hours=48)

end_ms=int(end.timestamp()*1000)
start_24_ms=int(start_24.timestamp()*1000)
start_prev_ms=int(start_prev.timestamp()*1000)

cur=jreq('GET', f'{BASE}/api/websites/{WID}/stats?startAt={start_24_ms}&endAt={end_ms}', headers=auth)
prev=jreq('GET', f'{BASE}/api/websites/{WID}/stats?startAt={start_prev_ms}&endAt={start_24_ms}', headers=auth)

# Top paths for last 24h
paths=jreq('GET', f'{BASE}/api/websites/{WID}/metrics?type=path&startAt={start_24_ms}&endAt={end_ms}', headers=auth)[:8]


def pct(delta, base):
    if base in (0, None):
        return None
    return (delta/base)*100

lines=[]
lines.append(f"{SITE_NAME} — Umami daily (rolling 24h)\n{SITE_DOMAIN}")

def row(label, key):
    c=cur.get(key,0)
    p=prev.get(key,0)
    d=c-p
    change=pct(d,p)
    if change is None:
        ch='—'
    else:
        ch=('+' if change>=0 else '')+f"{change:.0f}%"
    sign='+' if d>=0 else ''
    lines.append(f"- {label}: {c} ({sign}{d} vs prev 24h, {ch})")

row('Pageviews','pageviews')
row('Visitors','visitors')
row('Visits','visits')
row('Bounces','bounces')

# Derived
try:
    cur_visits=cur.get('visits',0) or 0
    prev_visits=prev.get('visits',0) or 0
    cur_br=(min(cur.get('visits',0),cur.get('bounces',0))/cur_visits*100) if cur_visits else None
    prev_br=(min(prev.get('visits',0),prev.get('bounces',0))/prev_visits*100) if prev_visits else None
    if cur_br is not None and prev_br is not None:
        diff=cur_br-prev_br
        lines.append(f"- Bounce rate: {cur_br:.0f}% ({diff:+.0f} pp vs prev 24h)")
except Exception:
    pass

if paths:
    lines.append("\nTop paths (24h):")
    for it in paths:
        lines.append(f"- {it.get('x')}: {it.get('y')}")

lines.append(f"\nWindow: {start_24.strftime('%Y-%m-%d %H:%M')} → {end.strftime('%Y-%m-%d %H:%M')} (Asia/Singapore)")

print('\n'.join(lines))
PY
)

# Send to Telegram via OpenClaw gateway.
openclaw message send --target "$CHAT_TARGET" --message "$REPORT" >/dev/null
