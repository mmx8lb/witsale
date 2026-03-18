from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class CustomerCategoryBase(BaseModel):
    """客户分类基础模型"""
    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    parent_category_id: Optional[int] = None
    level: int = Field(default=1, ge=1, le=5)
    is_active: bool = True


class CustomerCategoryCreate(CustomerCategoryBase):
    """客户分类创建模型"""
    pass


class CustomerCategoryUpdate(BaseModel):
    """客户分类更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    parent_category_id: Optional[int] = None
    level: Optional[int] = Field(None, ge=1, le=5)
    is_active: Optional[bool] = None


class CustomerCategoryInDB(CustomerCategoryBase):
    """数据库中的客户分类模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CustomerCategory(CustomerCategoryInDB):
    """客户分类响应模型"""
    parent: Optional["CustomerCategory"] = None
    children: List["CustomerCategory"] = []


class CustomerLevelBase(BaseModel):
    """客户等级基础模型"""
    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    min_spend: float = Field(default=0.0, ge=0.0)
    max_spend: Optional[float] = Field(None, ge=0.0)
    discount_rate: float = Field(default=1.0, ge=0.0, le=1.0)
    priority: int = Field(default=0, ge=0)
    is_active: bool = True


class CustomerLevelCreate(CustomerLevelBase):
    """客户等级创建模型"""
    pass


class CustomerLevelUpdate(BaseModel):
    """客户等级更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    min_spend: Optional[float] = Field(None, ge=0.0)
    max_spend: Optional[float] = Field(None, ge=0.0)
    discount_rate: Optional[float] = Field(None, ge=0.0, le=1.0)
    priority: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class CustomerLevelInDB(CustomerLevelBase):
    """数据库中的客户等级模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CustomerLevel(CustomerLevelInDB):
    """客户等级响应模型"""
    pass


class CustomerContactBase(BaseModel):
    """客户联系人基础模型"""
    name: str = Field(..., min_length=1, max_length=100)
    position: Optional[str] = Field(None, max_length=100)
    phone: str = Field(..., min_length=1, max_length=50)
    email: Optional[str] = Field(None, max_length=100)
    is_primary: bool = False
    remark: Optional[str] = None


class CustomerContactCreate(CustomerContactBase):
    """客户联系人创建模型"""
    pass


class CustomerContactUpdate(BaseModel):
    """客户联系人更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    position: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[str] = Field(None, max_length=100)
    is_primary: Optional[bool] = None
    remark: Optional[str] = None


class CustomerContactInDB(CustomerContactBase):
    """数据库中的客户联系人模型"""
    id: int
    customer_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CustomerContact(CustomerContactInDB):
    """客户联系人响应模型"""
    pass


class CustomerAddressBase(BaseModel):
    """客户地址基础模型"""
    type: str = Field(default="billing", min_length=1, max_length=20)
    province: str = Field(..., min_length=1, max_length=100)
    city: str = Field(..., min_length=1, max_length=100)
    district: str = Field(..., min_length=1, max_length=100)
    address: str = Field(..., min_length=1, max_length=500)
    zip_code: Optional[str] = Field(None, max_length=20)
    is_default: bool = False
    is_active: bool = True


class CustomerAddressCreate(CustomerAddressBase):
    """客户地址创建模型"""
    pass


class CustomerAddressUpdate(BaseModel):
    """客户地址更新模型"""
    type: Optional[str] = Field(None, min_length=1, max_length=20)
    province: Optional[str] = Field(None, min_length=1, max_length=100)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    district: Optional[str] = Field(None, min_length=1, max_length=100)
    address: Optional[str] = Field(None, min_length=1, max_length=500)
    zip_code: Optional[str] = Field(None, max_length=20)
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None


class CustomerAddressInDB(CustomerAddressBase):
    """数据库中的客户地址模型"""
    id: int
    customer_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CustomerAddress(CustomerAddressInDB):
    """客户地址响应模型"""
    pass


class CustomerTagBase(BaseModel):
    """客户标签基础模型"""
    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=50)
    color: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    is_active: bool = True


class CustomerTagCreate(CustomerTagBase):
    """客户标签创建模型"""
    pass


class CustomerTagUpdate(BaseModel):
    """客户标签更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    color: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class CustomerTagInDB(CustomerTagBase):
    """数据库中的客户标签模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CustomerTag(CustomerTagInDB):
    """客户标签响应模型"""
    pass


class CustomerBase(BaseModel):
    """客户基础模型"""
    name: str = Field(..., min_length=1, max_length=200)
    code: str = Field(..., min_length=1, max_length=50)
    short_name: Optional[str] = Field(None, max_length=100)
    type: str = Field(default="enterprise", min_length=1, max_length=20)
    category_id: Optional[int] = None
    level_id: Optional[int] = None
    contact_name: Optional[str] = Field(None, max_length=100)
    contact_phone: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=100)
    website: Optional[str] = Field(None, max_length=200)
    tax_no: Optional[str] = Field(None, max_length=50)
    registered_capital: Optional[float] = Field(None, ge=0.0)
    business_scope: Optional[str] = None
    founding_date: Optional[datetime] = None
    status: str = Field(default="active", min_length=1, max_length=20)
    credit_limit: Optional[float] = Field(None, ge=0.0)
    remark: Optional[str] = None
    is_active: bool = True


class CustomerCreate(CustomerBase):
    """客户创建模型"""
    contacts: Optional[List[CustomerContactCreate]] = []
    addresses: Optional[List[CustomerAddressCreate]] = []
    tag_ids: Optional[List[int]] = []


class CustomerUpdate(BaseModel):
    """客户更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    short_name: Optional[str] = Field(None, max_length=100)
    type: Optional[str] = Field(None, min_length=1, max_length=20)
    category_id: Optional[int] = None
    level_id: Optional[int] = None
    contact_name: Optional[str] = Field(None, max_length=100)
    contact_phone: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=100)
    website: Optional[str] = Field(None, max_length=200)
    tax_no: Optional[str] = Field(None, max_length=50)
    registered_capital: Optional[float] = Field(None, ge=0.0)
    business_scope: Optional[str] = None
    founding_date: Optional[datetime] = None
    status: Optional[str] = Field(None, min_length=1, max_length=20)
    credit_limit: Optional[float] = Field(None, ge=0.0)
    remark: Optional[str] = None
    is_active: Optional[bool] = None


class CustomerInDB(CustomerBase):
    """数据库中的客户模型"""
    id: int
    total_spend: float
    total_orders: int
    credit_balance: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Customer(CustomerInDB):
    """客户响应模型"""
    category: Optional[CustomerCategory] = None
    level: Optional[CustomerLevel] = None
    contacts: List[CustomerContact] = []
    addresses: List[CustomerAddress] = []
    tags: List[CustomerTag] = []


class CustomerUpdateTags(BaseModel):
    """客户标签更新模型"""
    tag_ids: List[int]


# 避免循环引用
CustomerCategory.model_rebuild()
