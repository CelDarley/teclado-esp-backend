<template>
  <div id="app">
    <header class="header">
      <h1>🎹 Teclado ESP32</h1>
      <p>Controle e Configuração</p>
    </header>

    <main class="main">
      <div class="status-card">
        <h2>Status da Conexão</h2>
        <div class="status-indicator" :class="{ connected: isConnected }">
          {{ isConnected ? '🟢 Conectado' : '🔴 Desconectado' }}
        </div>
        <button @click="testConnection" class="test-btn">
          Testar Conexão
        </button>
      </div>

      <div class="keyboard-status" v-if="keyboardData">
        <h2>Status do Teclado</h2>
        <div class="status-grid">
          <div class="status-item">
            <span class="label">Dispositivo:</span>
            <span class="value">{{ keyboardData.device }}</span>
          </div>
          <div class="status-item">
            <span class="label">Bateria:</span>
            <span class="value">{{ keyboardData.battery }}%</span>
          </div>
          <div class="status-item">
            <span class="label">RGB:</span>
            <span class="value">{{ keyboardData.rgb_enabled ? 'Ativado' : 'Desativado' }}</span>
          </div>
          <div class="status-item">
            <span class="label">Perfil:</span>
            <span class="value">{{ keyboardData.current_profile }}</span>
          </div>
        </div>
      </div>

      <div class="message" v-if="message">
        <div class="message-content" :class="messageType">
          {{ message }}
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const isConnected = ref(false)
const keyboardData = ref(null)
const message = ref('')
const messageType = ref('info')

const API_BASE_URL = 'http://localhost:8000/api'

const showMessage = (msg: string, type: 'success' | 'error' | 'info' = 'info') => {
  message.value = msg
  messageType.value = type
  setTimeout(() => {
    message.value = ''
  }, 5000)
}

const testConnection = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/test/`)
    const data = await response.json()
    
    if (response.ok) {
      isConnected.value = true
      showMessage('✅ ' + data.message, 'success')
    } else {
      isConnected.value = false
      showMessage('❌ Erro na conexão', 'error')
    }
  } catch (error) {
    isConnected.value = false
    showMessage('❌ Erro de conexão com o servidor', 'error')
    console.error('Erro:', error)
  }
}

const getKeyboardStatus = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/keyboard/status/`)
    const data = await response.json()
    
    if (response.ok) {
      keyboardData.value = data
    }
  } catch (error) {
    console.error('Erro ao obter status do teclado:', error)
  }
}

onMounted(() => {
  testConnection()
  getKeyboardStatus()
})
</script>

<style scoped>
#app {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header {
  text-align: center;
  padding: 2rem 0;
  color: white;
}

.header h1 {
  margin: 0;
  font-size: 2.5rem;
  font-weight: 300;
}

.header p {
  margin: 0.5rem 0 0 0;
  font-size: 1.1rem;
  opacity: 0.9;
}

.main {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 2rem;
}

.status-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.status-card h2 {
  margin: 0 0 1rem 0;
  color: #333;
  font-size: 1.5rem;
}

.status-indicator {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  background: #f8f9fa;
  border: 2px solid #e9ecef;
}

.status-indicator.connected {
  background: #d4edda;
  border-color: #c3e6cb;
  color: #155724;
}

.test-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.test-btn:hover {
  background: #0056b3;
}

.keyboard-status {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.keyboard-status h2 {
  margin: 0 0 1.5rem 0;
  color: #333;
  font-size: 1.5rem;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.label {
  font-weight: 600;
  color: #495057;
}

.value {
  color: #007bff;
  font-weight: 500;
}

.message {
  position: fixed;
  top: 2rem;
  right: 2rem;
  z-index: 1000;
}

.message-content {
  padding: 1rem 1.5rem;
  border-radius: 8px;
  color: white;
  font-weight: 500;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  animation: slideIn 0.3s ease-out;
}

.message-content.success {
  background: #28a745;
}

.message-content.error {
  background: #dc3545;
}

.message-content.info {
  background: #17a2b8;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .header h1 {
    font-size: 2rem;
  }
  
  .main {
    padding: 0 1rem;
  }
  
  .status-grid {
    grid-template-columns: 1fr;
  }
}
</style> 