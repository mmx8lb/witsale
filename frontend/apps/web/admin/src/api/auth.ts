import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api/v1'

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器，添加token
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 登录API
export const loginAPI = async (credentials: { username: string; password: string }) => {
  const response = await axiosInstance.post('/auth/login', credentials)
  return response.data
}

// 登出API
export const logoutAPI = async () => {
  const response = await axiosInstance.post('/auth/logout')
  return response.data
}

// 获取当前用户信息
export const getCurrentUserAPI = async () => {
  const response = await axiosInstance.get('/auth/me')
  return response.data
}
