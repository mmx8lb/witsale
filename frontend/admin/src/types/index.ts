// 商品相关类型
export interface Product {
  id: string;
  name: string;
  category: string;
  categoryId: string;
  description: string;
  status: string;
  created_at: string;
  updated_at: string;
  skus: Sku[];
}

export interface Sku {
  id: string;
  sku_code: string;
  name: string;
  price: number;
  stock: number;
}

export interface Category {
  title: string;
  value: string;
  children?: Category[];
}

// 订单相关类型
export interface Order {
  orderId: string;
  customer: string;
  amount: number;
  status: string;
  date: string;
  items?: OrderItem[];
}

export interface OrderItem {
  product: string;
  quantity: number;
  price: number;
}

// 库存相关类型
export interface Inventory {
  id: string;
  sku_id: string;
  sku_code: string;
  sku_name: string;
  product_name: string;
  warehouse_id: string;
  warehouse_name: string;
  quantity: number;
  reserved_quantity: number;
  threshold: number;
  status: string;
  updated_at: string;
}

export interface Warehouse {
  id: string;
  name: string;
  type: string;
  status: string;
}

export interface InventoryMovement {
  id: string;
  sku_code: string;
  type: string;
  quantity: number;
  warehouse?: string;
  from_warehouse?: string;
  to_warehouse?: string;
  reference?: string;
  created_at: string;
}

// 客户相关类型
export interface Customer {
  id: string;
  name: string;
  phone: string;
  email: string;
  level: string;
  status: string;
  tags: string[];
}

export interface Tag {
  id: string;
  name: string;
  color: string;
}

// API响应类型
export interface ApiResponse<T> {
  data: T;
  message: string;
  success: boolean;
}
