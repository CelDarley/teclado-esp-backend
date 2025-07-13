#!/bin/bash

echo "🚀 Deploy do Backend Django para 10.102.0.10"
echo "=============================================="

# Configurações
SERVER_IP="10.102.0.108"
SERVER_USER="darley"  # Ajuste se necessário
BACKEND_DIR="/home/darley/teclado-esp/backend"
REMOTE_DIR="/home/darley/teclado-esp-backend"

echo "📤 Copiando arquivos para $SERVER_IP..."

# Criar diretório no servidor (se não existir)
ssh $SERVER_USER@$SERVER_IP "mkdir -p $REMOTE_DIR"

# Copiar arquivos do backend (excluindo venv e .git)
rsync -avz --exclude='venv/' --exclude='.git/' --exclude='__pycache__/' \
    --exclude='*.pyc' --exclude='db.sqlite3' \
    $BACKEND_DIR/ $SERVER_USER@$SERVER_IP:$REMOTE_DIR/

echo "✅ Arquivos copiados com sucesso!"

echo "🔧 Configurando ambiente no servidor..."

# Executar comandos no servidor
ssh $SERVER_USER@$SERVER_IP << 'EOF'
cd /home/darley/teclado-esp-backend

echo "🐍 Criando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate

echo "📦 Instalando dependências..."
pip install -r requirements.txt

echo "🗄️ Executando migrações..."
python manage.py migrate

echo "🔧 Configurando ALLOWED_HOSTS..."
# Atualizar settings.py para incluir o IP do servidor
sed -i "s/ALLOWED_HOSTS = \['192.168.0.118', 'localhost', '127.0.0.1'\]/ALLOWED_HOSTS = ['10.102.0.108', '192.168.0.118', 'localhost', '127.0.0.1']/" core/settings.py

echo "🚀 Iniciando servidor Django..."
python manage.py runserver 0.0.0.0:8191
EOF

echo "🎉 Backend configurado e rodando em http://10.102.0.108:8191"
echo ""
echo "📋 Para acessar:"
echo "   - Backend: http://10.102.0.108:8191"
echo "   - API Status: http://10.102.0.108:8191/api/status/"
echo "   - Teste ESP32: http://10.102.0.108:8191/api/access/verify/"
echo ""
echo "⚠️  Lembre-se de atualizar o firmware do ESP32 com o novo IP!" 