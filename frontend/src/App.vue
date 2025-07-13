<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

// Interfaces
interface User {
  id: number
  first_name: string
  last_name: string
  username: string
  pin: string
  is_active_user: boolean
}

interface AccessLog {
  id: number
  user_name: string
  access_time: string
  ip_address?: string
  success: boolean
}

interface SystemStatus {
  total_users: number
  recent_accesses: number
  system_status: string
}

// State
const isLoggedIn = ref(false)
const currentPin = ref('')
const message = ref('')
const messageType = ref('info')
const activeTab = ref('users')
const showUserForm = ref(false)

// Data
const users = ref<User[]>([])
const accessLogs = ref<AccessLog[]>([])
const systemStatus = ref<SystemStatus>({
  total_users: 0,
  recent_accesses: 0,
  system_status: 'offline'
})
const config = ref({
  admin_pin: '8729',
  door_open_duration: 5
})
const newUser = ref({
  first_name: '',
  last_name: '',
  username: '',
  pin: ''
})

// Keypad layout
const keypadLayout = [
  ['1', '2', '3'],
  ['4', '5', '6'],
  ['7', '8', '9'],
  ['*', '0', '#']
]

const API_BASE_URL = 'http://10.102.0.108:8191/api'

// Methods
const showMessage = (msg: string, type: 'success' | 'error' | 'info' = 'info') => {
  message.value = msg
  messageType.value = type
  setTimeout(() => {
    message.value = ''
  }, 5000)
}

const handleKeyPress = (key: string) => {
  if (key === '*') {
    if (currentPin.value.length === 4) {
      login()
    }
  } else if (key === '#') {
    currentPin.value = ''
  } else if (currentPin.value.length < 4) {
    currentPin.value += key
  }
}

const login = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ pin: currentPin.value })
    })
    
    const data = await response.json()
    
    if (data.success) {
      isLoggedIn.value = true
      currentPin.value = ''
      showMessage('Login realizado com sucesso!', 'success')
      loadData()
    } else {
      showMessage(data.message, 'error')
      currentPin.value = ''
    }
  } catch (error) {
    showMessage('Erro de conexão', 'error')
    currentPin.value = ''
  }
}

const logout = () => {
  isLoggedIn.value = false
  currentPin.value = ''
}

const loadData = async () => {
  try {
    // Carregar usuários
    const usersResponse = await fetch(`${API_BASE_URL}/users/`)
    users.value = await usersResponse.json()
    
    // Carregar logs
    const logsResponse = await fetch(`${API_BASE_URL}/logs/`)
    accessLogs.value = await logsResponse.json()
    
    // Carregar status
    const statusResponse = await fetch(`${API_BASE_URL}/status/`)
    systemStatus.value = await statusResponse.json()
  } catch (error) {
    console.error('Erro ao carregar dados:', error)
  }
}

const createUser = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/users/create/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newUser.value)
    })
    
    const data = await response.json()
    
    if (response.ok) {
      showMessage('✅ Usuário criado com sucesso!', 'success')
      showUserForm.value = false
      newUser.value = {
        first_name: '',
        last_name: '',
        username: '',
        pin: ''
      }
      loadData()
    } else {
      // Tratar erros específicos
      if (data.username && data.username.includes('already exists')) {
        showMessage('❌ Usuário já existe! Escolha outro nome de usuário.', 'error')
      } else if (data.pin && data.pin.includes('already exists')) {
        showMessage('❌ PIN já existe! Escolha outro PIN.', 'error')
      } else {
        // Mostrar todos os erros de validação
        const errorMessages = Object.values(data).flat().join(', ')
        showMessage(`❌ Erro ao criar usuário: ${errorMessages}`, 'error')
      }
    }
  } catch (error) {
    showMessage('❌ Erro de conexão com o servidor', 'error')
  }
}

const deleteUser = async (userId: number) => {
  if (!confirm('Tem certeza que deseja excluir este usuário?')) {
    return
  }
  
  try {
    const response = await fetch(`${API_BASE_URL}/users/${userId}/delete/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    const data = await response.json()
    
    if (response.ok) {
      showMessage('✅ Usuário excluído com sucesso!', 'success')
      loadData()
    } else {
      showMessage(`❌ Erro ao excluir usuário: ${data.message || 'Erro desconhecido'}`, 'error')
    }
  } catch (error) {
    showMessage('❌ Erro de conexão com o servidor', 'error')
  }
}

const saveConfig = async () => {
  showMessage('Configurações salvas!', 'success')
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('pt-BR')
}

onMounted(() => {
  // Auto-login para desenvolvimento
  // isLoggedIn.value = true
  // loadData()
})
</script>

<template>
  <div id="app">
    <!-- Login Screen -->
    <div v-if="!isLoggedIn" class="login-container">
      <div class="login-card">
        <h1>🔐 Controle de Acesso</h1>
        <p>Digite o PIN do administrador</p>
        
        <div class="pin-input">
          <div class="pin-display">
            <span v-for="(digit, index) in 4" :key="index" class="pin-dot">
              {{ currentPin[index] || '•' }}
            </span>
          </div>
          
          <div class="keypad">
            <div class="keypad-row" v-for="row in keypadLayout" :key="row.join('')">
              <button 
                v-for="key in row" 
                :key="key"
                @click="handleKeyPress(key)"
                class="keypad-btn"
                :class="{ 'function-key': key === '*' || key === '#' }"
              >
                {{ key }}
              </button>
            </div>
          </div>
        </div>
        
        <div class="message" v-if="message">
          <div class="message-content" :class="messageType">
            {{ message }}
          </div>
        </div>
      </div>
    </div>

    <!-- Main Dashboard -->
    <div v-else class="dashboard">
      <header class="dashboard-header">
        <h1>🏢 Sistema de Controle de Acesso</h1>
        <div class="user-info">
          <span>Administrador</span>
          <button @click="logout" class="logout-btn">Sair</button>
        </div>
      </header>

      <main class="dashboard-main">
        <!-- Status Cards -->
        <div class="status-grid">
          <div class="status-card">
            <h3>👥 Usuários Ativos</h3>
            <div class="status-value">{{ systemStatus.total_users || 0 }}</div>
          </div>
          
          <div class="status-card">
            <h3>📊 Acessos Hoje</h3>
            <div class="status-value">{{ systemStatus.recent_accesses || 0 }}</div>
          </div>
          
          <div class="status-card">
            <h3>🔧 Status Sistema</h3>
            <div class="status-value" :class="{ 'online': systemStatus.system_status === 'online' }">
              {{ systemStatus.system_status === 'online' ? '🟢 Online' : '🔴 Offline' }}
            </div>
          </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="nav-tabs">
          <button 
            @click="activeTab = 'users'"
            :class="{ active: activeTab === 'users' }"
            class="tab-btn"
          >
            👥 Usuários
          </button>
          <button 
            @click="activeTab = 'logs'"
            :class="{ active: activeTab === 'logs' }"
            class="tab-btn"
          >
            📋 Histórico
          </button>
          <button 
            @click="activeTab = 'config'"
            :class="{ active: activeTab === 'config' }"
            class="tab-btn"
          >
            ⚙️ Configurações
          </button>
        </div>

        <!-- Users Tab -->
        <div v-if="activeTab === 'users'" class="tab-content">
          <div class="section-header">
            <h2>Gestão de Usuários</h2>
            <button @click="showUserForm = true" class="add-btn">+ Novo Usuário</button>
          </div>
          
          <div class="users-list">
            <div v-for="user in users" :key="user.id" class="user-card">
              <div class="user-info">
                <h4>{{ user.first_name }} {{ user.last_name }}</h4>
                <p>PIN: {{ user.pin }}</p>
                <p>Usuário: {{ user.username }}</p>
              </div>
              <div class="user-actions">
                <div class="user-status" :class="{ active: user.is_active_user }">
                  {{ user.is_active_user ? 'Ativo' : 'Inativo' }}
                </div>
                <button @click="deleteUser(user.id)" class="delete-btn" title="Excluir usuário">
                  🗑️
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Logs Tab -->
        <div v-if="activeTab === 'logs'" class="tab-content">
          <h2>Histórico de Acessos</h2>
          <div class="logs-list">
            <div v-for="log in accessLogs" :key="log.id" class="log-card" :class="{ success: log.success }">
              <div class="log-info">
                <h4>{{ log.user_name || 'Usuário Desconhecido' }}</h4>
                <p>{{ formatDate(log.access_time) }}</p>
                <p v-if="log.ip_address">IP: {{ log.ip_address }}</p>
              </div>
              <div class="log-status">
                {{ log.success ? '✅ Acesso' : '❌ Negado' }}
              </div>
            </div>
          </div>
        </div>

        <!-- Config Tab -->
        <div v-if="activeTab === 'config'" class="tab-content">
          <h2>Configurações do Sistema</h2>
          <div class="config-form">
            <div class="form-group">
              <label>PIN do Administrador:</label>
              <input v-model="config.admin_pin" type="text" maxlength="4" pattern="[0-9]{4}" />
            </div>
            <div class="form-group">
              <label>Duração da Abertura (segundos):</label>
              <input v-model="config.door_open_duration" type="number" min="1" max="30" />
            </div>
            <button @click="saveConfig" class="save-btn">Salvar Configurações</button>
          </div>
        </div>
      </main>

      <!-- User Form Modal -->
      <div v-if="showUserForm" class="modal-overlay" @click="showUserForm = false">
        <div class="modal" @click.stop>
          <h3>Novo Usuário</h3>
          <form @submit.prevent="createUser">
            <div class="form-group">
              <label>Nome:</label>
              <input v-model="newUser.first_name" type="text" required />
            </div>
            <div class="form-group">
              <label>Sobrenome:</label>
              <input v-model="newUser.last_name" type="text" required />
            </div>
            <div class="form-group">
              <label>Usuário:</label>
              <input v-model="newUser.username" type="text" required />
            </div>
            <div class="form-group">
              <label>PIN (4 dígitos):</label>
              <input v-model="newUser.pin" type="text" maxlength="4" pattern="[0-9]{4}" required />
            </div>
            <div class="form-actions">
              <button type="button" @click="showUserForm = false" class="cancel-btn">Cancelar</button>
              <button type="submit" class="submit-btn">Criar Usuário</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Global Messages -->
    <div class="message" v-if="message">
      <div class="message-content" :class="messageType">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Login Screen */
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.login-card {
  background: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 400px;
  width: 100%;
}

.login-card h1 {
  margin: 0 0 1rem 0;
  color: #333;
  font-size: 2rem;
}

.login-card p {
  color: #666;
  margin-bottom: 2rem;
}

.pin-input {
  margin-bottom: 2rem;
}

.pin-display {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.pin-dot {
  width: 40px;
  height: 40px;
  border: 2px solid #ddd;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
}

.keypad {
  display: grid;
  gap: 0.5rem;
}

.keypad-row {
  display: flex;
  gap: 0.5rem;
}

.keypad-btn {
  width: 60px;
  height: 60px;
  border: none;
  border-radius: 12px;
  background: #f8f9fa;
  font-size: 1.5rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
}

.keypad-btn:hover {
  background: #e9ecef;
  transform: scale(1.05);
}

.keypad-btn.function-key {
  background: #007bff;
  color: white;
}

.keypad-btn.function-key:hover {
  background: #0056b3;
}

/* Dashboard */
.dashboard {
  min-height: 100vh;
  background: #f8f9fa;
}

.dashboard-header {
  background: white;
  padding: 1.5rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard-header h1 {
  margin: 0;
  color: #333;
  font-size: 1.8rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logout-btn {
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
}

.dashboard-main {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.status-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.status-card h3 {
  margin: 0 0 1rem 0;
  color: #666;
  font-size: 1rem;
}

.status-value {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
}

.status-value.online {
  color: #28a745;
}

.nav-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.tab-btn {
  background: white;
  border: none;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tab-btn.active {
  background: #007bff;
  color: white;
}

.tab-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.add-btn {
  background: #28a745;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
}

.users-list, .logs-list {
  display: grid;
  gap: 1rem;
}

.user-card, .log-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  background: #f8f9fa;
}

.user-card.success, .log-card.success {
  border-color: #28a745;
  background: #d4edda;
}

.user-status {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
}

.user-status.active {
  background: #28a745;
  color: white;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.delete-btn {
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.delete-btn:hover {
  background: #c82333;
  transform: scale(1.1);
}

.log-status {
  font-weight: bold;
}

.config-form {
  max-width: 500px;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.save-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
}

.modal h3 {
  margin: 0 0 1.5rem 0;
  color: #333;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.cancel-btn {
  background: #6c757d;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
}

.submit-btn {
  background: #28a745;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
}

/* Messages */
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
  .dashboard-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .nav-tabs {
    flex-direction: column;
  }
  
  .status-grid {
    grid-template-columns: 1fr;
  }
}
</style>
