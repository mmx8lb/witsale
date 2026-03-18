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

// 获取订单列表
export const getOrdersAPI = async () => {
  const response = await axiosInstance.get('/orders')
  return response.data
}

// 更新订单状态
export const updateOrderStatusAPI = async (orderId: number, status: string) => {
  const response = await axiosInstance.patch(`/orders/${orderId}/status`, { status })
  return response.data
}

// 获取订单详情
export const getOrderDetailAPI = async (orderId: number) => {
  const response = await axiosInstance.get(`/orders/${orderId}`)
  return response.data
}
