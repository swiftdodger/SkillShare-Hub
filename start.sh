#!/bin/bash

# SkillShare-Hub Startup Script
# This script will start all Docker containers in the correct order

set -e

echo "🛑 Stopping host nginx if running..."
sudo systemctl stop nginx 2>/dev/null || true
sudo systemctl disable nginx 2>/dev/null || true

echo "🔍 Forcefully freeing ports 80 and 443..."
sudo fuser -k 80/tcp 2>/dev/null || true
sudo fuser -k 443/tcp 2>/dev/null || true
sleep 2

echo "🧹 Cleaning up old containers..."
docker compose down -v 2>/dev/null || true
sleep 3

echo "🔍 Verifying ports are free..."
# Check for LISTENING sockets only (sTATE == LISTEN)
if sudo ss -ltn | grep -qE ':80\s'; then
    echo "⚠️  Warning: Port 80 is being listened on!"
    sudo ss -ltnp | grep ':80'
    exit 1
fi
if sudo ss -ltn | grep -qE ':443\s'; then
    echo "⚠️  Warning: Port 443 is being listened on!"
    sudo ss -ltnp | grep ':443'
    exit 1
fi

echo "✅ Ports 80 and 443 are free for binding!"

echo "🔨 Building web container with health check support..."
docker compose build web

echo "🚀 Starting all services..."
docker compose up -d

echo "⏳ Waiting for services to be healthy..."
sleep 15

echo "📊 Checking container status..."
docker compose ps

echo ""
echo "✅ Services should be starting up!"
echo ""
echo "📝 To view logs:"
echo "   docker compose logs -f"
echo ""
echo "🌐 Access your application:"
echo "   HTTP:  http://skillforge.bg(redirects to HTTPS)"
echo "   HTTPS: https://skillforge.bg"
echo ""
echo "⚠️  You will see a browser warning about self-signed certificate."
echo "    Click 'Advanced' and 'Proceed' to continue."

