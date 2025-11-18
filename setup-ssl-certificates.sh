#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# SkillShare-Hub Production SSL Bootstrapper
# ------------------------------------------------------------------------------
# Provisions Let's Encrypt certificates for the Django + nginx + Docker stack.
# - Validates prerequisites (root, args, tooling, DNS hint)
# - Stops docker-compose stack (frees ports 80/443 for standalone certbot)
# - Installs certbot if missing
# - Requests certificates for DOMAIN + optional WWW_DOMAIN
# - Updates nginx + .env placeholders with the new domain
# - Restarts docker-compose stack and performs smoke checks
# - Creates/refreshes a cron job for automatic renewals
# ------------------------------------------------------------------------------
# Usage:
#   sudo ./setup-ssl-certificates.sh example.com admin@example.com [www.example.com]
# ------------------------------------------------------------------------------

set -Eeuo pipefail
trap 'echo "❌ Error on line $LINENO. Aborting." >&2' ERR

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$PROJECT_ROOT/docker-compose.yml"
NGINX_CONF="$PROJECT_ROOT/nginx/nginx.conf"
ENV_FILE="$PROJECT_ROOT/.env"
CERTBOT_WEBROOT="/var/www/certbot"
LE_DIR="/etc/letsencrypt"
CRON_MARKER="# skillshare-hub-certbot"

usage() {
  cat <<EOF
Usage: sudo $(basename "$0") DOMAIN EMAIL [ALT_DOMAIN]

Arguments:
  DOMAIN       Primary domain (e.g., skillforge.com)
  EMAIL        Email for Let's Encrypt renewal notices
  ALT_DOMAIN   Optional secondary domain (defaults to www.DOMAIN)

Requirements:
  - Run as root (sudo)
  - DOMAIN DNS A/AAAA records point to this server's public IP
  - Ports 80/443 reachable from the internet
EOF
}

require_root() {
  if [[ "${EUID}" -ne 0 ]]; then
    echo "❌ This script must be run with sudo/root privileges." >&2
    usage
    exit 1
  fi
}

require_args() {
  if [[ $# -lt 2 ]]; then
    echo "❌ Missing arguments." >&2
    usage
    exit 1
  fi
  DOMAIN="$1"
  EMAIL="$2"
  ALT_DOMAIN="${3:-www.$DOMAIN}"
  export DOMAIN EMAIL ALT_DOMAIN
}

require_files() {
  for file in "$COMPOSE_FILE" "$NGINX_CONF" "$ENV_FILE"; do
    if [[ ! -f "$file" ]]; then
      echo "❌ Required file not found: $file" >&2
      exit 1
    fi
  done
}

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "❌ Required command '$cmd' not found. Install it and retry." >&2
    exit 1
  fi
}

install_certbot() {
  if command -v certbot >/dev/null 2>&1; then
    echo "✅ certbot already installed"
    return
  fi
  echo "🔧 Installing certbot via snap..."
  require_cmd snap
  snap install core >/dev/null 2>&1 || true
  snap refresh core >/dev/null 2>&1 || true
  snap install --classic certbot >/dev/null 2>&1
  ln -sf /snap/bin/certbot /usr/bin/certbot
  echo "✅ certbot installed"
}

hint_dns() {
  if command -v dig >/dev/null 2>&1; then
    local ip
    ip=$(curl -s https://ifconfig.me || true)
    echo "🌐 Public IP detected: ${ip:-unknown}"
    echo "🔎 DNS A records (dig):"
    dig +short "$DOMAIN" || true
  else
    echo "ℹ️ Install 'dnsutils' to get dig output." >&2
  fi
}

prep_certbot_dirs() {
  mkdir -p "$CERTBOT_WEBROOT"
  chmod 755 "$CERTBOT_WEBROOT"
}

stop_stack() {
  if [[ -n $(docker ps -q 2>/dev/null) ]]; then
    echo "🛑 Stopping docker-compose services..."
    docker compose -f "$COMPOSE_FILE" down || true
  fi
}

obtain_certificates() {
  echo "🔐 Requesting Let's Encrypt certificates for $DOMAIN $ALT_DOMAIN"
  certbot certonly --standalone \
    --preferred-challenges http \
    --agree-tos \
    --no-eff-email \
    --email "$EMAIL" \
    -d "$DOMAIN" \
    -d "$ALT_DOMAIN"
  echo "✅ Certificates issued at $LE_DIR/live/$DOMAIN"
}

update_nginx_config() {
  echo "📝 Updating nginx configuration with $DOMAIN"
  sed -i "s/server_name[^;]*/server_name $DOMAIN $ALT_DOMAIN/" "$NGINX_CONF"
  sed -i "s#/etc/letsencrypt/live/.*/fullchain.pem#/etc/letsencrypt/live/$DOMAIN/fullchain.pem#g" "$NGINX_CONF"
  sed -i "s#/etc/letsencrypt/live/.*/privkey.pem#/etc/letsencrypt/live/$DOMAIN/privkey.pem#g" "$NGINX_CONF"
}

update_env_file() {
  echo "📝 Updating .env ALLOWED_HOSTS"
  if grep -q "ALLOWED_HOSTS" "$ENV_FILE"; then
    sed -i "s/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=localhost,127.0.0.1,$DOMAIN,$ALT_DOMAIN/" "$ENV_FILE"
  else
    echo "ALLOWED_HOSTS=localhost,127.0.0.1,$DOMAIN,$ALT_DOMAIN" >>"$ENV_FILE"
  fi
}

start_stack() {
  echo "🚀 Starting docker-compose services..."
  docker compose -f "$COMPOSE_FILE" up -d --build
  echo "⏳ Waiting for services to stabilize..."
  sleep 20
  docker compose -f "$COMPOSE_FILE" ps
}

smoke_tests() {
  echo "🩺 Running HTTPS smoke test"
  curl -kI "https://$DOMAIN" | head -n 5 || true
}

setup_cron() {
  echo "⏰ Configuring certbot auto-renewal cron job"
  local cron_line="0 3 * * * certbot renew --quiet --deploy-hook 'docker compose -f $COMPOSE_FILE restart nginx' $CRON_MARKER"
  (crontab -l 2>/dev/null | grep -v "$CRON_MARKER"; echo "$cron_line") | crontab -
}

summary() {
  cat <<EOF
🎉 SSL provisioning complete!

Domain:        $DOMAIN
Alt Domain:    $ALT_DOMAIN
Certificates:  $LE_DIR/live/$DOMAIN/
Nginx config:  $NGINX_CONF
.env hosts:    $(grep '^ALLOWED_HOSTS' "$ENV_FILE")

Verify in browser: https://$DOMAIN
Cron job: $(crontab -l 2>/dev/null | grep "$CRON_MARKER" | sed 's/^/  /')
EOF
}

main() {
  require_root
  require_args "$@"
  require_files
  require_cmd docker
  require_cmd curl
  install_certbot
  hint_dns
  prep_certbot_dirs
  stop_stack
  obtain_certificates
  update_nginx_config
  update_env_file
  start_stack
  smoke_tests
  setup_cron
  summary
}

main "$@"

