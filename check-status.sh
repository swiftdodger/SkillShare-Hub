#!/bin/bash

# SkillShare-Hub Status Check Script
# Run this to verify all services are working

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

resolve_domain() {
  local key value hosts_str host

  if [[ -n "$APP_DOMAIN" ]]; then
    echo "$APP_DOMAIN"
    return
  fi

  if [[ -f "$ENV_FILE" ]]; then
    while IFS='=' read -r key value; do
      key="$(echo "$key" | xargs)"
      value="$(echo "$value" | xargs | tr -d '"')"

      if [[ "$key" == "APP_DOMAIN" && -n "$value" ]]; then
        echo "$value"
        return
      fi

      if [[ "$key" == "ALLOWED_HOSTS" && -n "$value" ]]; then
        hosts_str="${value// /}"
        IFS=',' read -ra host_list <<< "$hosts_str"
        for host in "${host_list[@]}"; do
          host="$(echo "$host" | xargs)"
          if [[ -n "$host" && "$host" != "localhost" && "$host" != "127.0.0.1" ]]; then
            echo "$host"
            return
          fi
        done
      fi
    done < "$ENV_FILE"
  fi

  echo "skillshare.com"
}

DOMAIN=$(resolve_domain)
ALT_DOMAIN="www.${DOMAIN#www.}"

echo "========================================"
echo "🔍 SkillShare-Hub Status Check (domain: $DOMAIN)"
echo "========================================"
echo ""

echo "📦 Docker Containers:"
docker compose ps
echo ""

echo "🌐 Port Status:"
echo "Checking if ports are listening..."
sudo ss -tlnp | grep -E ':(80|443|8000|5433|6379)' || echo "No services found on expected ports"
echo ""

echo "🔗 Testing HTTP Connection:"
curl -I http://localhost 2>&1 | head -5 || echo "❌ HTTP connection failed"
echo ""

echo "🔒 Testing HTTPS Connection:"
curl -Ik https://localhost 2>&1 | head -5 || echo "❌ HTTPS connection failed"
echo ""

echo "📊 Container Logs (last 5 lines each):"
echo ""
echo "--- Nginx ---"
docker compose logs --tail=5 nginx
echo ""
echo "--- Web ---"
docker compose logs --tail=5 web
echo ""
echo "--- Redis ---"
docker compose logs --tail=5 redis
echo ""
echo "--- Database ---"
docker compose logs --tail=5 db
echo ""

echo "========================================"
echo "✅ Status check complete!"
echo "========================================"
echo ""
echo "🌐 Access your application at:"
echo "   HTTP:  http://$DOMAIN (redirects to HTTPS)"
echo "   HTTPS: https://$DOMAIN"
echo ""
echo "📝 To view live logs: docker compose logs -f"
echo "🛑 To stop services: docker compose down"
echo "🔄 To restart: docker compose restart"
