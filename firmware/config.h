// Configurações do Sistema de Controle de Acesso
// ESP32 + Teclado + WiFi + Backend Django

// ========================================
// CONFIGURAÇÕES WIFI
// ========================================
#define WIFI_SSID "catena"
#define WIFI_PASSWORD "Lolina2501"

// ========================================
// CONFIGURAÇÕES DO BACKEND
// ========================================
#define SERVER_URL "http://192.168.1.100:8000"  // Ajuste para o IP do seu backend
#define API_ENDPOINT "/api/access/verify/"

// ========================================
// CONFIGURAÇÕES DO TECLADO
// ========================================
// Pinos do ESP32 (baseado no seu mapeamento que funcionou)
#define ROW_PINS {25, 26, 27, 14}  // Linhas do ESP32
#define COL_PINS {12, 13, 15}       // Colunas do ESP32

// ========================================
// CONFIGURAÇÕES DE CONTROLE
// ========================================
#define LED_PIN 2       // LED de status
#define BUZZER_PIN 21   // Buzzer para feedback
#define RELAY_PIN 22    // Relé da fechadura

// ========================================
// CONFIGURAÇÕES DE TIMEOUT
// ========================================
#define KEY_TIMEOUT 10000        // 10 segundos para timeout do PIN
#define DOOR_OPEN_TIME 3000      // 3 segundos para manter porta aberta
#define WIFI_CHECK_INTERVAL 30000 // 30 segundos para verificar WiFi

// ========================================
// CONFIGURAÇÕES DE DEBUG
// ========================================
#define DEBUG_SERIAL true        // Habilitar debug no Serial
#define DEBUG_WIFI true          // Habilitar debug do WiFi
#define DEBUG_KEYPAD true        // Habilitar debug do teclado
#define DEBUG_BACKEND true       // Habilitar debug do backend 