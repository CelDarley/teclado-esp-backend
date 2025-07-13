#!/usr/bin/env python3
"""
Script para testar a API do sistema de controle de acesso
Simula o que o ESP32 faria ao enviar PINs para o servidor
"""

import requests
import json
import time

# Configurações
BASE_URL = "http://localhost:8000/api"
ADMIN_PIN = "8729"

def test_api_connection():
    """Testa se a API está respondendo"""
    try:
        response = requests.get(f"{BASE_URL}/status/")
        if response.status_code == 200:
            print("✅ API está respondendo")
            return True
        else:
            print(f"❌ API retornou status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar à API")
        print("   Certifique-se de que o backend está rodando:")
        print("   cd backend && python manage.py runserver")
        return False

def test_pin_validation(pin):
    """Testa a validação de um PIN"""
    print(f"\n🔐 Testando PIN: {pin}")
    
    data = {"pin": pin}
    
    try:
        response = requests.post(f"{BASE_URL}/access/", json=data)
        
        print(f"📤 Enviado: {json.dumps(data)}")
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📋 Resposta: {json.dumps(result, indent=2)}")
            
            if result.get("success"):
                print("✅ ACESSO AUTORIZADO!")
                duration = result.get("duration", 5)
                print(f"⏱️  Porta ficará aberta por {duration} segundos")
            else:
                print("❌ ACESSO NEGADO!")
                print(f"💬 Mensagem: {result.get('message', 'N/A')}")
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"📋 Resposta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")

def test_user_creation():
    """Testa a criação de um usuário"""
    print(f"\n👤 Testando criação de usuário")
    
    data = {
        "name": "Usuário Teste",
        "pin": "1234",
        "is_active": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/create/", json=data)
        
        print(f"📤 Enviado: {json.dumps(data)}")
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"📋 Resposta: {json.dumps(result, indent=2)}")
            print("✅ Usuário criado com sucesso!")
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"📋 Resposta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")

def test_users_list():
    """Testa a listagem de usuários"""
    print(f"\n📋 Testando listagem de usuários")
    
    try:
        response = requests.get(f"{BASE_URL}/users/")
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📋 Usuários encontrados: {len(result)}")
            for user in result:
                print(f"   - {user['name']} (PIN: {user['pin']}, Ativo: {user['is_active']})")
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"📋 Resposta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")

def test_logs():
    """Testa a listagem de logs"""
    print(f"\n📊 Testando listagem de logs")
    
    try:
        response = requests.get(f"{BASE_URL}/logs/")
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📋 Logs encontrados: {len(result)}")
            for log in result[:5]:  # Mostra apenas os 5 primeiros
                print(f"   - {log['timestamp']}: {log['pin']} -> {log['success']}")
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"📋 Resposta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")

def simulate_esp32_behavior():
    """Simula o comportamento do ESP32"""
    print("\n🤖 SIMULANDO COMPORTAMENTO DO ESP32")
    print("=" * 50)
    
    # PINs para testar
    test_pins = [
        "8729",  # Admin (deve funcionar)
        "1234",  # Usuário normal (se existir)
        "0000",  # PIN inválido
        "9999",  # PIN inválido
        "123",   # PIN muito curto
        "12345", # PIN muito longo
    ]
    
    for pin in test_pins:
        test_pin_validation(pin)
        time.sleep(1)  # Pausa entre testes

def main():
    """Função principal"""
    print("🔐 TESTE DO SISTEMA DE CONTROLE DE ACESSO")
    print("=" * 50)
    
    # Teste de conexão
    if not test_api_connection():
        return
    
    # Testes básicos
    test_users_list()
    test_logs()
    
    # Teste de criação de usuário
    test_user_creation()
    
    # Simulação do ESP32
    simulate_esp32_behavior()
    
    print("\n" + "=" * 50)
    print("✅ TESTE CONCLUÍDO!")
    print("\n📝 PRÓXIMOS PASSOS:")
    print("1. Configure o WiFi no firmware")
    print("2. Faça upload do código para o ESP32")
    print("3. Conecte o teclado matricial")
    print("4. Teste com o hardware real")

if __name__ == "__main__":
    main() 