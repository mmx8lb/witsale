import api from './api';
import { ApiResponse, Inventory, Warehouse, InventoryMovement } from '../types';

interface InventoryAdjustmentData {
  inventory_id: string;
  type: 'increase' | 'decrease';
  quantity: number;
  reason: string;
  reference?: string;
}

const inventoryService = {
  // 获取库存列表
  getInventory: async (params: Record<string, any> = {}): Promise<ApiResponse<Inventory[]>> => {
    try {
      const response = await api.get('/v1/inventory/stocks', { params });
      return response.data;
    } catch (error) {
      console.error('获取库存列表失败:', error);
      throw error;
    }
  },

  // 获取库存详情
  getInventoryById: async (id: string): Promise<ApiResponse<Inventory>> => {
    try {
      const response = await api.get(`/v1/inventory/stocks/${id}`);
      return response.data;
    } catch (error) {
      console.error(`获取库存详情失败 (ID: ${id}):`, error);
      throw error;
    }
  },

  // 库存调整
  adjustInventory: async (adjustmentData: InventoryAdjustmentData): Promise<ApiResponse<Inventory>> => {
    try {
      const response = await api.post('/v1/inventory/stocks/adjust', adjustmentData);
      return response.data;
    } catch (error) {
      console.error('库存调整失败:', error);
      throw error;
    }
  },

  // 获取仓库列表
  getWarehouses: async (): Promise<ApiResponse<Warehouse[]>> => {
    try {
      const response = await api.get('/v1/inventory/warehouses');
      return response.data;
    } catch (error) {
      console.error('获取仓库列表失败:', error);
      throw error;
    }
  },

  // 获取库存变动记录
  getMovements: async (params: Record<string, any> = {}): Promise<ApiResponse<InventoryMovement[]>> => {
    try {
      const response = await api.get('/v1/inventory/transfers', { params });
      return response.data;
    } catch (error) {
      console.error('获取库存变动记录失败:', error);
      throw error;
    }
  },
};

export default inventoryService;