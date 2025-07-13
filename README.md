# Sistema de Controle de Acesso ESP32

Sistema completo de controle de acesso com teclado 4x3, ESP32-WROOM, backend Django e frontend Vue.js.

## 🏗️ Arquitetura do Sistema

```
┌─────────────────┐    WiFi    ┌─────────────────┐    HTTP    ┌─────────────────┐
│   ESP32-WROOM   │ ────────── │  Backend Django │ ────────── │  Frontend Vue   │
│                 │             │                 │             │                 │
│ • Teclado 4x3   │             │ • API REST      │             │ • Interface Web │
│ • LED + Buzzer  │             │ • Banco SQLite  │             │ • Gestão Users  │
│ • Relé Fechadura│             │ • Logs Acesso   │             │ • Logs + Config │
└─────────────────┘             └─────────────────┘             └─────────────────┘
```

## 📋 Componentes

### Hardware
- **ESP32-WROOM** - Microcontrolador principal
- **Teclado 4x3** - Entrada de PINs
- **LED** - Feedback visual
- **Buzzer** - Feedback sonoro
- **Relé** - Controle da fechadura magnética

### Software
- **Backend Django** - API REST, banco de dados, logs
- **Frontend Vue.js** - Interface web para administração
- **Firmware ESP32** - Controle do hardware

## 🔧 Configuração

### 1. Backend Django

```bash
# Instalar dependências
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

pip install -r requirements.txt

# Configurar banco
python manage.py migrate

# Criar superusuário (opcional)
python manage.py createsuperuser

# Rodar servidor
python manage.py runserver 0.0.0.0:8000
```

### 2. Frontend Vue.js

```bash
# Instalar dependências
cd frontend
npm install

# Rodar servidor de desenvolvimento
npm run dev
```

### 3. Firmware ESP32

#### Configuração do Arduino IDE
1. Instalar ESP32 board package
2. Selecionar board: "ESP32 Dev Module"
3. Configurar porta serial

#### Bibliotecas Necessárias
- `WiFi` (incluída)
- `HTTPClient` (incluída)
- `ArduinoJson` (instalar via Library Manager)
- `Keypad` (instalar via Library Manager)

#### Configuração do Sistema
Editar `firmware/config.h`:

```cpp
// WiFi
#define WIFI_SSID "SUA_REDE_WIFI"
#define WIFI_PASSWORD "SUA_SENHA_WIFI"

// Backend
#define SERVER_URL "http://192.168.1.100:8000"  // IP do seu backend

// Pinos do teclado (confirmados funcionando)
#define ROW_PINS {25, 26, 27, 14}  // Linhas
#define COL_PINS {12, 13, 15}       // Colunas
```

## 🔌 Conexões do Hardware

### Teclado 4x3 → ESP32
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
LED → ESP32 Pino 2
Buzzer → ESP32 Pino 21
Relé → ESP32 Pino 22
```

## 🚀 Como Usar

### 1. Inicialização
1. Conectar hardware conforme diagrama
2. Configurar WiFi no `config.h`
3. Fazer upload do firmware `sistema_final.ino`
4. Rodar backend Django
5. Rodar frontend Vue.js

### 2. Teste do Sistema
1. **Digite um PIN** no teclado (ex: 1234)
2. **Pressione *** para confirmar
3. **Aguarde resposta** do backend
4. **Veja feedback** no LED e buzzer
5. **Acesse liberado** se PIN correto

### 3. PINs Padrão
- **Admin**: 8729 (configurável no frontend)
- **Usuários**: Criados via interface web

## 📊 Funcionalidades

### ESP32
- ✅ Detecção de teclas
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
- ✅ PIN admin configurável

### Frontend Vue.js
- ✅ Interface web responsiva
- ✅ Login administrativo
- ✅ Gestão de usuários
- ✅ Visualização de logs
- ✅ Configurações do sistema
- ✅ Dashboard em tempo real

## 🔍 Debug e Troubleshooting

### Serial Monitor
O ESP32 envia informações detalhadas via Serial:
```
=== SISTEMA DE CONTROLE DE ACESSO FINAL ===
📡 Conectando ao WiFi: SUA_REDE_WIFI
✅ WiFi conectado! IP: 192.168.1.101
🔘 TECLA: '1'
📝 PIN ATUAL: 1
🌐 Enviando PIN para o backend...
🔓 Acesso concedido: SIM
🎉 ACESSO LIBERADO!
```

### Problemas Comuns

#### Teclado não funciona
- Verificar conexões dos pinos
- Confirmar mapeamento no `config.h`
- Testar com código simples primeiro

#### WiFi não conecta
- Verificar SSID e senha
- Confirmar rede 2.4GHz
- Verificar distância do roteador

#### Backend não responde
- Verificar se Django está rodando
- Confirmar IP no `config.h`
- Testar endpoint via curl:
```bash
curl -X POST http://localhost:8000/api/access/verify/ \
  -H "Content-Type: application/json" \
  -d '{"pin":"8729"}'
```

## 📁 Estrutura do Projeto

```
teclado-esp/
├── backend/                 # Django API
│   ├── api/                # App principal
│   ├── core/               # Configurações
│   ├── manage.py           # Script Django
│   └── requirements.txt    # Dependências Python
├── frontend/               # Vue.js Interface
│   ├── src/               # Código fonte
│   ├── package.json       # Dependências Node
│   └── vite.config.js     # Config Vite
└── firmware/              # Código ESP32
    ├── sistema_final.ino  # Código principal
    ├── config.h           # Configurações
    └── *.ino             # Códigos de teste
```

## 🎯 Próximos Passos

1. **Testar sistema completo** com hardware real
2. **Configurar rede WiFi** correta
3. **Ajustar IP do backend** no `config.h`
4. **Testar PIN admin** (8729)
5. **Criar usuários** via frontend
6. **Verificar logs** de acesso

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar Serial Monitor do ESP32
2. Consultar logs do backend Django
3. Verificar console do navegador (frontend)
4. Testar cada componente isoladamente

---

**Sistema desenvolvido com ESP32-WROOM, Django, Vue.js e teclado 4x3** 