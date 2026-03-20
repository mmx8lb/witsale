import api from './api';
import { ApiResponse, Order } from '../types';

interface OrderCreateData {
  customer_id: string;
  items: Array<{
    sku_id: string;
    quantity: number;
  }>;
  total_amount: number;
  payment_method: string;
}

interface PaymentCreateData {
  order_id: string;
  amount: number;
  payment_method: string;
  transaction_id: string;
}

const orderService = {
  // 获取订单列表
  getOrders: async (params: Record<string, any> = {}): Promise<ApiResponse<Order[]>> => {
    try {
      const response = await api.get('/v1/orders', { params });
      return response.data;
    } catch (error) {
      console.error('获取订单列表失败:', error);
      throw error;
    }
  },

  // 获取订单详情
  getOrder: async (id: string): Promise<ApiResponse<Order>> => {
    try {
      const response = await api.get(`/v1/orders/${id}`);
      return response.data;
    } catch (error) {
      console.error(`获取订单详情失败 (ID: ${id}):`, error);
      throw error;
    }
  },

  // 创建订单
  createOrder: async (orderData: OrderCreateData): Promise<ApiResponse<Order>> => {
    try {
      const response = await api.post('/v1/orders', orderData);
      return response.data;
    } catch (error) {
      console.error('创建订单失败:', error);
      throw error;
    }
  },

  // 更新订单状态
  updateOrderStatus: async (id: string, status: string): Promise<ApiResponse<Order>> => {
    try {
      const response = await api.put(`/v1/orders/${id}/status`, { status });
      return response.data;
    } catch (error) {
      console.error(`更新订单状态失败 (ID: ${id}):`, error);
      throw error;
    }
  },

  // 删除订单
  deleteOrder: async (id: string): Promise<ApiResponse<void>> => {
    try {
      const response = await api.delete(`/v1/orders/${id}`);
      return response.data;
    } catch (error) {
      console.error(`删除订单失败 (ID: ${id}):`, error);
      throw error;
    }
  },

  // 创建支付
  createPayment: async (paymentData: PaymentCreateData): Promise<ApiResponse<any>> => {
    try {
      const response = await api.post('/v1/payments', paymentData);
      return response.data;
    } catch (error) {
      console.error('创建支付失败:', error);
      throw error;
    }
  },
};

export default orderService;