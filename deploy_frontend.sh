#!/bin/bash

# ========================================
# SCRIPT DE DEPLOY DO FRONTEND
# ========================================
# Deploy do frontend Vue.js para o servidor 10.102.0.108

set -e

# Configurações
SERVER_IP="10.102.0.108"
SERVER_USER="darley"
SERVER_PATH="/home/darley/teclado-esp-frontend"
LOCAL_FRONTEND_DIR="frontend"
BUILD_DIR="dist"

echo "🚀 INICIANDO DEPLOY DO FRONTEND"
echo "📡 Servidor: $SERVER_IP"
echo "👤 Usuário: $SERVER_USER"
echo "📁 Diretório: $SERVER_PATH"
echo "========================================"

# Verificar se o diretório frontend existe
if [ ! -d "$LOCAL_FRONTEND_DIR" ]; then
    echo "❌ ERRO: Diretório frontend não encontrado!"
    exit 1
fi

echo "📦 Instalando dependências..."
cd "$LOCAL_FRONTEND_DIR"
npm install

echo "🔨 Fazendo build do frontend..."
npm run build

if [ ! -d "$BUILD_DIR" ]; then
    echo "❌ ERRO: Build falhou! Diretório dist não foi criado."
    exit 1
fi

echo "✅ Build concluído com sucesso!"

# Criar diretório no servidor se não existir
echo "📁 Criando diretório no servidor..."
ssh "$SERVER_USER@$SERVER_IP" "mkdir -p $SERVER_PATH"

# Copiar arquivos para o servidor
echo "📤 Copiando arquivos para o servidor..."
scp -r "$BUILD_DIR"/* "$SERVER_USER@$SERVER_IP:$SERVER_PATH/"

echo "✅ Frontend copiado para o servidor!"

# Criar script de servidor web simples
echo "🌐 Configurando servidor web..."
cat > server_web.py << 'EOF'
#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys

PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    print(f"🌐 Servidor web rodando em http://0.0.0.0:{PORT}")
    print(f"📁 Diretório: {DIRECTORY}")
    print("🛑 Pressione Ctrl+C para parar")
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor parado.")
EOF

# Copiar script do servidor web
scp server_web.py "$SERVER_USER@$SERVER_IP:$SERVER_PATH/"

# Criar script de inicialização
cat > start_frontend.sh << EOF
#!/bin/bash
cd $SERVER_PATH
python3 server_web.py
EOF

scp start_frontend.sh "$SERVER_USER@$SERVER_IP:$SERVER_PATH/"

# Dar permissões de execução
ssh "$SERVER_USER@$SERVER_IP" "chmod +x $SERVER_PATH/server_web.py $SERVER_PATH/start_frontend.sh"

echo "✅ Scripts de servidor web criados!"

# Verificar se há processos rodando na porta 3000
echo "🔍 Verificando processos na porta 3000..."
ssh "$SERVER_USER@$SERVER_IP" "pkill -f 'server_web.py' || true"

echo "🚀 Iniciando servidor web..."
ssh "$SERVER_USER@$SERVER_IP" "cd $SERVER_PATH && nohup python3 server_web.py > server.log 2>&1 &"

echo "✅ DEPLOY CONCLUÍDO!"
echo "========================================"
echo "🌐 Frontend disponível em: http://$SERVER_IP:3000"
echo "📊 Logs do servidor: $SERVER_PATH/server.log"
echo "🛑 Para parar o servidor: ssh $SERVER_USER@$SERVER_IP 'pkill -f server_web.py'"
echo "🔄 Para reiniciar: ssh $SERVER_USER@$SERVER_IP 'cd $SERVER_PATH && ./start_frontend.sh'"

# Limpar arquivos temporários
rm -f server_web.py start_frontend.sh

echo "🧹 Arquivos temporários removidos!" 