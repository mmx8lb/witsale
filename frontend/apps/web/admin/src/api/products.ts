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

// 获取商品列表
export const getProductsAPI = async () => {
  const response = await axiosInstance.get('/products')
  return response.data
}

// 创建商品
export const createProductAPI = async (product: any) => {
  const response = await axiosInstance.post('/products', product)
  return response.data
}

// 更新商品
export const updateProductAPI = async (productId: number, product: any) => {
  const response = await axiosInstance.put(`/products/${productId}`, product)
  return response.data
}

// 删除商品
export const deleteProductAPI = async (productId: number) => {
  const response = await axiosInstance.delete(`/products/${productId}`)
  return response.data
}
