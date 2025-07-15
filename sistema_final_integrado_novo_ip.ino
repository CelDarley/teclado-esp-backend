// ========================================
// SISTEMA DE CONTROLE DE ACESSO - ESP32
// ========================================
// Versão atualizada para servidor 10.102.0.108
// 
// MAPEAMENTO DE PINOS PARA ESP32-WROOM:
// ========================================
// TECLADO -> ESP32 (mapeamento correto):
// Linhas: 22, 21, 32, 17 (Pinos 7,6,5,4)
// Colunas: 25, 26, 27 (Pinos 3,2,1)
// ========================================

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// ========================================
// CONFIGURAÇÕES DO BACKEND
// ========================================
#define SERVER_URL "http://10.102.0.108:8191"  // NOVO IP DO SERVIDOR
#define API_ENDPOINT "/api/access/verify/"

// ========================================
// CONFIGURAÇÕES DO TECLADO
// ========================================
// Mapeamento correto baseado no teste físico
// Pinos do teclado -> Pinos do ESP32
const int PINOS_LINHAS[] = {22, 21, 32, 17};  // Linhas: Pino 7,6,5,4 -> GPIO 22,21,32,17
const int PINOS_COLUNAS[] = {25, 26, 27};      // Colunas: Pino 3,2,1 -> GPIO 25,26,27

char teclas[4][3] = {
  {'1','2','3'},  // Linha 1 (Pino 7)
  {'4','5','6'},  // Linha 2 (Pino 6)
  {'7','8','9'},  // Linha 3 (Pino 5)
  {'*','0','#'}   // Linha 4 (Pino 4)
};

// ========================================
// CONFIGURAÇÕES DO SISTEMA
// ========================================
#define PIN_RELE 18        // Pino do relé (mudado para não conflitar com GPIO 14)
#define PIN_LED_VERDE 12   // LED verde (mudado para não conflitar)
#define PIN_LED_VERMELHO 13 // LED vermelho (mudado para não conflitar)
#define PIN_BUZZER 15      // Buzzer (mudado para não conflitar)

// ========================================
// CONFIGURAÇÕES DO WIFI
// ========================================
const char* WIFI_SSID = "catena";      // Sua rede WiFi
const char* WIFI_PASSWORD = "Lolina2501";  // Sua senha WiFi

// ========================================
// VARIÁVEIS GLOBAIS
// ========================================
String pinDigitado = "";
bool aguardandoConfirmacao = false;
unsigned long ultimaTecla = 0;
const unsigned long DEBOUNCE_TIME = 200;
bool debugTeclado = false;   // Debug reduzido - apenas teclas detectadas

// ========================================
// SETUP
// ========================================
void setup() {
  Serial.begin(115200);
  delay(2000);
  
  Serial.println("\n\n=== SISTEMA DE CONTROLE DE ACESSO ===");
  Serial.println("Servidor: " + String(SERVER_URL));
  Serial.println("=======================================");
  
  // Configurar pinos
  configurarPinos();
  
  // Conectar WiFi
  conectarWiFi();
  
  Serial.println("🎯 SISTEMA PRONTO!");
  Serial.println("🎯 Digite o PIN e pressione '*' para confirmar");
  Serial.println("🎯 Pressione '#' para cancelar");
  Serial.println("---");
  
  Serial.println("✅ Sistema configurado com mapeamento correto!");
  Serial.println("🔧 Pronto para testar o teclado!");
}

// ========================================
// LOOP PRINCIPAL
// ========================================
void loop() {
  // Ler teclado
  char tecla = lerTeclado();
  
  if (tecla != 0) {
    processarTecla(tecla);
  }
  
  // Verificar conexão WiFi periodicamente
  static unsigned long lastWiFiCheck = 0;
  if (millis() - lastWiFiCheck > 30000) { // A cada 30 segundos
    if (WiFi.status() != WL_CONNECTED) {
      Serial.println("⚠️ Reconectando WiFi...");
      conectarWiFi();
    }
    lastWiFiCheck = millis();
  }
}

// ========================================
// CONFIGURAÇÃO DOS PINOS
// ========================================
void configurarPinos() {
  Serial.println("🔧 Configurando pinos...");
  
  // Configurar pinos das linhas
  for (int i = 0; i < 4; i++) {
    pinMode(PINOS_LINHAS[i], OUTPUT);
    digitalWrite(PINOS_LINHAS[i], HIGH);
    Serial.println("Linha " + String(i) + " (GPIO " + String(PINOS_LINHAS[i]) + ") configurada como OUTPUT");
  }
  
  // Configurar pinos das colunas
  for (int i = 0; i < 3; i++) {
    pinMode(PINOS_COLUNAS[i], INPUT_PULLUP);
    Serial.println("Coluna " + String(i) + " (GPIO " + String(PINOS_COLUNAS[i]) + ") configurada como INPUT_PULLUP");
  }
  
  // Configurar pinos do sistema
  pinMode(PIN_RELE, OUTPUT);
  pinMode(PIN_LED_VERDE, OUTPUT);
  pinMode(PIN_LED_VERMELHO, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  
  // Estado inicial
  digitalWrite(PIN_RELE, LOW);
  digitalWrite(PIN_LED_VERDE, LOW);
  digitalWrite(PIN_LED_VERMELHO, LOW);
  digitalWrite(PIN_BUZZER, LOW);
  
  Serial.println("✅ Configuração de pinos concluída!");
}

// ========================================
// CONEXÃO WIFI
// ========================================
void conectarWiFi() {
  Serial.print("📡 Conectando ao WiFi: ");
  Serial.println(WIFI_SSID);
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  int tentativas = 0;
  while (WiFi.status() != WL_CONNECTED && tentativas < 20) {
    delay(500);
    Serial.print(".");
    tentativas++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println();
    Serial.println("✅ WiFi conectado!");
    Serial.print("📱 IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println();
    Serial.println("❌ Falha na conexão WiFi");
  }
}

// ========================================
// LEITURA DO TECLADO
// ========================================
char lerTeclado() {
  // Debounce
  if (millis() - ultimaTecla < DEBOUNCE_TIME) {
    return 0;
  }
  

  
  // Testar cada linha
  for (int linha = 0; linha < 4; linha++) {
    // Ativar linha atual
    digitalWrite(PINOS_LINHAS[linha], LOW);
    delay(10);
    
    // Verificar colunas
    for (int coluna = 0; coluna < 3; coluna++) {
      int estadoColuna = digitalRead(PINOS_COLUNAS[coluna]);
      
      if (estadoColuna == LOW) {
        char tecla = teclas[linha][coluna];
        
        // Aguardar soltar a tecla
        while (digitalRead(PINOS_COLUNAS[coluna]) == LOW) {
          delay(10);
        }
        
        // Desativar linha atual
        digitalWrite(PINOS_LINHAS[linha], HIGH);
        
        ultimaTecla = millis();
        return tecla;
      }
    }
    
    // Desativar linha atual
    digitalWrite(PINOS_LINHAS[linha], HIGH);
  }
  
  return 0;
}

// ========================================
// PROCESSAMENTO DE TECLAS
// ========================================
void processarTecla(char tecla) {
  Serial.print("🔘 TECLA: '");
  Serial.print(tecla);
  Serial.println("'");
  
  if (tecla == '*') {  // '*' para confirmar
    // Confirmar PIN
    if (pinDigitado.length() > 0) {
      Serial.println("✅ CONFIRMAÇÃO: PIN digitado: " + pinDigitado);
      Serial.println("📊 Comprimento: " + String(pinDigitado.length()));
      
      if (pinDigitado.length() == 4) {
        verificarAcesso(pinDigitado);
      } else {
        Serial.println("❌ PIN deve ter 4 dígitos");
        feedbackErro();
      }
      
      pinDigitado = "";
    } else {
      Serial.println("❌ Nenhum PIN digitado");
      feedbackErro();
    }
  } else if (tecla == '#') {  // '#' para cancelar
    // Cancelar
    Serial.println("❌ CANCELADO");
    pinDigitado = "";
    feedbackErro();
  } else if (tecla >= '0' && tecla <= '9') {
    // Adicionar dígito
    if (pinDigitado.length() < 4) {
      pinDigitado += tecla;
      Serial.println("📝 PIN: " + pinDigitado);
    } else {
      Serial.println("❌ PIN muito longo");
      feedbackErro();
    }
  }
}

// ========================================
// VERIFICAÇÃO DE ACESSO
// ========================================
void verificarAcesso(String pin) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("❌ Sem conexão WiFi");
    feedbackErro();
    return;
  }
  
  Serial.println("🌐 Enviando PIN para o backend...");
  Serial.println("📡 URL: " + String(SERVER_URL) + API_ENDPOINT);
  
  HTTPClient http;
  http.begin(String(SERVER_URL) + API_ENDPOINT);
  http.addHeader("Content-Type", "application/json");
  
  // Criar JSON
  String jsonPayload = "{\"pin\":\"" + pin + "\"}";
  Serial.println("📤 Payload: " + jsonPayload);
  
  int httpCode = http.POST(jsonPayload);
  Serial.println("📥 Código de resposta: " + String(httpCode));
  
  if (httpCode > 0) {
    String response = http.getString();
    Serial.println("📥 Resposta: " + response);
    
    // Parse JSON
    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, response);
    
    if (!error) {
      bool success = doc["success"];
      
      if (success) {
        Serial.println("✅ SUCESSO: Acesso autorizado");
        feedbackSucesso();
        acionarRele();
      } else {
        Serial.println("❌ ACESSO NEGADO");
        feedbackErro();
      }
    } else {
      Serial.println("❌ ERRO: Falha ao processar resposta JSON");
      feedbackErro();
    }
  } else {
    Serial.println("❌ ERRO: Falha na requisição HTTP");
    feedbackErro();
  }
  
  http.end();
}

// ========================================
// FEEDBACK VISUAL E SONORO
// ========================================
void feedbackSucesso() {
  Serial.println("🟢 FEEDBACK: Sucesso (LED verde + buzzer)");
  
  // LED verde
  digitalWrite(PIN_LED_VERDE, HIGH);
  
  // Buzzer (frequência alta)
  tone(PIN_BUZZER, 2000);
  delay(500);
  noTone(PIN_BUZZER);
  
  // Desligar LED
  delay(1000);
  digitalWrite(PIN_LED_VERDE, LOW);
}

void feedbackErro() {
  Serial.println("🔴 FEEDBACK: Erro (LED vermelho + buzzer)");
  
  // LED vermelho
  digitalWrite(PIN_LED_VERMELHO, HIGH);
  
  // Buzzer (frequência baixa)
  tone(PIN_BUZZER, 500);
  delay(1000);
  noTone(PIN_BUZZER);
  
  // Desligar LED
  delay(1000);
  digitalWrite(PIN_LED_VERMELHO, LOW);
}

// ========================================
// CONTROLE DO RELÉ
// ========================================
void acionarRele() {
  Serial.println("🔓 RELÉ: Porta aberta por 5 segundos");
  
  digitalWrite(PIN_RELE, HIGH);
  delay(5000);  // 5 segundos
  digitalWrite(PIN_RELE, LOW);
  
  Serial.println("🔒 RELÉ: Porta fechada");
} 