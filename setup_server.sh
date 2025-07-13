#!/bin/bash

echo "🚀 Configurando servidor 10.102.0.10 para o backend Django"
echo "=========================================================="

# Conectar ao servidor e executar comandos
ssh darley@10.102.0.10 << 'EOF'

echo "📦 Instalando dependências do sistema..."
sudo apt update
sudo apt install -y python3-pip python3-venv

echo "🐍 Configurando ambiente Python..."
cd /home/darley/teclado-esp-backend

# Remover venv antigo se existir
rm -rf venv

# Criar novo ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

echo "📦 Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🗄️ Executando migrações..."
python manage.py migrate

echo "🔧 Configurando ALLOWED_HOSTS..."
# Atualizar settings.py para incluir o IP do servidor
sed -i "s/ALLOWED_HOSTS = \['192.168.0.118', 'localhost', '127.0.0.1'\]/ALLOWED_HOSTS = ['10.102.0.10', '192.168.0.118', 'localhost', '127.0.0.1']/" core/settings.py

echo "🚀 Iniciando servidor Django..."
echo "📊 Backend rodando em: http://10.102.0.10:8000"
echo "📊 API Status: http://10.102.0.10:8000/api/status/"
echo "📊 Teste ESP32: http://10.102.0.10:8000/api/access/verify/"

# Iniciar Django
python manage.py runserver 0.0.0.0:8000

EOF

echo "✅ Configuração concluída!"
echo ""
echo "📋 URLs importantes:"
echo "   - Backend: http://10.102.0.10:8000"
echo "   - API Status: http://10.102.0.10:8000/api/status/"
echo "   - Teste ESP32: http://10.102.0.10:8000/api/access/verify/"
echo ""
echo "⚠️  Lembre-se de atualizar o firmware do ESP32 com o novo IP!" 