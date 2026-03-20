import api from './api';
import { ApiResponse, Customer, Tag } from '../types';

interface CustomerCreateData {
  name: string;
  phone: string;
  email: string;
  level: string;
  status: string;
  tags?: string[];
}

const customerService = {
  // 获取客户列表
  getCustomers: async (params: Record<string, any> = {}): Promise<ApiResponse<Customer[]>> => {
    try {
      const response = await api.get('/v1/customers', { params });
      return response.data;
    } catch (error) {
      console.error('获取客户列表失败:', error);
      throw error;
    }
  },

  // 获取客户详情
  getCustomer: async (id: string): Promise<ApiResponse<Customer>> => {
    try {
      const response = await api.get(`/v1/customers/${id}`);
      return response.data;
    } catch (error) {
      console.error(`获取客户详情失败 (ID: ${id}):`, error);
      throw error;
    }
  },

  // 创建客户
  createCustomer: async (customerData: CustomerCreateData): Promise<ApiResponse<Customer>> => {
    try {
      const response = await api.post('/v1/customers', customerData);
      return response.data;
    } catch (error) {
      console.error('创建客户失败:', error);
      throw error;
    }
  },

  // 更新客户
  updateCustomer: async (id: string, customerData: CustomerCreateData): Promise<ApiResponse<Customer>> => {
    try {
      const response = await api.put(`/v1/customers/${id}`, customerData);
      return response.data;
    } catch (error) {
      console.error(`更新客户失败 (ID: ${id}):`, error);
      throw error;
    }
  },

  // 删除客户
  deleteCustomer: async (id: string): Promise<ApiResponse<void>> => {
    try {
      const response = await api.delete(`/v1/customers/${id}`);
      return response.data;
    } catch (error) {
      console.error(`删除客户失败 (ID: ${id}):`, error);
      throw error;
    }
  },

  // 获取标签列表
  getTags: async (): Promise<ApiResponse<Tag[]>> => {
    try {
      const response = await api.get('/v1/tags');
      return response.data;
    } catch (error) {
      console.error('获取标签列表失败:', error);
      throw error;
    }
  },

  // 更新客户标签
  updateCustomerTags: async (customerId: string, tagIds: string[]): Promise<ApiResponse<Customer>> => {
    try {
      const response = await api.put(`/v1/customers/${customerId}/tags`, { tag_ids: tagIds });
      return response.data;
    } catch (error) {
      console.error(`更新客户标签失败 (客户ID: ${customerId}):`, error);
      throw error;
    }
  },
};

export default customerService;