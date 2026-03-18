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

// 获取客户列表
export const getCustomersAPI = async () => {
  const response = await axiosInstance.get('/customers')
  return response.data
}

// 创建客户
export const createCustomerAPI = async (customer: any) => {
  const response = await axiosInstance.post('/customers', customer)
  return response.data
}

// 更新客户
export const updateCustomerAPI = async (customerId: number, customer: any) => {
  const response = await axiosInstance.put(`/customers/${customerId}`, customer)
  return response.data
}

// 删除客户
export const deleteCustomerAPI = async (customerId: number) => {
  const response = await axiosInstance.delete(`/customers/${customerId}`)
  return response.data
}
