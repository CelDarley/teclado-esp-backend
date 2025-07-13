# 🔐 Sistema de Controle de Acesso ESP32

Sistema completo de controle de acesso com ESP32, teclado matricial, backend Django e frontend Vue.js.

## 🏗️ Arquitetura

- **ESP32-WROOM**: Controla teclado matricial e relé
- **Backend Django**: API REST para verificação de PINs
- **Frontend Vue.js**: Interface web para gerenciamento
- **Teclado 4x3**: Entrada de PINs de acesso

## 📁 Estrutura do Projeto

```
teclado-esp/
├── backend/                 # Django API
│   ├── api/                # App principal
│   ├── core/               # Configurações
│   └── requirements.txt    # Dependências Python
├── frontend/               # Vue.js Interface
│   ├── src/               # Código fonte
│   └── package.json       # Dependências Node
├── firmware/              # Código ESP32
│   ├── sistema_final_integrado_novo_ip.ino
│   └── config.h           # Configurações
├── docs/                  # Documentação
└── scripts/               # Scripts de deploy
```

## 🔌 Conexões do Hardware

### Teclado 4x3 → ESP32-WROOM
```
Teclado Pino 1 → ESP32 Pino 25 (Linha 1)
Teclado Pino 2 → ESP32 Pino 26 (Linha 2)
Teclado Pino 3 → ESP32 Pino 27 (Linha 3)
Teclado Pino 4 → ESP32 Pino 14 (Linha 4)
Teclado Pino 5 → ESP32 Pino 12 (Coluna 1)
Teclado Pino 6 → ESP32 Pino 13 (Coluna 2)
Teclado Pino 7 → ESP32 Pino 15 (Coluna 3)
```

### Outros Componentes
```
LED Verde → ESP32 Pino 33
LED Vermelho → ESP32 Pino 21
Buzzer → ESP32 Pino 22
Relé → ESP32 Pino 32
```

## 🚀 Instalação e Configuração

### 1. Backend Django

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8191
```

### 2. Frontend Vue.js

```bash
cd frontend
npm install
npm run dev
```

### 3. Firmware ESP32

1. Abra o Arduino IDE
2. Instale as bibliotecas:
   - `WiFi` (incluída)
   - `HTTPClient` (incluída)
   - `ArduinoJson` (via Library Manager)
3. Configure o ESP32 como placa
4. Edite `firmware/config.h` com suas configurações WiFi
5. Faça upload do `firmware/sistema_final_integrado_novo_ip.ino`

## ⚙️ Configurações

### WiFi (firmware/config.h)
```cpp
#define WIFI_SSID "SUA_REDE_WIFI"
#define WIFI_PASSWORD "SUA_SENHA_WIFI"
```

### Backend (firmware/config.h)
```cpp
#define SERVER_URL "http://10.102.0.108:8191"
```

### Frontend (frontend/src/App.vue)
```javascript
const API_BASE_URL = 'http://10.102.0.108:8191/api'
```

## 🎯 Funcionalidades

### ESP32
- ✅ Detecção de teclas matriciais
- ✅ Entrada de PIN (4 dígitos)
- ✅ Conexão WiFi
- ✅ Comunicação com backend
- ✅ Controle de relé
- ✅ Feedback LED/buzzer
- ✅ Timeout automático

### Backend Django
- ✅ API REST para verificação de PINs
- ✅ Banco de dados SQLite
- ✅ Logs de acesso
- ✅ Gestão de usuários
- ✅ Configurações do sistema
- ✅ PIN admin configurável (8729)

### Frontend Vue.js
- ✅ Interface web responsiva
- ✅ Login administrativo
- ✅ Gestão de usuários
- ✅ Visualização de logs
- ✅ Configurações do sistema
- ✅ Dashboard em tempo real

## 🔍 Debug e Troubleshooting

### Serial Monitor ESP32
```
=== SISTEMA DE CONTROLE DE ACESSO ===
📡 Conectando ao WiFi: SUA_REDE_WIFI
✅ WiFi conectado! IP: 192.168.1.101
🔘 TECLA: '1'
📝 PIN ATUAL: 1
🌐 Enviando PIN para o backend...
🔓 Acesso concedido: SIM
🎉 ACESSO LIBERADO!
```

### Teste da API
```bash
curl -X POST http://10.102.0.108:8191/api/access/verify/ \
  -H "Content-Type: application/json" \
  -d '{"pin":"8729"}'
```

### Problemas Comuns

#### Teclado não funciona
- Verificar conexões dos pinos
- Confirmar mapeamento no firmware
- Testar com código simples primeiro

#### WiFi não conecta
- Verificar SSID e senha
- Confirmar rede 2.4GHz
- Verificar distância do roteador

#### Backend não responde
- Verificar se Django está rodando
- Confirmar IP no firmware
- Testar endpoint via curl

## 📊 PINs Padrão

- **Admin**: 8729 (configurável no frontend)
- **Usuários**: Criados via interface web

## 🛠️ Scripts Úteis

- `deploy_backend.sh`: Deploy do backend para servidor
- `deploy_frontend.sh`: Deploy do frontend para servidor
- `test_teclado.py`: Teste da API
- `monitor_esp32.sh`: Monitoramento do ESP32

## 📚 Documentação

- `docs/hardware.md`: Esquemas de conexão
- `docs/verificacao_teclado.md`: Troubleshooting do teclado
- `docs/teste_teclado.md`: Guia de testes

## 🎯 Próximos Passos

1. **Configurar rede WiFi** no firmware
2. **Ajustar IP do backend** no firmware
3. **Testar PIN admin** (8729)
4. **Criar usuários** via frontend
5. **Verificar logs** de acesso

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar Serial Monitor do ESP32
2. Consultar logs do backend Django
3. Verificar console do navegador (frontend)
4. Testar cada componente isoladamente

---

**🎉 Sistema desenvolvido com ESP32-WROOM, Django, Vue.js e teclado 4x3** 