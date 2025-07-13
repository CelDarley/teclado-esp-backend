# Documentação do Hardware - Sistema de Controle de Acesso

## Componentes Necessários

### ESP32
- ESP32 DevKit ou similar
- Micro USB para programação
- Alimentação 3.3V

### Teclado Matricial 4x3
- 12 teclas organizadas em matriz
- Layout padrão: 1-9, *, 0, #
- Interface de 7 pinos (4 linhas + 3 colunas)

### Relé
- Relé de 5V para controle da fechadura
- Módulo relé com isolamento óptico
- Suporte a 10A/250VAC

### LED e Buzzer
- LED de status (qualquer cor)
- Buzzer piezoelétrico
- Resistores apropriados

## Esquema de Conexões

### Teclado Matricial
```
ESP32    Teclado
Pin 19 → Linha 1
Pin 18 → Linha 2  
Pin 5  → Linha 3
Pin 17 → Linha 4
Pin 16 → Coluna 1
Pin 4  → Coluna 2
Pin 22 → Coluna 3
```

### Relé
```
ESP32    Relé
Pin 23 → IN (controle)
3.3V   → VCC
GND    → GND
```

### LED e Buzzer
```
ESP32    LED
Pin 2  → Ânodo (+)
GND    → Cátodo (-) via resistor 220Ω

ESP32    Buzzer
Pin 21 → Terminal positivo
GND    → Terminal negativo
```

## Layout do Teclado

```
┌─────────┬─────────┬─────────┐
│    1    │    2    │    3    │
├─────────┼─────────┼─────────┤
│    4    │    5    │    6    │
├─────────┼─────────┼─────────┤
│    7    │    8    │    9    │
├─────────┼─────────┼─────────┤
│    *    │    0    │    #    │
└─────────┴─────────┴─────────┘
```

## Funcionamento

### Fluxo de Acesso
1. **Entrada do PIN**: Usuário digita 4 dígitos
2. **Confirmação**: Pressiona * para enviar
3. **Cancelamento**: Pressiona # para limpar
4. **Validação**: ESP32 envia PIN para servidor
5. **Resposta**: Servidor retorna autorização
6. **Ação**: Se autorizado, ativa relé por X segundos
7. **Feedback**: LED pisca e buzzer toca

### Estados do LED
- **Desligado**: Aguardando entrada
- **Pisca rápido**: Dígito digitado
- **3 piscadas lentas**: Acesso autorizado
- **5 piscadas rápidas**: Acesso negado
- **Aceso**: Sistema inicializando

### Estados do Buzzer
- **Tone 1000Hz, 500ms**: Acesso autorizado
- **Tone 200Hz, 1000ms**: Acesso negado

## Configuração WiFi

No firmware, altere as configurações:
```cpp
const char* ssid = "SUA_REDE_WIFI";
const char* password = "SUA_SENHA_WIFI";
const char* serverUrl = "http://SEU_IP:8000/api/access/";
```

## Teste de Funcionamento

### Teste do Teclado
1. Conecte o teclado
2. Upload do firmware
3. Abra o Serial Monitor (115200 baud)
4. Digite teclas e verifique saída

### Teste do Relé
1. Conecte multímetro ou lâmpada de teste
2. Digite PIN válido
3. Verifique ativação do relé
4. Confirme tempo de abertura

### Teste de Comunicação
1. Configure WiFi
2. Verifique IP no Serial Monitor
3. Teste acesso com PIN conhecido
4. Verifique logs no servidor

## Troubleshooting

### Teclado não responde
- Verifique conexões dos pinos
- Confirme mapeamento correto
- Teste continuidade dos fios

### Relé não ativa
- Verifique alimentação 5V
- Confirme conexão do pino 23
- Teste relé com multímetro

### WiFi não conecta
- Verifique credenciais
- Confirme força do sinal
- Teste com rede 2.4GHz

### Servidor não responde
- Verifique IP do servidor
- Confirme porta 8000
- Teste conectividade de rede

## Segurança Física

### Recomendações
- Use caixa resistente para ESP32
- Proteja conexões com silicone
- Instale em local seguro
- Use fonte de alimentação confiável

### Manutenção
- Verifique conexões periodicamente
- Limpe teclado regularmente
- Monitore logs de acesso
- Faça backup das configurações 