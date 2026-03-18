from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class WarehouseBase(BaseModel):
    """仓库基础模型"""
    name: str = Field(..., min_length=1, max_length=200)
    code: str = Field(..., min_length=1, max_length=50)
    address: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    warehouse_type: str = Field(default="central", min_length=1, max_length=20)
    level: int = Field(default=1, ge=1, le=5)
    parent_warehouse_id: Optional[int] = None
    is_active: bool = True


class WarehouseCreate(WarehouseBase):
    """仓库创建模型"""
    pass


class WarehouseUpdate(BaseModel):
    """仓库更新模型"""
    name: Optional[str] = None
    code: Optional[str] = None
    address: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    warehouse_type: Optional[str] = None
    level: Optional[int] = None
    parent_warehouse_id: Optional[int] = None
    is_active: Optional[bool] = None


class WarehouseInDB(WarehouseBase):
    """数据库中的仓库模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Warehouse(WarehouseInDB):
    """仓库响应模型"""
    parent: Optional["Warehouse"] = None
    children: List["Warehouse"] = []
    
    class Config:
        from_attributes = True


class StockBase(BaseModel):
    """库存基础模型"""
    warehouse_id: int
    product_id: int
    product_name: str
    sku_id: Optional[int] = None
    sku_code: Optional[str] = None
    quantity: int = Field(default=0, ge=0)
    available_quantity: int = Field(default=0, ge=0)
    locked_quantity: int = Field(default=0, ge=0)
    cost_price: float = Field(default=0.0, ge=0.0)
    min_stock: int = Field(default=0, ge=0)
    max_stock: Optional[int] = None
    batch_no: Optional[str] = None
    expiry_date: Optional[datetime] = None
    attributes: Optional[Dict[str, Any]] = None
    is_active: bool = True


class StockCreate(StockBase):
    """库存创建模型"""
    pass


class StockUpdate(BaseModel):
    """库存更新模型"""
    quantity: Optional[int] = Field(None, ge=0)
    available_quantity: Optional[int] = Field(None, ge=0)
    locked_quantity: Optional[int] = Field(None, ge=0)
    cost_price: Optional[float] = Field(None, ge=0.0)
    min_stock: Optional[int] = Field(None, ge=0)
    max_stock: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class StockInDB(StockBase):
    """数据库中的库存模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Stock(StockInDB):
    """库存响应模型"""
    warehouse: Warehouse


class StockMovementBase(BaseModel):
    """库存变动记录基础模型"""
    stock_id: int
    movement_type: str = Field(..., min_length=1, max_length=20)
    quantity: int
    before_quantity: int
    after_quantity: int
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None
    reference_no: Optional[str] = None
    remark: Optional[str] = None
    operator_id: Optional[int] = None
    operator_name: Optional[str] = None


class StockMovementCreate(StockMovementBase):
    """库存变动记录创建模型"""
    pass


class StockMovementInDB(StockMovementBase):
    """数据库中的库存变动记录模型"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class StockMovement(StockMovementInDB):
    """库存变动记录响应模型"""
    stock: Stock


class StockTransferItemBase(BaseModel):
    """库存调拨明细基础模型"""
    product_id: int
    product_name: str
    sku_id: Optional[int] = None
    sku_code: Optional[str] = None
    quantity: int = Field(..., ge=1)
    shipped_quantity: int = Field(default=0, ge=0)
    received_quantity: int = Field(default=0, ge=0)
    remark: Optional[str] = None


class StockTransferItemCreate(StockTransferItemBase):
    """库存调拨明细创建模型"""
    pass


class StockTransferItemInDB(StockTransferItemBase):
    """数据库中的库存调拨明细模型"""
    id: int
    transfer_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class StockTransferItem(StockTransferItemInDB):
    """库存调拨明细响应模型"""
    pass


class StockTransferBase(BaseModel):
    """库存调拨基础模型"""
    from_warehouse_id: int
    to_warehouse_id: int
    transfer_type: str = Field(default="normal", min_length=1, max_length=20)
    remark: Optional[str] = None


class StockTransferCreate(StockTransferBase):
    """库存调拨创建模型"""
    items: List[StockTransferItemCreate]


class StockTransferUpdate(BaseModel):
    """库存调拨更新模型"""
    remark: Optional[str] = None


class StockTransferInDB(StockTransferBase):
    """数据库中的库存调拨模型"""
    id: int
    transfer_no: str
    transfer_status: str
    total_quantity: int
    operator_id: Optional[int] = None
    operator_name: Optional[str] = None
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    received_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class StockTransfer(StockTransferInDB):
    """库存调拨响应模型"""
    from_warehouse: Warehouse
    to_warehouse: Warehouse
    items: List[StockTransferItem] = []


class StockCheckItemBase(BaseModel):
    """库存盘点明细基础模型"""
    stock_id: int
    product_id: int
    product_name: str
    sku_id: Optional[int] = None
    sku_code: Optional[str] = None
    system_quantity: int
    actual_quantity: int
    diff_quantity: int
    remark: Optional[str] = None


class StockCheckItemCreate(StockCheckItemBase):
    """库存盘点明细创建模型"""
    pass


class StockCheckItemInDB(StockCheckItemBase):
    """数据库中的库存盘点明细模型"""
    id: int
    check_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class StockCheckItem(StockCheckItemInDB):
    """库存盘点明细响应模型"""
    pass


class StockCheckBase(BaseModel):
    """库存盘点基础模型"""
    warehouse_id: int
    check_type: str = Field(default="full", min_length=1, max_length=20)
    remark: Optional[str] = None


class StockCheckCreate(StockCheckBase):
    """库存盘点创建模型"""
    items: List[StockCheckItemCreate]


class StockCheckUpdate(BaseModel):
    """库存盘点更新模型"""
    remark: Optional[str] = None


class StockCheckInDB(StockCheckBase):
    """数据库中的库存盘点模型"""
    id: int
    check_no: str
    check_status: str
    operator_id: Optional[int] = None
    operator_name: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class StockCheck(StockCheckInDB):
    """库存盘点响应模型"""
    warehouse: Warehouse
    items: List[StockCheckItem] = []


class StockAdjustmentRequest(BaseModel):
    """库存调整请求模型"""
    stock_id: int
    adjustment_quantity: int
    remark: str


class StockLockRequest(BaseModel):
    """库存锁定请求模型"""
    stock_id: int
    lock_quantity: int
    reference_type: str
    reference_id: int
    reference_no: Optional[str] = None


class StockUnlockRequest(BaseModel):
    """库存解锁请求模型"""
    stock_id: int
    unlock_quantity: int
    reference_type: str
    reference_id: int


# 避免循环引用
Warehouse.model_rebuild()
