#!/usr/bin/env bash
set -euo pipefail

CLAWDBOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${CLAWDBOT_DIR}/.." && pwd)"
REGISTRY_FILE="${CLAWDBOT_DIR}/active-tasks.json"
LOG_DIR="${CLAWDBOT_DIR}/logs"
mkdir -p "$LOG_DIR"

need_bin() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required binary: $1" >&2
    exit 2
  }
}

now_ms() {
  python3 - <<'PY'
import time
print(int(time.time()*1000))
PY
}

jqr() {
  jq -r "$@"
}

registry_read() {
  cat "$REGISTRY_FILE"
}

registry_write() {
  local tmp
  tmp="${REGISTRY_FILE}.tmp"
  cat >"$tmp"
  mv "$tmp" "$REGISTRY_FILE"
}

registry_get_by_id() {
  local id="$1"
  registry_read | jq --arg id "$id" '.[] | select(.id==$id)'
}

registry_upsert() {
  local obj_json="$1"
  local id
  id=$(echo "$obj_json" | jq -r '.id')
  registry_read \
    | jq --arg id "$id" --argjson obj "$obj_json" '
        (map(select(.id!=$id)) + [$obj])
      ' \
    | registry_write
}

registry_remove_by_id() {
  local id="$1"
  registry_read \
    | jq --arg id "$id" 'map(select(.id!=$id))' \
    | registry_write
}

require_repo_root() {
  if [ ! -d "${REPO_ROOT}/.git" ]; then
    echo "Expected to run inside a git repo (missing ${REPO_ROOT}/.git)" >&2
    exit 2
  fi
}

safe_tmux_has_session() {
  local session="$1"
  tmux has-session -t "$session" 2>/dev/null
}
