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

// 获取库存列表
export const getInventoryAPI = async () => {
  const response = await axiosInstance.get('/inventory')
  return response.data
}

// 更新库存
export const updateInventoryAPI = async (inventoryId: number, inventory: any) => {
  const response = await axiosInstance.put(`/inventory/${inventoryId}`, inventory)
  return response.data
}

// 库存调拨
export const transferInventoryAPI = async (transferData: any) => {
  const response = await axiosInstance.post('/inventory/transfer', transferData)
  return response.data
}
