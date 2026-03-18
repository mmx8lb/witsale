from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.application.services.product_service import ProductService
from app.schemas.product import (
    CategoryCreate, CategoryUpdate, Category,
    ProductCreate, ProductUpdate, Product,
    ProductSKUCreate, ProductSKUUpdate, ProductSKU,
    ProductPriceCreate, ProductPriceUpdate, ProductPrice,
    ProductAttributeCreate, ProductAttribute
)
from app.interfaces.api.deps import get_current_active_user
from app.models import User

router = APIRouter(prefix="/products", tags=["products"])


# 分类相关接口
@router.post("/categories", response_model=Category)
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建商品分类"""
    service = ProductService(db)
    return await service.create_category(category)

@router.get("/categories", response_model=List[Category])
async def get_categories(
    parent_id: Optional[int] = Query(None, description="父分类ID"),
    is_active: Optional[bool] = Query(None, description="是否激活"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取分类列表"""
    service = ProductService(db)
    return await service.get_categories(parent_id, is_active)

@router.get("/categories/{category_id}", response_model=Category)
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取分类详情"""
    service = ProductService(db)
    category = await service.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    return category

@router.put("/categories/{category_id}", response_model=Category)
async def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新分类"""
    service = ProductService(db)
    updated_category = await service.update_category(category_id, category)
    if not updated_category:
        raise HTTPException(status_code=404, detail="分类不存在")
    return updated_category

@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除分类"""
    service = ProductService(db)
    deleted = await service.delete_category(category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="分类不存在")
    return {"message": "分类删除成功"}


# 商品相关接口
@router.post("", response_model=Product)
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建商品"""
    service = ProductService(db)
    return await service.create_product(product)

@router.get("", response_model=List[Product])
async def get_products(
    category_id: Optional[int] = Query(None, description="分类ID"),
    is_active: Optional[bool] = Query(None, description="是否激活"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取商品列表"""
    service = ProductService(db)
    return await service.get_products(category_id, is_active, skip, limit)

@router.get("/{product_id}", response_model=Product)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取商品详情"""
    service = ProductService(db)
    product = await service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product

@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新商品"""
    service = ProductService(db)
    updated_product = await service.update_product(product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return updated_product

@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除商品"""
    service = ProductService(db)
    deleted = await service.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="商品不存在")
    return {"message": "商品删除成功"}


# SKU相关接口
@router.post("/{product_id}/skus", response_model=ProductSKU)
async def create_sku(
    product_id: int,
    sku: ProductSKUCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """为商品创建SKU"""
    service = ProductService(db)
    return await service.create_sku(product_id, sku)

@router.get("/{product_id}/skus", response_model=List[ProductSKU])
async def get_skus(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取商品的SKU列表"""
    service = ProductService(db)
    return await service.get_skus_by_product(product_id)

@router.get("/skus/{sku_id}", response_model=ProductSKU)
async def get_sku(
    sku_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取SKU详情"""
    service = ProductService(db)
    sku = await service.get_sku(sku_id)
    if not sku:
        raise HTTPException(status_code=404, detail="SKU不存在")
    return sku

@router.put("/skus/{sku_id}", response_model=ProductSKU)
async def update_sku(
    sku_id: int,
    sku: ProductSKUUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新SKU"""
    service = ProductService(db)
    updated_sku = await service.update_sku(sku_id, sku)
    if not updated_sku:
        raise HTTPException(status_code=404, detail="SKU不存在")
    return updated_sku

@router.delete("/skus/{sku_id}")
async def delete_sku(
    sku_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除SKU"""
    service = ProductService(db)
    deleted = await service.delete_sku(sku_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="SKU不存在")
    return {"message": "SKU删除成功"}


# 价格相关接口
@router.post("/skus/{sku_id}/prices", response_model=ProductPrice)
async def create_price(
    sku_id: int,
    price: ProductPriceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """为SKU创建价格"""
    service = ProductService(db)
    return await service.create_price(sku_id, price)

@router.get("/skus/{sku_id}/prices", response_model=List[ProductPrice])
async def get_prices(
    sku_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取SKU的价格列表"""
    service = ProductService(db)
    return await service.get_prices_by_sku(sku_id)

@router.put("/prices/{price_id}", response_model=ProductPrice)
async def update_price(
    price_id: int,
    price: ProductPriceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新价格"""
    service = ProductService(db)
    updated_price = await service.update_price(price_id, price)
    if not updated_price:
        raise HTTPException(status_code=404, detail="价格不存在")
    return updated_price

@router.delete("/prices/{price_id}")
async def delete_price(
    price_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除价格"""
    service = ProductService(db)
    deleted = await service.delete_price(price_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="价格不存在")
    return {"message": "价格删除成功"}


# 属性相关接口
@router.post("/{product_id}/attributes", response_model=ProductAttribute)
async def create_attribute(
    product_id: int,
    attribute: ProductAttributeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """为商品创建属性"""
    service = ProductService(db)
    return await service.create_attribute(product_id, attribute)

@router.get("/{product_id}/attributes", response_model=List[ProductAttribute])
async def get_attributes(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取商品的属性列表"""
    service = ProductService(db)
    return await service.get_attributes_by_product(product_id)

@router.delete("/attributes/{attribute_id}")
async def delete_attribute(
    attribute_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除商品属性"""
    service = ProductService(db)
    deleted = await service.delete_attribute(attribute_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="属性不存在")
    return {"message": "属性删除成功"}
