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

// 获取账户列表
export const getAccountsAPI = async () => {
  const response = await axiosInstance.get('/finance/accounts')
  return response.data
}

// 获取交易列表
export const getTransactionsAPI = async () => {
  const response = await axiosInstance.get('/finance/transactions')
  return response.data
}

// 获取发票列表
export const getInvoicesAPI = async () => {
  const response = await axiosInstance.get('/finance/invoices')
  return response.data
}

// 生成财务报表
export const generateReportAPI = async (params: { startDate: string; endDate: string }) => {
  const response = await axiosInstance.post('/finance/reports/income-statement', params)
  return response.data
}
