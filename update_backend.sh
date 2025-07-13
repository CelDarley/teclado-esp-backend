#!/bin/bash

echo "🔄 Atualizando arquivos do backend no servidor..."

# Configurações
SERVER_IP="10.102.0.108"
SERVER_USER="darley"
REMOTE_DIR="/home/darley/teclado-esp-backend"

# Copiar arquivos específicos
echo "📤 Copiando views.py..."
scp backend/api/views.py $SERVER_USER@$SERVER_IP:$REMOTE_DIR/api/

echo "📤 Copiando models.py..."
scp backend/api/models.py $SERVER_USER@$SERVER_IP:$REMOTE_DIR/api/

echo "📤 Copiando urls.py..."
scp backend/api/urls.py $SERVER_USER@$SERVER_IP:$REMOTE_DIR/api/

echo "📤 Copiando serializers.py..."
scp backend/api/serializers.py $SERVER_USER@$SERVER_IP:$REMOTE_DIR/api/

echo "✅ Arquivos atualizados!"
echo "🔄 Reiniciando backend no servidor..."

# Reiniciar o backend
ssh $SERVER_USER@$SERVER_IP "cd $REMOTE_DIR && pkill -f 'python.*manage.py' && nohup python manage.py runserver 0.0.0.0:8191 > server.log 2>&1 &"

echo "✅ Backend atualizado e reiniciado!"
echo "🌐 Acesse: http://$SERVER_IP:8191" 