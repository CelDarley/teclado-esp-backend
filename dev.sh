#!/bin/bash

# Script para desenvolvimento do Teclado ESP32
# Uso: ./dev.sh [backend|frontend|both]

case $1 in
    "backend")
        echo "🚀 Iniciando Backend Django..."
        cd backend
        source venv/bin/activate
        python manage.py runserver
        ;;
    "frontend")
        echo "🎨 Iniciando Frontend Vue..."
        cd frontend
        npm run dev
        ;;
    "both")
        echo "🚀 Iniciando Backend e Frontend..."
        # Inicia o backend em background
        cd backend
        source venv/bin/activate
        python manage.py runserver &
        BACKEND_PID=$!
        
        # Inicia o frontend
        cd ../frontend
        npm run dev &
        FRONTEND_PID=$!
        
        echo "✅ Backend rodando em: http://localhost:8000"
        echo "✅ Frontend rodando em: http://localhost:5173"
        echo "✅ API disponível em: http://localhost:8000/api/"
        echo ""
        echo "Pressione Ctrl+C para parar ambos os serviços"
        
        # Aguarda Ctrl+C
        trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
        wait
        ;;
    *)
        echo "🎹 Teclado ESP32 - Script de Desenvolvimento"
        echo ""
        echo "Uso: ./dev.sh [backend|frontend|both]"
        echo ""
        echo "Comandos:"
        echo "  backend  - Inicia apenas o backend Django"
        echo "  frontend - Inicia apenas o frontend Vue"
        echo "  both     - Inicia backend e frontend simultaneamente"
        echo ""
        echo "Endpoints disponíveis:"
        echo "  - Backend: http://localhost:8000"
        echo "  - Frontend: http://localhost:5173"
        echo "  - API Test: http://localhost:8000/api/test/"
        echo "  - Keyboard Status: http://localhost:8000/api/keyboard/status/"
        ;;
esac 