from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.product_repository import ProductRepository
from app.schemas.product import (
    CategoryCreate, CategoryUpdate, Category,
    ProductCreate, ProductUpdate, Product,
    ProductSKUCreate, ProductSKUUpdate, ProductSKU,
    ProductPriceCreate, ProductPriceUpdate, ProductPrice,
    ProductAttributeCreate, ProductAttribute
)


class ProductService:
    """商品管理服务层"""
    
    def __init__(self, db: AsyncSession):
        self.repository = ProductRepository(db)
    
    # 分类相关服务
    async def create_category(self, category_data: CategoryCreate) -> Category:
        """创建分类"""
        category = await self.repository.create_category(
            name=category_data.name,
            parent_id=category_data.parent_id,
            level=category_data.level,
            sort=category_data.sort
        )
        return Category.model_validate(category)
    
    async def get_category(self, category_id: int) -> Optional[Category]:
        """获取分类详情"""
        category = await self.repository.get_category(category_id)
        if not category:
            return None
        return Category.model_validate(category)
    
    async def get_categories(self, parent_id: Optional[int] = None, is_active: Optional[bool] = None) -> List[Category]:
        """获取分类列表"""
        categories = await self.repository.get_categories(parent_id, is_active)
        return [Category.model_validate(category) for category in categories]
    
    async def update_category(self, category_id: int, category_data: CategoryUpdate) -> Optional[Category]:
        """更新分类"""
        update_data = category_data.model_dump(exclude_unset=True)
        category = await self.repository.update_category(category_id, **update_data)
        if not category:
            return None
        return Category.model_validate(category)
    
    async def delete_category(self, category_id: int) -> bool:
        """删除分类"""
        return await self.repository.delete_category(category_id)
    
    # 商品相关服务
    async def create_product(self, product_data: ProductCreate) -> Product:
        """创建商品"""
        product = await self.repository.create_product(
            name=product_data.name,
            category_id=product_data.category_id,
            description=product_data.description,
            brand=product_data.brand,
            model=product_data.model,
            is_active=product_data.is_active
        )
        return Product.model_validate(product)
    
    async def get_product(self, product_id: int) -> Optional[Product]:
        """获取商品详情"""
        product = await self.repository.get_product(product_id)
        if not product:
            return None
        return Product.model_validate(product)
    
    async def get_products(self, category_id: Optional[int] = None, is_active: Optional[bool] = None, skip: int = 0, limit: int = 100) -> List[Product]:
        """获取商品列表"""
        products = await self.repository.get_products(category_id, is_active, skip, limit)
        return [Product.model_validate(product) for product in products]
    
    async def update_product(self, product_id: int, product_data: ProductUpdate) -> Optional[Product]:
        """更新商品"""
        update_data = product_data.model_dump(exclude_unset=True)
        product = await self.repository.update_product(product_id, **update_data)
        if not product:
            return None
        return Product.model_validate(product)
    
    async def delete_product(self, product_id: int) -> bool:
        """删除商品"""
        return await self.repository.delete_product(product_id)
    
    # SKU相关服务
    async def create_sku(self, product_id: int, sku_data: ProductSKUCreate) -> ProductSKU:
        """创建SKU"""
        sku = await self.repository.create_sku(
            product_id=product_id,
            sku_code=sku_data.sku_code,
            attributes=sku_data.attributes,
            stock=sku_data.stock
        )
        return ProductSKU.model_validate(sku)
    
    async def get_sku(self, sku_id: int) -> Optional[ProductSKU]:
        """获取SKU详情"""
        sku = await self.repository.get_sku(sku_id)
        if not sku:
            return None
        return ProductSKU.model_validate(sku)
    
    async def get_skus_by_product(self, product_id: int) -> List[ProductSKU]:
        """获取商品的所有SKU"""
        skus = await self.repository.get_skus_by_product(product_id)
        return [ProductSKU.model_validate(sku) for sku in skus]
    
    async def update_sku(self, sku_id: int, sku_data: ProductSKUUpdate) -> Optional[ProductSKU]:
        """更新SKU"""
        update_data = sku_data.model_dump(exclude_unset=True)
        sku = await self.repository.update_sku(sku_id, **update_data)
        if not sku:
            return None
        return ProductSKU.model_validate(sku)
    
    async def delete_sku(self, sku_id: int) -> bool:
        """删除SKU"""
        return await self.repository.delete_sku(sku_id)
    
    # 价格相关服务
    async def create_price(self, sku_id: int, price_data: ProductPriceCreate) -> ProductPrice:
        """创建价格"""
        price = await self.repository.create_price(
            sku_id=sku_id,
            price_type=price_data.price_type,
            price=price_data.price,
            min_quantity=price_data.min_quantity,
            max_quantity=price_data.max_quantity
        )
        return ProductPrice.model_validate(price)
    
    async def get_prices_by_sku(self, sku_id: int) -> List[ProductPrice]:
        """获取SKU的所有价格"""
        prices = await self.repository.get_prices_by_sku(sku_id)
        return [ProductPrice.model_validate(price) for price in prices]
    
    async def update_price(self, price_id: int, price_data: ProductPriceUpdate) -> Optional[ProductPrice]:
        """更新价格"""
        update_data = price_data.model_dump(exclude_unset=True)
        price = await self.repository.update_price(price_id, **update_data)
        if not price:
            return None
        return ProductPrice.model_validate(price)
    
    async def delete_price(self, price_id: int) -> bool:
        """删除价格"""
        return await self.repository.delete_price(price_id)
    
    # 属性相关服务
    async def create_attribute(self, product_id: int, attribute_data: ProductAttributeCreate) -> ProductAttribute:
        """创建商品属性"""
        attribute = await self.repository.create_attribute(
            product_id=product_id,
            name=attribute_data.name,
            value=attribute_data.value
        )
        return ProductAttribute.model_validate(attribute)
    
    async def get_attributes_by_product(self, product_id: int) -> List[ProductAttribute]:
        """获取商品的所有属性"""
        attributes = await self.repository.get_attributes_by_product(product_id)
        return [ProductAttribute.model_validate(attribute) for attribute in attributes]
    
    async def delete_attribute(self, attribute_id: int) -> bool:
        """删除商品属性"""
        return await self.repository.delete_attribute(attribute_id)
