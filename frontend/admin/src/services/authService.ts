import api from './api';
import { ApiResponse } from '../types';

interface LoginData {
  username: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: {
    id: string;
    username: string;
    email: string;
    role: {
      id: string;
      name: string;
      description: string;
    };
  };
}

const authService = {
  // 登录
  login: async (loginData: LoginData): Promise<ApiResponse<LoginResponse>> => {
    try {
      // 使用application/x-www-form-urlencoded格式发送登录请求
      const response = await api.post('/auth/login', new URLSearchParams({
        username: loginData.username,
        password: loginData.password
      }), {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      
      // 存储token到localStorage
      if (response.data.data.access_token) {
        localStorage.setItem('token', response.data.data.access_token);
        // 触发storage事件，让App组件更新认证状态
        window.dispatchEvent(new Event('storage'));
      }
      
      return response.data;
    } catch (error) {
      console.error('登录失败:', error);
      throw error;
    }
  },

  // 登出
  logout: (): void => {
    localStorage.removeItem('token');
    // 触发storage事件，让App组件更新认证状态
    window.dispatchEvent(new Event('storage'));
  },

  // 检查是否已登录
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('token');
  },

  // 获取当前用户信息
  getCurrentUser: async (): Promise<ApiResponse<any>> => {
    try {
      const response = await api.get('/auth/me');
      return response.data;
    } catch (error) {
      console.error('获取用户信息失败:', error);
      throw error;
    }
  },
};

export default authService;