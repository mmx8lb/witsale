from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Warehouse(Base):
    """仓库模型"""
    __tablename__ = "warehouses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), nullable=False, unique=True, index=True)
    address = Column(String(500), nullable=True)
    contact_person = Column(String(100), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    warehouse_type = Column(String(20), nullable=False, default="central")
    level = Column(Integer, nullable=False, default=1)
    parent_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    parent = relationship("Warehouse", remote_side=[id], backref="children")
    stocks = relationship("Stock", back_populates="warehouse")
    stock_transfers = relationship("StockTransfer", foreign_keys="StockTransfer.from_warehouse_id", back_populates="from_warehouse")
    stock_transfers_to = relationship("StockTransfer", foreign_keys="StockTransfer.to_warehouse_id", back_populates="to_warehouse")


class Stock(Base):
    """库存模型"""
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    product_id = Column(Integer, nullable=False)
    product_name = Column(String(200), nullable=False)
    sku_id = Column(Integer, nullable=True)
    sku_code = Column(String(50), nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    available_quantity = Column(Integer, nullable=False, default=0)
    locked_quantity = Column(Integer, nullable=False, default=0)
    cost_price = Column(Float, nullable=False, default=0.0)
    min_stock = Column(Integer, nullable=False, default=0)
    max_stock = Column(Integer, nullable=True)
    batch_no = Column(String(100), nullable=True)
    expiry_date = Column(DateTime, nullable=True)
    attributes = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    warehouse = relationship("Warehouse", back_populates="stocks")
    stock_movements = relationship("StockMovement", back_populates="stock")


class StockMovement(Base):
    """库存变动记录模型"""
    __tablename__ = "stock_movements"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    movement_type = Column(String(20), nullable=False)
    quantity = Column(Integer, nullable=False)
    before_quantity = Column(Integer, nullable=False)
    after_quantity = Column(Integer, nullable=False)
    reference_type = Column(String(50), nullable=True)
    reference_id = Column(Integer, nullable=True)
    reference_no = Column(String(100), nullable=True)
    remark = Column(Text, nullable=True)
    operator_id = Column(Integer, nullable=True)
    operator_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    stock = relationship("Stock", back_populates="stock_movements")


class StockTransfer(Base):
    """库存调拨模型"""
    __tablename__ = "stock_transfers"
    
    id = Column(Integer, primary_key=True, index=True)
    transfer_no = Column(String(50), nullable=False, unique=True, index=True)
    from_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    to_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    transfer_type = Column(String(20), nullable=False, default="normal")
    transfer_status = Column(String(20), nullable=False, default="pending")
    total_quantity = Column(Integer, nullable=False, default=0)
    remark = Column(Text, nullable=True)
    operator_id = Column(Integer, nullable=True)
    operator_name = Column(String(100), nullable=True)
    approved_by = Column(Integer, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    shipped_at = Column(DateTime, nullable=True)
    received_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    from_warehouse = relationship("Warehouse", foreign_keys=[from_warehouse_id], back_populates="stock_transfers")
    to_warehouse = relationship("Warehouse", foreign_keys=[to_warehouse_id], back_populates="stock_transfers_to")
    items = relationship("StockTransferItem", back_populates="transfer")


class StockTransferItem(Base):
    """库存调拨明细模型"""
    __tablename__ = "stock_transfer_items"
    
    id = Column(Integer, primary_key=True, index=True)
    transfer_id = Column(Integer, ForeignKey("stock_transfers.id"), nullable=False)
    product_id = Column(Integer, nullable=False)
    product_name = Column(String(200), nullable=False)
    sku_id = Column(Integer, nullable=True)
    sku_code = Column(String(50), nullable=True)
    quantity = Column(Integer, nullable=False)
    shipped_quantity = Column(Integer, nullable=False, default=0)
    received_quantity = Column(Integer, nullable=False, default=0)
    remark = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    transfer = relationship("StockTransfer", back_populates="items")


class StockCheck(Base):
    """库存盘点模型"""
    __tablename__ = "stock_checks"
    
    id = Column(Integer, primary_key=True, index=True)
    check_no = Column(String(50), nullable=False, unique=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    check_type = Column(String(20), nullable=False, default="full")
    check_status = Column(String(20), nullable=False, default="pending")
    remark = Column(Text, nullable=True)
    operator_id = Column(Integer, nullable=True)
    operator_name = Column(String(100), nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    warehouse = relationship("Warehouse")
    items = relationship("StockCheckItem", back_populates="check")


class StockCheckItem(Base):
    """库存盘点明细模型"""
    __tablename__ = "stock_check_items"
    
    id = Column(Integer, primary_key=True, index=True)
    check_id = Column(Integer, ForeignKey("stock_checks.id"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    product_id = Column(Integer, nullable=False)
    product_name = Column(String(200), nullable=False)
    sku_id = Column(Integer, nullable=True)
    sku_code = Column(String(50), nullable=True)
    system_quantity = Column(Integer, nullable=False)
    actual_quantity = Column(Integer, nullable=False)
    diff_quantity = Column(Integer, nullable=False)
    remark = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    check = relationship("StockCheck", back_populates="items")
