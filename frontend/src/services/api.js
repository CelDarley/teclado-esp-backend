import axios from 'axios'

const API_BASE_URL = 'http://10.102.0.108:8191/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
}) 