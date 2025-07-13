# Verificação do Teclado Matricial

## Problema: Teclado não responde

### 1. Verificar Biblioteca Keypad

No Arduino IDE:
1. Vá em **Sketch > Include Library > Manage Libraries**
2. Procure por "Keypad"
3. Instale a biblioteca "Keypad" por Mark Stanley
4. Versão recomendada: 3.1.1 ou superior

### 2. Verificar Conexões Físicas

**Teclado Matricial 4x3:**
```
Layout:
1 2 3
4 5 6
7 8 9
* 0 #
```

**Conexões ESP32:**
- **Linha 1:** Pino 19
- **Linha 2:** Pino 18
- **Linha 3:** Pino 5
- **Linha 4:** Pino 17
- **Coluna 1:** Pino 16
- **Coluna 2:** Pino 4
- **Coluna 3:** Pino 22

### 3. Teste de Continuidade

Use um multímetro para verificar:
1. **Modo continuidade** no multímetro
2. Teste cada conexão do teclado ao ESP32
3. Verifique se não há curto-circuito entre pinos

### 4. Teste com Multímetro

**Teste de resistência:**
- Pressione uma tecla
- Meça a resistência entre linha e coluna correspondente
- Deve ser próxima de 0Ω quando pressionada
- Deve ser infinita quando não pressionada

### 5. Problemas Comuns

#### A) Teclado não detectado
- Verifique se a biblioteca Keypad está instalada
- Confirme se os pinos estão corretos
- Teste com pinos diferentes

#### B) Teclas erradas detectadas
- Verifique a matriz de teclas no código
- Confirme se linhas e colunas estão invertidas

#### C) Múltiplas teclas pressionadas
- Verifique se não há curto-circuito
- Teste cada tecla individualmente

#### D) Nenhuma tecla responde
- Verifique alimentação do teclado
- Confirme conexões GND e VCC
- Teste com teclado diferente

### 6. Código de Teste Simples

```cpp
#include <Keypad.h>

const byte ROWS = 4;
const byte COLS = 3;

char keys[ROWS][COLS] = {
  {'1','2','3'},
  {'4','5','6'},
  {'7','8','9'},
  {'*','0','#'}
};

byte rowPins[ROWS] = {19, 18, 5, 17};
byte colPins[COLS] = {16, 4, 22};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

void setup() {
  Serial.begin(115200);
  Serial.println("Teste do teclado");
}

void loop() {
  char key = keypad.getKey();
  if (key) {
    Serial.print("Tecla: ");
    Serial.println(key);
  }
}
```

### 7. Verificação de Pinos

**Teste manual dos pinos:**
```cpp
void testPins() {
  for (int i = 0; i < ROWS; i++) {
    pinMode(rowPins[i], OUTPUT);
    digitalWrite(rowPins[i], LOW);
    
    for (int j = 0; j < COLS; j++) {
      pinMode(colPins[j], INPUT_PULLUP);
      if (digitalRead(colPins[j]) == LOW) {
        Serial.print("Linha ");
        Serial.print(i);
        Serial.print(" Coluna ");
        Serial.println(j);
      }
    }
    
    digitalWrite(rowPins[i], HIGH);
  }
}
```

### 8. Checklist de Verificação

- [ ] Biblioteca Keypad instalada
- [ ] Pinos corretos no código
- [ ] Conexões físicas corretas
- [ ] Alimentação do teclado (VCC e GND)
- [ ] Sem curto-circuito
- [ ] Teclado funcionando (teste com multímetro)
- [ ] ESP32 funcionando (LED pisca)
- [ ] Serial monitor aberto (115200 baud)

### 9. Teste Alternativo

Se o teclado não funcionar, teste com pinos diferentes:
```cpp
// Pinos alternativos
byte rowPins[ROWS] = {25, 26, 27, 14};  // Alternativa 1
byte colPins[COLS] = {12, 13, 15};       // Alternativa 1

// Ou
byte rowPins[ROWS] = {32, 33, 25, 26};   // Alternativa 2
byte colPins[COLS] = {27, 14, 12};       // Alternativa 2
```

### 10. Debug Avançado

Adicione este código para debug detalhado:
```cpp
void debugKeypad() {
  Serial.println("=== DEBUG DETALHADO ===");
  
  // Testar cada linha
  for (int i = 0; i < ROWS; i++) {
    Serial.print("Testando linha ");
    Serial.println(i);
    
    pinMode(rowPins[i], OUTPUT);
    digitalWrite(rowPins[i], LOW);
    delay(100);
    
    for (int j = 0; j < COLS; j++) {
      pinMode(colPins[j], INPUT_PULLUP);
      int val = digitalRead(colPins[j]);
      Serial.print("  Coluna ");
      Serial.print(j);
      Serial.print(": ");
      Serial.println(val);
    }
    
    digitalWrite(rowPins[i], HIGH);
    delay(100);
  }
}
``` 