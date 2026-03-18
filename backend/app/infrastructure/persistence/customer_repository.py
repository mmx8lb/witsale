from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import selectinload
from datetime import datetime

from app.models.customer import (
    CustomerCategory, CustomerLevel, Customer, 
    CustomerContact, CustomerAddress, CustomerTag
)


class CustomerRepository:
    """客户管理数据库操作类"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # 客户分类相关操作
    async def create_customer_category(self, **kwargs) -> CustomerCategory:
        """创建客户分类"""
        category = CustomerCategory(**kwargs)
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category
    
    async def get_customer_category(self, category_id: int) -> Optional[CustomerCategory]:
        """获取客户分类详情"""
        result = await self.db.execute(
            select(CustomerCategory)
            .options(selectinload(CustomerCategory.children))
            .where(CustomerCategory.id == category_id)
        )
        return result.scalar_one_or_none()
    
    async def get_customer_categories(self, parent_category_id: Optional[int] = None, 
                                    is_active: Optional[bool] = None) -> List[CustomerCategory]:
        """获取客户分类列表"""
        query = select(CustomerCategory)
        if parent_category_id is not None:
            query = query.where(CustomerCategory.parent_category_id == parent_category_id)
        if is_active is not None:
            query = query.where(CustomerCategory.is_active == is_active)
        query = query.order_by(CustomerCategory.level, CustomerCategory.id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_customer_category(self, category_id: int, **kwargs) -> Optional[CustomerCategory]:
        """更新客户分类"""
        category = await self.get_customer_category(category_id)
        if not category:
            return None
        for key, value in kwargs.items():
            if hasattr(category, key):
                setattr(category, key, value)
        await self.db.commit()
        await self.db.refresh(category)
        return category
    
    async def delete_customer_category(self, category_id: int) -> bool:
        """删除客户分类"""
        result = await self.db.execute(
            delete(CustomerCategory).where(CustomerCategory.id == category_id)
        )
        await self.db.commit()
        return result.rowcount > 0
    
    # 客户等级相关操作
    async def create_customer_level(self, **kwargs) -> CustomerLevel:
        """创建客户等级"""
        level = CustomerLevel(**kwargs)
        self.db.add(level)
        await self.db.commit()
        await self.db.refresh(level)
        return level
    
    async def get_customer_level(self, level_id: int) -> Optional[CustomerLevel]:
        """获取客户等级详情"""
        result = await self.db.execute(
            select(CustomerLevel).where(CustomerLevel.id == level_id)
        )
        return result.scalar_one_or_none()
    
    async def get_customer_levels(self, is_active: Optional[bool] = None) -> List[CustomerLevel]:
        """获取客户等级列表"""
        query = select(CustomerLevel)
        if is_active is not None:
            query = query.where(CustomerLevel.is_active == is_active)
        query = query.order_by(CustomerLevel.priority.desc(), CustomerLevel.id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_customer_level(self, level_id: int, **kwargs) -> Optional[CustomerLevel]:
        """更新客户等级"""
        level = await self.get_customer_level(level_id)
        if not level:
            return None
        for key, value in kwargs.items():
            if hasattr(level, key):
                setattr(level, key, value)
        await self.db.commit()
        await self.db.refresh(level)
        return level
    
    async def delete_customer_level(self, level_id: int) -> bool:
        """删除客户等级"""
        result = await self.db.execute(
            delete(CustomerLevel).where(CustomerLevel.id == level_id)
        )
        await self.db.commit()
        return result.rowcount > 0
    
    # 客户标签相关操作
    async def create_customer_tag(self, **kwargs) -> CustomerTag:
        """创建客户标签"""
        tag = CustomerTag(**kwargs)
        self.db.add(tag)
        await self.db.commit()
        await self.db.refresh(tag)
        return tag
    
    async def get_customer_tag(self, tag_id: int) -> Optional[CustomerTag]:
        """获取客户标签详情"""
        result = await self.db.execute(
            select(CustomerTag).where(CustomerTag.id == tag_id)
        )
        return result.scalar_one_or_none()
    
    async def get_customer_tags(self, is_active: Optional[bool] = None) -> List[CustomerTag]:
        """获取客户标签列表"""
        query = select(CustomerTag)
        if is_active is not None:
            query = query.where(CustomerTag.is_active == is_active)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_customer_tag(self, tag_id: int, **kwargs) -> Optional[CustomerTag]:
        """更新客户标签"""
        tag = await self.get_customer_tag(tag_id)
        if not tag:
            return None
        for key, value in kwargs.items():
            if hasattr(tag, key):
                setattr(tag, key, value)
        await self.db.commit()
        await self.db.refresh(tag)
        return tag
    
    async def delete_customer_tag(self, tag_id: int) -> bool:
        """删除客户标签"""
        result = await self.db.execute(
            delete(CustomerTag).where(CustomerTag.id == tag_id)
        )
        await self.db.commit()
        return result.rowcount > 0
    
    # 客户相关操作
    async def create_customer(self, **kwargs) -> Customer:
        """创建客户"""
        # 处理联系人、地址和标签
        contacts_data = kwargs.pop('contacts', [])
        addresses_data = kwargs.pop('addresses', [])
        tag_ids = kwargs.pop('tag_ids', [])
        
        customer = Customer(**kwargs)
        self.db.add(customer)
        await self.db.flush()
        
        # 创建联系人
        for contact_data in contacts_data:
            contact = CustomerContact(customer_id=customer.id, **contact_data)
            self.db.add(contact)
        
        # 创建地址
        for address_data in addresses_data:
            address = CustomerAddress(customer_id=customer.id, **address_data)
            self.db.add(address)
        
        # 添加标签
        if tag_ids:
            tags = await self.db.execute(
                select(CustomerTag).where(CustomerTag.id.in_(tag_ids))
            )
            customer.tags = tags.scalars().all()
        
        await self.db.commit()
        await self.db.refresh(customer)
        return customer
    
    async def get_customer(self, customer_id: int) -> Optional[Customer]:
        """获取客户详情"""
        result = await self.db.execute(
            select(Customer)
            .options(
                selectinload(Customer.category),
                selectinload(Customer.level),
                selectinload(Customer.contacts),
                selectinload(Customer.addresses),
                selectinload(Customer.tags)
            )
            .where(Customer.id == customer_id)
        )
        return result.scalar_one_or_none()
    
    async def get_customers(self, 
                          category_id: Optional[int] = None,
                          level_id: Optional[int] = None,
                          status: Optional[str] = None,
                          is_active: Optional[bool] = None,
                          skip: int = 0,
                          limit: int = 100) -> List[Customer]:
        """获取客户列表"""
        query = select(Customer)
        if category_id is not None:
            query = query.where(Customer.category_id == category_id)
        if level_id is not None:
            query = query.where(Customer.level_id == level_id)
        if status is not None:
            query = query.where(Customer.status == status)
        if is_active is not None:
            query = query.where(Customer.is_active == is_active)
        query = query.options(
            selectinload(Customer.category),
            selectinload(Customer.level)
        )
        query = query.order_by(Customer.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_customer(self, customer_id: int, **kwargs) -> Optional[Customer]:
        """更新客户"""
        customer = await self.get_customer(customer_id)
        if not customer:
            return None
        
        for key, value in kwargs.items():
            if hasattr(customer, key):
                setattr(customer, key, value)
        
        await self.db.commit()
        await self.db.refresh(customer)
        return customer
    
    async def update_customer_tags(self, customer_id: int, tag_ids: List[int]) -> Optional[Customer]:
        """更新客户标签"""
        customer = await self.get_customer(customer_id)
        if not customer:
            return None
        
        tags = await self.db.execute(
            select(CustomerTag).where(CustomerTag.id.in_(tag_ids))
        )
        customer.tags = tags.scalars().all()
        
        await self.db.commit()
        await self.db.refresh(customer)
        return customer
    
    async def delete_customer(self, customer_id: int) -> bool:
        """删除客户"""
        result = await self.db.execute(
            delete(Customer).where(Customer.id == customer_id)
        )
        await self.db.commit()
        return result.rowcount > 0
    
    # 客户联系人相关操作
    async def create_customer_contact(self, customer_id: int, **kwargs) -> CustomerContact:
        """创建客户联系人"""
        contact = CustomerContact(customer_id=customer_id, **kwargs)
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact
    
    async def get_customer_contact(self, contact_id: int) -> Optional[CustomerContact]:
        """获取客户联系人详情"""
        result = await self.db.execute(
            select(CustomerContact).where(CustomerContact.id == contact_id)
        )
        return result.scalar_one_or_none()
    
    async def get_customer_contacts(self, customer_id: int) -> List[CustomerContact]:
        """获取客户联系人列表"""
        result = await self.db.execute(
            select(CustomerContact)
            .where(CustomerContact.customer_id == customer_id)
            .order_by(CustomerContact.is_primary.desc(), CustomerContact.id)
        )
        return result.scalars().all()
    
    async def update_customer_contact(self, contact_id: int, **kwargs) -> Optional[CustomerContact]:
        """更新客户联系人"""
        contact = await self.get_customer_contact(contact_id)
        if not contact:
            return None
        
        for key, value in kwargs.items():
            if hasattr(contact, key):
                setattr(contact, key, value)
        
        await self.db.commit()
        await self.db.refresh(contact)
        return contact
    
    async def delete_customer_contact(self, contact_id: int) -> bool:
        """删除客户联系人"""
        result = await self.db.execute(
            delete(CustomerContact).where(CustomerContact.id == contact_id)
        )
        await self.db.commit()
        return result.rowcount > 0
    
    # 客户地址相关操作
    async def create_customer_address(self, customer_id: int, **kwargs) -> CustomerAddress:
        """创建客户地址"""
        address = CustomerAddress(customer_id=customer_id, **kwargs)
        self.db.add(address)
        await self.db.commit()
        await self.db.refresh(address)
        return address
    
    async def get_customer_address(self, address_id: int) -> Optional[CustomerAddress]:
        """获取客户地址详情"""
        result = await self.db.execute(
            select(CustomerAddress).where(CustomerAddress.id == address_id)
        )
        return result.scalar_one_or_none()
    
    async def get_customer_addresses(self, customer_id: int, 
                                   address_type: Optional[str] = None,
                                   is_active: Optional[bool] = None) -> List[CustomerAddress]:
        """获取客户地址列表"""
        query = select(CustomerAddress).where(CustomerAddress.customer_id == customer_id)
        if address_type is not None:
            query = query.where(CustomerAddress.type == address_type)
        if is_active is not None:
            query = query.where(CustomerAddress.is_active == is_active)
        query = query.order_by(CustomerAddress.is_default.desc(), CustomerAddress.id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_customer_address(self, address_id: int, **kwargs) -> Optional[CustomerAddress]:
        """更新客户地址"""
        address = await self.get_customer_address(address_id)
        if not address:
            return None
        
        for key, value in kwargs.items():
            if hasattr(address, key):
                setattr(address, key, value)
        
        await self.db.commit()
        await self.db.refresh(address)
        return address
    
    async def delete_customer_address(self, address_id: int) -> bool:
        """删除客户地址"""
        result = await self.db.execute(
            delete(CustomerAddress).where(CustomerAddress.id == address_id)
        )
        await self.db.commit()
        return result.rowcount > 0
