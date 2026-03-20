import api from './api';
import { ApiResponse, Product, Sku, Category } from '../types';

interface ProductCreateData {
  name: string;
  categoryId: string;
  description: string;
  specs?: string;
  attributes?: string;
  status: string;
  image?: string;
}

interface SkuCreateData {
  product_id: string;
  sku_code: string;
  name: string;
  price: number;
  stock: number;
  specs?: string;
}

interface PriceCreateData {
  sku_id: string;
  price: number;
  type: string;
  start_date?: string;
  end_date?: string;
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
      const response = await api.get('/v1/categories');
      return response.data;
    } catch (error) {
      console.error('获取商品分类失败:', error);
      throw error;
    }
  },

  // 获取SKU列表
  getSkus: async (productId: string): Promise<ApiResponse<Sku[]>> => {
    try {
      const response = await api.get('/v1/skus', { params: { product_id: productId } });
      return response.data;
    } catch (error) {
      console.error(`获取SKU列表失败 (商品ID: ${productId}):`, error);
      throw error;
    }
  },

  // 创建SKU
  createSku: async (skuData: SkuCreateData): Promise<ApiResponse<Sku>> => {
    try {
      const response = await api.post('/v1/skus', skuData);
      return response.data;
    } catch (error) {
      console.error('创建SKU失败:', error);
      throw error;
    }
  },

  // 更新SKU
  updateSku: async (id: string, skuData: SkuCreateData): Promise<ApiResponse<Sku>> => {
    try {
      const response = await api.put(`/v1/skus/${id}`, skuData);
      return response.data;
    } catch (error) {
      console.error(`更新SKU失败 (ID: ${id}):`, error);
      throw error;
    }
  },

  // 删除SKU
  deleteSku: async (id: string): Promise<ApiResponse<void>> => {
    try {
      const response = await api.delete(`/v1/skus/${id}`);
      return response.data;
    } catch (error) {
      console.error(`删除SKU失败 (ID: ${id}):`, error);
      throw error;
    }
  },

  // 获取价格列表
  getPrices: async (skuId: string): Promise<ApiResponse<any[]>> => {
    try {
      const response = await api.get('/v1/prices', { params: { sku_id: skuId } });
      return response.data;
    } catch (error) {
      console.error(`获取价格列表失败 (SKU ID: ${skuId}):`, error);
      throw error;
    }
  },

  // 创建价格
  createPrice: async (priceData: PriceCreateData): Promise<ApiResponse<any>> => {
    try {
      const response = await api.post('/v1/prices', priceData);
      return response.data;
    } catch (error) {
      console.error('创建价格失败:', error);
      throw error;
    }
  },
};

export default productService;