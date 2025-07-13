# 🚀 Guia de Deploy - Backend para Servidor 10.102.0.10

## 📋 **Resumo**
- **Servidor:** 10.102.0.10
- **Porta:** 8000
- **URL:** http://10.102.0.10:8000
- **API:** http://10.102.0.10:8000/api/

---

## 🔧 **1. Deploy Automático (Recomendado)**

### Execute o script de deploy:
```bash
./deploy_backend.sh
```

**O que o script faz:**
- ✅ Copia arquivos para o servidor
- ✅ Cria ambiente virtual Python
- ✅ Instala dependências
- ✅ Executa migrações
- ✅ Configura ALLOWED_HOSTS
- ✅ Inicia o servidor Django

---

## 🔧 **2. Deploy Manual**

### **2.1. No servidor 10.102.0.10:**

```bash
# Conectar ao servidor
ssh darley@10.102.0.10

# Criar diretório
mkdir -p /home/darley/teclado-esp-backend
cd /home/darley/teclado-esp-backend

# Copiar arquivos (do seu computador atual)
# Use rsync ou scp para copiar os arquivos
```

### **2.2. Configurar ambiente Python:**

```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar migrações
python manage.py migrate
```

### **2.3. Configurar Django:**

```bash
# Editar settings.py
nano core/settings.py

# Adicionar o IP do servidor em ALLOWED_HOSTS:
ALLOWED_HOSTS = ['10.102.0.10', '192.168.0.118', 'localhost', '127.0.0.1']
```

### **2.4. Iniciar servidor:**

```bash
# Iniciar Django
python manage.py runserver 0.0.0.0:8000
```

---

## 🔧 **3. Atualizar Firmware ESP32**

### **3.1. Editar configurações no firmware:**

Abra o arquivo `firmware/sistema_final_integrado_novo_ip.ino` e ajuste:

```cpp
// Configurar WiFi
const char* WIFI_SSID = "SUA_REDE_WIFI";
const char* WIFI_PASSWORD = "SUA_SENHA_WIFI";

// IP do servidor já está configurado
#define SERVER_URL "http://10.102.0.10:8000"
```

### **3.2. Fazer upload para ESP32:**

1. Abra a Arduino IDE
2. Abra o arquivo `sistema_final_integrado_novo_ip.ino`
3. Configure a placa: **ESP32 Dev Module**
4. Faça upload

---

## 🧪 **4. Testes**

### **4.1. Testar Backend:**

```bash
# Testar se está rodando
curl http://10.102.0.10:8000/api/status/

# Testar verificação de acesso
curl -X POST http://10.102.0.10:8000/api/access/verify/ \
  -H "Content-Type: application/json" \
  -d '{"pin":"8729"}'
```

### **4.2. Testar ESP32:**

1. Conecte o ESP32 via USB
2. Abra o Monitor Serial (115200 baud)
3. Digite **8729** no teclado físico
4. Pressione **'*'** para confirmar
5. Verifique se recebe resposta de sucesso

---

## 📊 **5. URLs Importantes**

- **Backend:** http://10.102.0.10:8000
- **API Status:** http://10.102.0.10:8000/api/status/
- **Verificar Acesso:** http://10.102.0.10:8000/api/access/verify/
- **Frontend:** http://localhost:5173 (ainda no seu computador)

---

## 🔧 **6. Troubleshooting**

### **Problema: Servidor não responde**
```bash
# Verificar se está rodando
ps aux | grep python

# Verificar porta
netstat -tlnp | grep 8000
```

### **Problema: ESP32 não conecta**
- Verifique se o WiFi está correto
- Verifique se o IP do servidor está acessível
- Teste: `ping 10.102.0.10`

### **Problema: Acesso negado**
- Verifique se o PIN está correto (8729 para admin)
- Verifique logs do Django no servidor

---

## 📝 **7. Logs e Monitoramento**

### **Ver logs do Django:**
```bash
# No servidor 10.102.0.10
tail -f /home/darley/teclado-esp-backend/django.log
```

### **Monitorar ESP32:**
```bash
# No seu computador
./monitor_esp32.sh
```

---

## ✅ **8. Checklist Final**

- [ ] Backend rodando em http://10.102.0.10:8000
- [ ] API respondendo corretamente
- [ ] ESP32 conectado ao WiFi
- [ ] Firmware atualizado com novo IP
- [ ] Teclado funcionando
- [ ] Relé acionando corretamente
- [ ] LEDs e buzzer funcionando

---

**🎉 Sistema pronto para uso!** 