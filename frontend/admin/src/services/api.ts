import axios from 'axios';
import { ApiResponse } from '../types';

// 创建axios实例
const api = axios.create({
  baseURL: '/api', // 后端API地址（使用Vite代理）
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    // 确保返回的数据符合ApiResponse格式
    const data = response.data;
    response.data = {
      data: data.data || data,
      message: data.message || 'Success',
      success: data.success !== false
    } as ApiResponse<any>;
    return response;
  },
  error => {
    // 处理错误响应
    if (error.response) {
      // 服务器返回错误状态码
      switch (error.response.status) {
        case 401:
          // 未授权，跳转到登录页
          window.location.href = '/login';
          break;
        case 403:
          // 禁止访问
          alert('没有权限访问该资源');
          break;
        case 404:
          // 资源不存在
          alert('请求的资源不存在');
          break;
        case 500:
          // 服务器错误
          alert('服务器内部错误');
          break;
        default:
          alert(`请求失败: ${error.response.data.message || '未知错误'}`);
      }
    } else if (error.request) {
      // 请求已发出但没有收到响应
      alert('网络错误，请检查网络连接');
    } else {
      // 请求配置出错
      alert(`请求配置出错: ${error.message}`);
    }
    return Promise.reject(error);
  }
);

export default api;