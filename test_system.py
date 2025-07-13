#!/usr/bin/env python3
"""
Script de teste para o Sistema de Controle de Acesso
"""

import requests
import json
import time

# Configurações
BASE_URL = "http://localhost:8000/api"
ADMIN_PIN = "8729"

def test_api_connection():
    """Testa conexão com a API"""
    try:
        response = requests.get(f"{BASE_URL}/status/")
        if response.status_code == 200:
            print("✅ API conectada com sucesso!")
            return True
        else:
            print(f"❌ Erro na API: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar à API")
        print("   Verifique se o servidor Django está rodando em http://localhost:8000")
        return False

def test_admin_login():
    """Testa login do administrador"""
    try:
        data = {"pin": ADMIN_PIN}
        response = requests.post(f"{BASE_URL}/login/", json=data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ Login do administrador funcionando!")
                return True
            else:
                print(f"❌ Login falhou: {result.get('message')}")
                return False
        else:
            print(f"❌ Erro no login: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no teste de login: {e}")
        return False

def test_access_attempt():
    """Testa tentativa de acesso (simulando ESP32)"""
    try:
        data = {"pin": ADMIN_PIN}
        response = requests.post(f"{BASE_URL}/access/", json=data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ Tentativa de acesso funcionando!")
                print(f"   Duração da abertura: {result.get('duration')} segundos")
                return True
            else:
                print(f"❌ Acesso negado: {result.get('message')}")
                return False
        else:
            print(f"❌ Erro na tentativa de acesso: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no teste de acesso: {e}")
        return False

def test_user_creation():
    """Testa criação de usuário"""
    try:
        data = {
            "username": "teste",
            "first_name": "Usuário",
            "last_name": "Teste",
            "pin": "1234",
            "password": "senha123"
        }
        response = requests.post(f"{BASE_URL}/users/create/", json=data)
        
        if response.status_code == 201:
            print("✅ Criação de usuário funcionando!")
            return True
        else:
            print(f"❌ Erro na criação de usuário: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no teste de criação: {e}")
        return False

def test_logs():
    """Testa acesso aos logs"""
    try:
        response = requests.get(f"{BASE_URL}/logs/")
        
        if response.status_code == 200:
            logs = response.json()
            print(f"✅ Logs funcionando! ({len(logs)} registros)")
            return True
        else:
            print(f"❌ Erro ao acessar logs: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no teste de logs: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🔍 Testando Sistema de Controle de Acesso")
    print("=" * 50)
    
    tests = [
        ("Conexão com API", test_api_connection),
        ("Login do Administrador", test_admin_login),
        ("Tentativa de Acesso", test_access_attempt),
        ("Criação de Usuário", test_user_creation),
        ("Acesso aos Logs", test_logs),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testando: {test_name}")
        if test_func():
            passed += 1
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print(f"📊 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Sistema funcionando perfeitamente!")
        print("\n📋 Próximos passos:")
        print("1. Acesse http://localhost:5173")
        print("2. Digite o PIN: 8729")
        print("3. Configure usuários e parâmetros")
        print("4. Teste o hardware ESP32")
    else:
        print("⚠️  Alguns testes falharam. Verifique:")
        print("1. Servidor Django rodando em :8000")
        print("2. Migrações aplicadas")
        print("3. Configurações corretas")

if __name__ == "__main__":
    main() 