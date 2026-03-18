from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Order(Base):
    """订单主表模型"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(50), nullable=False, unique=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    customer_name = Column(String(200), nullable=False)
    order_type = Column(String(20), nullable=False, default="sales")
    order_level = Column(String(20), nullable=False, default="enterprise")
    parent_order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    total_amount = Column(Float, nullable=False, default=0.0)
    actual_amount = Column(Float, nullable=False, default=0.0)
    discount_amount = Column(Float, nullable=False, default=0.0)
    payment_method = Column(String(50), nullable=True)
    payment_status = Column(String(20), nullable=False, default="unpaid")
    order_status = Column(String(20), nullable=False, default="pending")
    shipping_address = Column(JSON, nullable=True)
    logistics_company = Column(String(100), nullable=True)
    tracking_number = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    parent = relationship("Order", remote_side=[id], backref="children")
    items = relationship("OrderItem", back_populates="order")
    payments = relationship("OrderPayment", back_populates="order")
    status_history = relationship("OrderStatusHistory", back_populates="order")
    refunds = relationship("OrderRefund", back_populates="order")


class OrderItem(Base):
    """订单商品明细模型"""
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, nullable=False)
    product_name = Column(String(200), nullable=False)
    sku_id = Column(Integer, nullable=True)
    sku_code = Column(String(50), nullable=True)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    discount_price = Column(Float, nullable=False, default=0.0)
    attributes = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    order = relationship("Order", back_populates="items")


class OrderPayment(Base):
    """订单支付记录模型"""
    __tablename__ = "order_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    payment_no = Column(String(50), nullable=False, unique=True, index=True)
    payment_method = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_id = Column(String(100), nullable=True)
    payment_status = Column(String(20), nullable=False, default="pending")
    paid_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    order = relationship("Order", back_populates="payments")


class OrderStatusHistory(Base):
    """订单状态历史记录模型"""
    __tablename__ = "order_status_history"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    status = Column(String(20), nullable=False)
    previous_status = Column(String(20), nullable=True)
    description = Column(Text, nullable=True)
    operator_id = Column(Integer, nullable=True)
    operator_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    order = relationship("Order", back_populates="status_history")


class OrderRefund(Base):
    """订单退款记录模型"""
    __tablename__ = "order_refunds"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    refund_no = Column(String(50), nullable=False, unique=True, index=True)
    refund_type = Column(String(20), nullable=False)
    refund_amount = Column(Float, nullable=False)
    reason = Column(Text, nullable=True)
    refund_status = Column(String(20), nullable=False, default="pending")
    processed_at = Column(DateTime, nullable=True)
    processed_by = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    order = relationship("Order", back_populates="refunds")
