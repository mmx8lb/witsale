from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class OrderItemBase(BaseModel):
    """订单商品明细基础模型"""
    product_id: int
    product_name: str
    sku_id: Optional[int] = None
    sku_code: Optional[str] = None
    quantity: int = Field(default=1, ge=1)
    unit_price: float = Field(..., ge=0.0)
    total_price: float = Field(..., ge=0.0)
    discount_price: float = Field(default=0.0, ge=0.0)
    attributes: Optional[Dict[str, Any]] = None


class OrderItemCreate(OrderItemBase):
    """订单商品明细创建模型"""
    pass


class OrderItemUpdate(BaseModel):
    """订单商品明细更新模型"""
    quantity: Optional[int] = Field(None, ge=1)
    unit_price: Optional[float] = Field(None, ge=0.0)
    discount_price: Optional[float] = Field(None, ge=0.0)


class OrderItemInDB(OrderItemBase):
    """数据库中的订单商品明细模型"""
    id: int
    order_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OrderItem(OrderItemInDB):
    """订单商品明细响应模型"""
    pass


class OrderPaymentBase(BaseModel):
    """订单支付记录基础模型"""
    payment_method: str = Field(..., min_length=1, max_length=50)
    amount: float = Field(..., ge=0.0)
    transaction_id: Optional[str] = None
    notes: Optional[str] = None


class OrderPaymentCreate(OrderPaymentBase):
    """订单支付记录创建模型"""
    pass


class OrderPaymentInDB(OrderPaymentBase):
    """数据库中的订单支付记录模型"""
    id: int
    order_id: int
    payment_no: str
    payment_status: str
    paid_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OrderPayment(OrderPaymentInDB):
    """订单支付记录响应模型"""
    pass


class OrderStatusHistoryBase(BaseModel):
    """订单状态历史记录基础模型"""
    status: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None
    operator_id: Optional[int] = None
    operator_name: Optional[str] = None


class OrderStatusHistoryCreate(OrderStatusHistoryBase):
    """订单状态历史记录创建模型"""
    pass


class OrderStatusHistoryInDB(OrderStatusHistoryBase):
    """数据库中的订单状态历史记录模型"""
    id: int
    order_id: int
    previous_status: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class OrderStatusHistory(OrderStatusHistoryInDB):
    """订单状态历史记录响应模型"""
    pass


class OrderRefundBase(BaseModel):
    """订单退款记录基础模型"""
    refund_type: str = Field(..., min_length=1, max_length=20)
    refund_amount: float = Field(..., ge=0.0)
    reason: Optional[str] = None
    notes: Optional[str] = None


class OrderRefundCreate(OrderRefundBase):
    """订单退款记录创建模型"""
    pass


class OrderRefundUpdate(BaseModel):
    """订单退款记录更新模型"""
    refund_status: Optional[str] = None
    notes: Optional[str] = None


class OrderRefundInDB(OrderRefundBase):
    """数据库中的订单退款记录模型"""
    id: int
    order_id: int
    refund_no: str
    refund_status: str
    processed_at: Optional[datetime] = None
    processed_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OrderRefund(OrderRefundInDB):
    """订单退款记录响应模型"""
    pass


class OrderBase(BaseModel):
    """订单基础模型"""
    customer_id: int
    customer_name: str
    order_type: str = Field(default="sales", min_length=1, max_length=20)
    order_level: str = Field(default="enterprise", min_length=1, max_length=20)
    parent_order_id: Optional[int] = None
    shipping_address: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    """订单创建模型"""
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    """订单更新模型"""
    shipping_address: Optional[Dict[str, Any]] = None
    logistics_company: Optional[str] = None
    tracking_number: Optional[str] = None
    notes: Optional[str] = None


class OrderStatusUpdate(BaseModel):
    """订单状态更新模型"""
    order_status: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None


class OrderPaymentRequest(BaseModel):
    """订单支付请求模型"""
    payment_method: str = Field(..., min_length=1, max_length=50)
    transaction_id: Optional[str] = None
    notes: Optional[str] = None


class OrderShipRequest(BaseModel):
    """订单发货请求模型"""
    logistics_company: str = Field(..., min_length=1, max_length=100)
    tracking_number: str = Field(..., min_length=1, max_length=100)
    notes: Optional[str] = None


class OrderCancelRequest(BaseModel):
    """订单取消请求模型"""
    reason: str


class OrderInDB(OrderBase):
    """数据库中的订单模型"""
    id: int
    order_no: str
    total_amount: float
    actual_amount: float
    discount_amount: float
    payment_method: Optional[str] = None
    payment_status: str
    order_status: str
    logistics_company: Optional[str] = None
    tracking_number: Optional[str] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Order(OrderInDB):
    """订单响应模型"""
    items: List[OrderItem] = []
    payments: List[OrderPayment] = []
    status_history: List[OrderStatusHistory] = []
    refunds: List[OrderRefund] = []


class OrderList(OrderInDB):
    """订单列表响应模型（简化版）"""
    pass


class OrderStats(BaseModel):
    """订单统计数据模型"""
    total_orders: int
    total_amount: float
    paid_orders: int
    shipped_orders: int
    completed_orders: int
    cancelled_orders: int
