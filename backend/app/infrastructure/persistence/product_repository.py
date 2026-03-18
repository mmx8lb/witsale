from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import selectinload

from app.models.product import Category, Product, ProductSKU, ProductPrice, ProductAttribute


class ProductRepository:
    """商品管理数据库操作类"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # 分类相关操作
    async def create_category(self, name: str, parent_id: Optional[int] = None, level: int = 1, sort: int = 0) -> Category:
        """创建分类"""
        category = Category(
            name=name,
            parent_id=parent_id,
            level=level,
            sort=sort
        )
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category
    
    async def get_category(self, category_id: int) -> Optional[Category]:
        """获取分类详情"""
        result = await self.db.execute(select(Category).where(Category.id == category_id))
        return result.scalar_one_or_none()
    
    async def get_categories(self, parent_id: Optional[int] = None, is_active: Optional[bool] = None) -> List[Category]:
        """获取分类列表"""
        query = select(Category)
        if parent_id is not None:
            query = query.where(Category.parent_id == parent_id)
        if is_active is not None:
            query = query.where(Category.is_active == is_active)
        query = query.order_by(Category.sort, Category.id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_category(self, category_id: int, **kwargs) -> Optional[Category]:
        """更新分类"""
        category = await self.get_category(category_id)
        if not category:
            return None
        for key, value in kwargs.items():
            if hasattr(category, key):
                setattr(category, key, value)
        await self.db.commit()
        await self.db.refresh(category)
        return category
    
    async def delete_category(self, category_id: int) -> bool:
        """删除分类"""
        result = await self.db.execute(delete(Category).where(Category.id == category_id))
        await self.db.commit()
        return result.rowcount > 0
    
    # 商品相关操作
    async def create_product(self, name: str, category_id: int, **kwargs) -> Product:
        """创建商品"""
        product = Product(
            name=name,
            category_id=category_id,
            **kwargs
        )
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product
    
    async def get_product(self, product_id: int) -> Optional[Product]:
        """获取商品详情"""
        result = await self.db.execute(
            select(Product)
            .options(selectinload(Product.skus).selectinload(ProductSKU.prices))
            .where(Product.id == product_id)
        )
        return result.scalar_one_or_none()
    
    async def get_products(self, category_id: Optional[int] = None, is_active: Optional[bool] = None, skip: int = 0, limit: int = 100) -> List[Product]:
        """获取商品列表"""
        query = select(Product)
        if category_id is not None:
            query = query.where(Product.category_id == category_id)
        if is_active is not None:
            query = query.where(Product.is_active == is_active)
        query = query.order_by(Product.id.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_product(self, product_id: int, **kwargs) -> Optional[Product]:
        """更新商品"""
        product = await self.get_product(product_id)
        if not product:
            return None
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
        await self.db.commit()
        await self.db.refresh(product)
        return product
    
    async def delete_product(self, product_id: int) -> bool:
        """删除商品"""
        result = await self.db.execute(delete(Product).where(Product.id == product_id))
        await self.db.commit()
        return result.rowcount > 0
    
    # SKU相关操作
    async def create_sku(self, product_id: int, sku_code: str, attributes: Dict[str, Any], stock: int = 0) -> ProductSKU:
        """创建SKU"""
        sku = ProductSKU(
            product_id=product_id,
            sku_code=sku_code,
            attributes=attributes,
            stock=stock
        )
        self.db.add(sku)
        await self.db.commit()
        await self.db.refresh(sku)
        return sku
    
    async def get_sku(self, sku_id: int) -> Optional[ProductSKU]:
        """获取SKU详情"""
        result = await self.db.execute(
            select(ProductSKU)
            .options(selectinload(ProductSKU.prices))
            .where(ProductSKU.id == sku_id)
        )
        return result.scalar_one_or_none()
    
    async def get_skus_by_product(self, product_id: int) -> List[ProductSKU]:
        """获取商品的所有SKU"""
        result = await self.db.execute(
            select(ProductSKU)
            .options(selectinload(ProductSKU.prices))
            .where(ProductSKU.product_id == product_id)
        )
        return result.scalars().all()
    
    async def update_sku(self, sku_id: int, **kwargs) -> Optional[ProductSKU]:
        """更新SKU"""
        sku = await self.get_sku(sku_id)
        if not sku:
            return None
        for key, value in kwargs.items():
            if hasattr(sku, key):
                setattr(sku, key, value)
        await self.db.commit()
        await self.db.refresh(sku)
        return sku
    
    async def delete_sku(self, sku_id: int) -> bool:
        """删除SKU"""
        result = await self.db.execute(delete(ProductSKU).where(ProductSKU.id == sku_id))
        await self.db.commit()
        return result.rowcount > 0
    
    # 价格相关操作
    async def create_price(self, sku_id: int, price_type: str, price: float, min_quantity: int = 1, max_quantity: Optional[int] = None) -> ProductPrice:
        """创建价格"""
        product_price = ProductPrice(
            sku_id=sku_id,
            price_type=price_type,
            price=price,
            min_quantity=min_quantity,
            max_quantity=max_quantity
        )
        self.db.add(product_price)
        await self.db.commit()
        await self.db.refresh(product_price)
        return product_price
    
    async def get_prices_by_sku(self, sku_id: int) -> List[ProductPrice]:
        """获取SKU的所有价格"""
        result = await self.db.execute(
            select(ProductPrice)
            .where(ProductPrice.sku_id == sku_id)
            .order_by(ProductPrice.min_quantity)
        )
        return result.scalars().all()
    
    async def update_price(self, price_id: int, **kwargs) -> Optional[ProductPrice]:
        """更新价格"""
        result = await self.db.execute(select(ProductPrice).where(ProductPrice.id == price_id))
        price = result.scalar_one_or_none()
        if not price:
            return None
        for key, value in kwargs.items():
            if hasattr(price, key):
                setattr(price, key, value)
        await self.db.commit()
        await self.db.refresh(price)
        return price
    
    async def delete_price(self, price_id: int) -> bool:
        """删除价格"""
        result = await self.db.execute(delete(ProductPrice).where(ProductPrice.id == price_id))
        await self.db.commit()
        return result.rowcount > 0
    
    # 属性相关操作
    async def create_attribute(self, product_id: int, name: str, value: str) -> ProductAttribute:
        """创建商品属性"""
        attribute = ProductAttribute(
            product_id=product_id,
            name=name,
            value=value
        )
        self.db.add(attribute)
        await self.db.commit()
        await self.db.refresh(attribute)
        return attribute
    
    async def get_attributes_by_product(self, product_id: int) -> List[ProductAttribute]:
        """获取商品的所有属性"""
        result = await self.db.execute(
            select(ProductAttribute)
            .where(ProductAttribute.product_id == product_id)
        )
        return result.scalars().all()
    
    async def delete_attribute(self, attribute_id: int) -> bool:
        """删除商品属性"""
        result = await self.db.execute(delete(ProductAttribute).where(ProductAttribute.id == attribute_id))
        await self.db.commit()
        return result.rowcount > 0
