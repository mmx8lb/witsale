from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class CategoryBase(BaseModel):
    """分类基础模型"""
    name: str = Field(..., min_length=1, max_length=100)
    parent_id: Optional[int] = None
    level: int = Field(default=1, ge=1, le=5)
    sort: int = Field(default=0, ge=0)
    is_active: bool = True


class CategoryCreate(CategoryBase):
    """分类创建模型"""
    pass


class CategoryUpdate(BaseModel):
    """分类更新模型"""
    name: Optional[str] = None
    parent_id: Optional[int] = None
    level: Optional[int] = Field(None, ge=1, le=5)
    sort: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class CategoryInDB(CategoryBase):
    """数据库中的分类模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Category(CategoryInDB):
    """分类响应模型"""
    pass


class ProductAttributeBase(BaseModel):
    """商品属性基础模型"""
    name: str = Field(..., min_length=1, max_length=100)
    value: Any
    is_active: bool = True


class ProductAttributeCreate(ProductAttributeBase):
    """商品属性创建模型"""
    pass


class ProductAttributeUpdate(BaseModel):
    """商品属性更新模型"""
    name: Optional[str] = None
    value: Optional[Any] = None
    is_active: Optional[bool] = None


class ProductAttributeInDB(ProductAttributeBase):
    """数据库中的商品属性模型"""
    id: int
    product_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductAttribute(ProductAttributeInDB):
    """商品属性响应模型"""
    pass


class ProductSKUBase(BaseModel):
    """商品SKU基础模型"""
    sku_code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    stock: int = Field(default=0, ge=0)
    cost_price: float = Field(default=0.0, ge=0.0)
    weight: Optional[float] = Field(None, ge=0.0)
    volume: Optional[float] = Field(None, ge=0.0)
    attributes: Optional[Dict[str, Any]] = None
    is_active: bool = True


class ProductSKUCreate(ProductSKUBase):
    """商品SKU创建模型"""
    pass


class ProductSKUUpdate(BaseModel):
    """商品SKU更新模型"""
    sku_code: Optional[str] = None
    name: Optional[str] = None
    stock: Optional[int] = Field(None, ge=0)
    cost_price: Optional[float] = Field(None, ge=0.0)
    weight: Optional[float] = Field(None, ge=0.0)
    volume: Optional[float] = Field(None, ge=0.0)
    attributes: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class ProductSKUInDB(ProductSKUBase):
    """数据库中的商品SKU模型"""
    id: int
    product_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductPriceBase(BaseModel):
    """商品价格基础模型"""
    price_type: str = Field(..., min_length=1, max_length=20)
    price: float = Field(..., ge=0.0)
    min_quantity: int = Field(default=1, ge=1)
    max_quantity: Optional[int] = Field(None, ge=1)
    is_active: bool = True


class ProductPriceCreate(ProductPriceBase):
    """商品价格创建模型"""
    pass


class ProductPriceUpdate(BaseModel):
    """商品价格更新模型"""
    price_type: Optional[str] = None
    price: Optional[float] = Field(None, ge=0.0)
    min_quantity: Optional[int] = Field(None, ge=1)
    max_quantity: Optional[int] = Field(None, ge=1)
    is_active: Optional[bool] = None


class ProductPriceInDB(ProductPriceBase):
    """数据库中的商品价格模型"""
    id: int
    sku_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductPrice(ProductPriceInDB):
    """商品价格响应模型"""
    pass


class ProductSKU(ProductSKUInDB):
    """商品SKU响应模型"""
    prices: List[ProductPrice] = []


class ProductBase(BaseModel):
    """商品基础模型"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category_id: int
    brand: Optional[str] = None
    model: Optional[str] = None
    is_active: bool = True


class ProductCreate(ProductBase):
    """商品创建模型"""
    pass


class ProductUpdate(BaseModel):
    """商品更新模型"""
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    is_active: Optional[bool] = None


class ProductInDB(ProductBase):
    """数据库中的商品模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Product(ProductInDB):
    """商品响应模型"""
    category: Category
    skus: List[ProductSKU] = []
    attributes: List[ProductAttribute] = []


# 避免循环引用
Category.model_rebuild()
