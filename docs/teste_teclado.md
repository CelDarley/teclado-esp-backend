# Guia de Teste do Teclado Matricial

## Como Testar o Teclado

### 1. Teste Básico (keypad_test.ino)

Use o arquivo `firmware/keypad_test.ino` para testar apenas o teclado sem conexão com o servidor.

**Passos:**
1. Abra o Arduino IDE
2. Carregue o arquivo `firmware/keypad_test.ino`
3. Configure as bibliotecas necessárias:
   - Keypad (por Mark Stanley)
4. Configure o ESP32 como placa
5. Faça upload do código
6. Abra o Monitor Serial (115200 baud)

**O que você verá no console:**
```
=== TESTE DO TECLADO MATRICIAL ===
Pinos configurados:
Linhas: 19, 18, 5, 17
Colunas: 16, 4, 22
Layout do teclado:
Linha 0: 1 2 3
Linha 1: 4 5 6
Linha 2: 7 8 9
Linha 3: * 0 #
```

### 2. Teste Completo (keypad_access.ino)

Use o arquivo `firmware/keypad_access.ino` para testar com conexão ao servidor.

**Configuração necessária:**
1. Configure o WiFi no código:
   ```cpp
   const char* ssid = "SUA_REDE_WIFI";
   const char* password = "SUA_SENHA_WIFI";
   ```

2. Certifique-se de que o backend está rodando:
   ```bash
   cd backend
   python manage.py runserver
   ```

### 3. Conexões Físicas

**Teclado Matricial 4x3:**
```
Layout:
1 2 3
4 5 6
7 8 9
* 0 #
```

**Conexões ESP32:**
- **Linhas (Rows):** 19, 18, 5, 17
- **Colunas (Cols):** 16, 4, 22
- **LED:** Pino 2
- **Buzzer:** Pino 21
- **Relé:** Pino 23 (apenas no código completo)

### 4. O que Testar

#### Teste Individual das Teclas
1. Pressione cada tecla individualmente
2. Verifique se aparece no console:
   ```
   🔘 TECLA: '1'
   📍 Posição na matriz: Linha 0, Coluna 0
   ```

#### Teste de PIN
1. Digite um PIN de 4 dígitos (ex: 1234)
2. Pressione * para confirmar
3. Verifique se aparece:
   ```
   ✅ CONFIRMAÇÃO: PIN digitado: 1234
   📊 Comprimento do PIN: 4
   ```

#### Teste de Cancelamento
1. Digite alguns dígitos
2. Pressione # para cancelar
3. Verifique se aparece:
   ```
   ❌ CANCELADO: Entrada cancelada pelo usuário
   ```

#### Teste de Timeout
1. Digite alguns dígitos
2. Aguarde 10 segundos sem pressionar nada
3. Verifique se aparece:
   ```
   ⏰ TIMEOUT: PIN limpo automaticamente
   ```

### 5. Problemas Comuns

#### Tecla não responde
- Verifique as conexões físicas
- Confirme se os pinos estão corretos
- Teste com multímetro se há continuidade

#### Múltiplas teclas pressionadas
- Verifique se não há curto-circuito
- Confirme se as conexões estão isoladas

#### Tecla errada detectada
- Verifique a matriz de teclas no código
- Confirme se as linhas e colunas estão corretas

### 6. Debug Avançado

Para debug mais detalhado, adicione este código no `setup()`:

```cpp
void debugKeypad() {
  Serial.println("=== DEBUG DO TECLADO ===");
  
  // Testar cada linha
  for (int i = 0; i < ROWS; i++) {
    Serial.print("Testando linha ");
    Serial.println(i);
    digitalWrite(rowPins[i], LOW);
    
    for (int j = 0; j < COLS; j++) {
      if (digitalRead(colPins[j]) == LOW) {
        Serial.print("  Coluna ");
        Serial.print(j);
        Serial.println(" ativa");
      }
    }
    
    digitalWrite(rowPins[i], HIGH);
  }
}
```

### 7. PINs de Teste

- **Admin padrão:** 8729
- **Teste de erro:** 0000
- **Qualquer PIN de 4 dígitos**

### 8. Feedback Visual e Sonoro

- **LED pisca:** Tecla pressionada
- **LED verde (3x):** Sucesso
- **LED vermelho (5x):** Erro
- **Buzzer:** Confirmação sonora

### 9. Monitoramento em Tempo Real

Para monitorar continuamente, use este código:

```cpp
void monitorKeypad() {
  static unsigned long lastPrint = 0;
  
  if (millis() - lastPrint > 1000) {  // A cada 1 segundo
    Serial.print("Status: PIN=");
    Serial.print(currentPin);
    Serial.print(", WiFi=");
    Serial.println(WiFi.status() == WL_CONNECTED ? "OK" : "ERRO");
    lastPrint = millis();
  }
}
```

### 10. Checklist de Teste

- [ ] Todas as teclas respondem
- [ ] PIN é digitado corretamente
- [ ] Confirmação (*) funciona
- [ ] Cancelamento (#) funciona
- [ ] Timeout funciona
- [ ] LED pisca ao pressionar
- [ ] Buzzer funciona
- [ ] WiFi conecta (código completo)
- [ ] Comunicação com servidor (código completo) 