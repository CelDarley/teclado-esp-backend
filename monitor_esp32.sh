#!/bin/bash

echo "🔍 Monitorando ESP32..."
echo "📱 Digite o PIN admin (8729) no teclado físico"
echo "🔘 Pressione '*' para confirmar"
echo "📊 Aguardando dados do ESP32..."
echo "---"

# Monitorar o serial do ESP32
cat /dev/ttyACM0 