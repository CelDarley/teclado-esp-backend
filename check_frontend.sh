#!/bin/bash

# ========================================
# SCRIPT PARA VERIFICAR FRONTEND
# ========================================
# Verifica se o frontend está rodando no servidor

SERVER_IP="10.102.0.108"
SERVER_USER="darley"
SERVER_PATH="/home/darley/teclado-esp-frontend"

echo "🔍 VERIFICANDO STATUS DO FRONTEND"
echo "📡 Servidor: $SERVER_IP"
echo "========================================"

# Verificar se o processo está rodando
echo "🔍 Verificando processo do servidor web..."
ssh "$SERVER_USER@$SERVER_IP" "ps aux | grep server_web.py | grep -v grep"

if [ $? -eq 0 ]; then
    echo "✅ Servidor web está rodando!"
else
    echo "❌ Servidor web não está rodando."
fi

# Verificar se a porta 3000 está em uso
echo "🔍 Verificando porta 3000..."
ssh "$SERVER_USER@$SERVER_IP" "netstat -tlnp | grep :3000"

# Verificar se os arquivos existem
echo "🔍 Verificando arquivos do frontend..."
ssh "$SERVER_USER@$SERVER_IP" "ls -la $SERVER_PATH/"

# Testar conexão HTTP
echo "🔍 Testando conexão HTTP..."
curl -s -o /dev/null -w "Status: %{http_code}\n" "http://$SERVER_IP:3000" || echo "❌ Não foi possível conectar ao frontend"

echo "========================================"
echo "🌐 URL do frontend: http://$SERVER_IP:3000"
echo "📊 Logs: ssh $SERVER_USER@$SERVER_IP 'tail -f $SERVER_PATH/server.log'" 