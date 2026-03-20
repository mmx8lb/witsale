import api from './api';
import { ApiResponse, Product, Sku, Category } from '../types';

interface ProductCreateData {
  name: string;
  category_id: number;
  description?: string;
  brand?: string;
  model?: string;
  is_active: boolean;
  image?: string;
}

interface SkuCreateData {
  product_id: string;
  sku_code: string;
  name: string;
  stock: number;
  cost_price: number;
  weight?: number;
  volume?: number;
  attributes?: any;
  is_active: boolean;
}

interface PriceCreateData {
  sku_id: string;
  price_type: string;
  price: number;
  min_quantity?: number;
  max_quantity?: number;
  is_active?: boolean;
}

const productService = {
  // 获取商品列表
  getProducts: async (params: Record<string, any> = {}): Promise<ApiResponse<Product[]>> => {
    try {
      const response = await api.get('/v1/products', { params });
      return response.data;
    } catch (error) {
      console.error('获取商品列表失败:', error);
      throw error;
    }
  },

  // 获取商品详情
  getProduct: async (id: string): Promise<ApiResponse<Product>> => {
    try {
      const response = await api.get(`/v1/products/${id}`);
      return response.data;
    } catch (error) {
      console.error(`获取商品详情失败 (ID: ${id}):`, error);
      throw error;
    }
  },

  // 创建商品
  createProduct: async (productData: ProductCreateData): Promise<ApiResponse<Product>> => {
    try {
      const response = await api.post('/v1/products', productData);
      return response.data;
    } catch (error) {
      console.error('创建商品失败:', error);
      throw error;
    }
  },

  // 更新商品
  updateProduct: async (id: string, productData: ProductCreateData): Promise<ApiResponse<Product>> => {
    try {
      const response = await api.put(`/v1/products/${id}`, productData);
      return response.data;
    } catch (error) {
      console.error(`更新商品失败 (ID: ${id}):`, error);
      throw error;
    }
  },

  // 删除商品
  deleteProduct: async (id: string): Promise<ApiResponse<void>> => {
    try {
      const response = await api.delete(`/v1/products/${id}`);
      return response.data;
    } catch (error) {
      console.error(`删除商品失败 (ID: ${id}):`, error);
      throw error;
    }
  },

  // 获取商品分类列表
  getCategories: async (): Promise<ApiResponse<Category[]>> => {
    try {
      const response = await api.get('/v1/products/categories');
      return response.data;
    } catch (error) {
      console.error('获取商品分类失败:', error);
      throw error;
    }
  },

  // 创建分类
  createCategory: async (categoryData: any): Promise<ApiResponse<Category>> => {
    try {
      const response = await api.post('/v1/products/categories', categoryData);
      return response.data;
    } catch (error) {
      console.error('创建分类失败:', error);
      throw error;
    }
  },

  // 更新分类
  updateCategory: async (id: string, categoryData: any): Promise<ApiResponse<Category>> => {
    try {
      const response = await api.put(`/v1/products/categories/${id}`, categoryData);
      return response.data;
    } catch (error) {
      console.error('更新分类失败:', error);
      throw error;
    }
  },

  // 删除分类
  deleteCategory: async (id: string): Promise<ApiResponse<void>> => {
    try {
      const response = await api.delete(`/v1/products/categories/${id}`);
      return response.data;
    } catch (error) {
      console.error('删除分类失败:', error);
      throw error;
    }
  },

  // 获取SKU列表
  getSkus: async (productId: string): Promise<ApiResponse<Sku[]>> => {
    try {
      const response = await api.get(`/v1/products/${productId}/skus`);
      return response.data;
    } catch (error) {
      console.error(`获取SKU列表失败 (商品ID: ${productId}):`, error);
      throw error;
    }
  },

  // 创建SKU
  createSku: async (skuData: SkuCreateData): Promise<ApiResponse<Sku>> => {
    try {
      // 从skuData中移除product_id字段，因为它是通过URL路径传递的
      const { product_id, ...skuDataWithoutProductId } = skuData;
      const response = await api.post(`/v1/products/${product_id}/skus`, skuDataWithoutProductId);
      return response.data;
    } catch (error) {
      console.error('创建SKU失败:', error);
      throw error;
    }
  },

  // 更新SKU
  updateSku: async (id: string, skuData: SkuCreateData): Promise<ApiResponse<Sku>> => {
    try {
      // 从skuData中移除product_id字段，因为更新SKU时不需要它
      const { product_id, ...skuDataWithoutProductId } = skuData;
      const response = await api.put(`/v1/products/skus/${id}`, skuDataWithoutProductId);
      return response.data;
    } catch (error) {
      console.error(`更新SKU失败 (ID: ${id}):`, error);
      throw error;
    }
  },

  // 删除SKU
  deleteSku: async (id: string): Promise<ApiResponse<void>> => {
    try {
      const response = await api.delete(`/v1/products/skus/${id}`);
      return response.data;
    } catch (error) {
      console.error(`删除SKU失败 (ID: ${id}):`, error);
      throw error;
    }
  },

  // 获取价格列表
  getPrices: async (skuId: string): Promise<ApiResponse<any[]>> => {
    try {
      const response = await api.get(`/v1/products/skus/${skuId}/prices`);
      return response.data;
    } catch (error) {
      console.error(`获取价格列表失败 (SKU ID: ${skuId}):`, error);
      throw error;
    }
  },

  // 创建价格
  createPrice: async (priceData: PriceCreateData): Promise<ApiResponse<any>> => {
    try {
      const response = await api.post(`/v1/products/skus/${priceData.sku_id}/prices`, priceData);
      return response.data;
    } catch (error) {
      console.error('创建价格失败:', error);
      throw error;
    }
  },

  // 更新价格
  updatePrice: async (id: string, priceData: PriceCreateData): Promise<ApiResponse<any>> => {
    try {
      const response = await api.put(`/v1/products/prices/${id}`, priceData);
      return response.data;
    } catch (error) {
      console.error(`更新价格失败 (ID: ${id}):`, error);
      throw error;
    }
  },

  // 删除价格
  deletePrice: async (id: string): Promise<ApiResponse<void>> => {
    try {
      const response = await api.delete(`/v1/products/prices/${id}`);
      return response.data;
    } catch (error) {
      console.error(`删除价格失败 (ID: ${id}):`, error);
      throw error;
    }
  },
};

export default productService;