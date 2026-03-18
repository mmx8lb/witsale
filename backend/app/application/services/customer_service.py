from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.infrastructure.persistence.customer_repository import CustomerRepository
from app.schemas.customer import (
    CustomerCategoryCreate, CustomerCategoryUpdate, CustomerCategory,
    CustomerLevelCreate, CustomerLevelUpdate, CustomerLevel,
    CustomerCreate, CustomerUpdate, Customer, CustomerUpdateTags,
    CustomerContactCreate, CustomerContactUpdate, CustomerContact,
    CustomerAddressCreate, CustomerAddressUpdate, CustomerAddress,
    CustomerTagCreate, CustomerTagUpdate, CustomerTag
)


class CustomerService:
    """客户管理服务层"""
    
    def __init__(self, db: AsyncSession):
        self.repository = CustomerRepository(db)
    
    # 客户分类相关服务
    async def create_customer_category(self, category_data: CustomerCategoryCreate) -> CustomerCategory:
        """创建客户分类"""
        category_dict = category_data.model_dump()
        category = await self.repository.create_customer_category(**category_dict)
        # 只选择基本字段，避免children关系的异步加载问题
        category_data = {
            "id": category.id,
            "name": category.name,
            "code": category.code,
            "description": category.description,
            "parent_category_id": category.parent_category_id,
            "level": category.level,
            "is_active": category.is_active,
            "created_at": category.created_at,
            "updated_at": category.updated_at
        }
        return CustomerCategory(**category_data)
    
    async def get_customer_category(self, category_id: int) -> Optional[CustomerCategory]:
        """获取客户分类详情"""
        category = await self.repository.get_customer_category(category_id)
        if not category:
            return None
        # 只选择基本字段，避免children关系的异步加载问题
        category_data = {
            "id": category.id,
            "name": category.name,
            "code": category.code,
            "description": category.description,
            "parent_category_id": category.parent_category_id,
            "level": category.level,
            "is_active": category.is_active,
            "created_at": category.created_at,
            "updated_at": category.updated_at
        }
        return CustomerCategory(**category_data)
    
    async def get_customer_categories(self, parent_category_id: Optional[int] = None, 
                                    is_active: Optional[bool] = None) -> List[CustomerCategory]:
        """获取客户分类列表"""
        categories = await self.repository.get_customer_categories(parent_category_id, is_active)
        result = []
        for category in categories:
            # 只选择基本字段，避免children关系的异步加载问题
            category_data = {
                "id": category.id,
                "name": category.name,
                "code": category.code,
                "description": category.description,
                "parent_category_id": category.parent_category_id,
                "level": category.level,
                "is_active": category.is_active,
                "created_at": category.created_at,
                "updated_at": category.updated_at
            }
            result.append(CustomerCategory(**category_data))
        return result
    
    async def update_customer_category(self, category_id: int, category_data: CustomerCategoryUpdate) -> Optional[CustomerCategory]:
        """更新客户分类"""
        update_data = category_data.model_dump(exclude_unset=True)
        category = await self.repository.update_customer_category(category_id, **update_data)
        if not category:
            return None
        # 只选择基本字段，避免children关系的异步加载问题
        category_data = {
            "id": category.id,
            "name": category.name,
            "code": category.code,
            "description": category.description,
            "parent_category_id": category.parent_category_id,
            "level": category.level,
            "is_active": category.is_active,
            "created_at": category.created_at,
            "updated_at": category.updated_at
        }
        return CustomerCategory(**category_data)
    
    async def delete_customer_category(self, category_id: int) -> bool:
        """删除客户分类"""
        return await self.repository.delete_customer_category(category_id)
    
    # 客户等级相关服务
    async def create_customer_level(self, level_data: CustomerLevelCreate) -> CustomerLevel:
        """创建客户等级"""
        level_dict = level_data.model_dump()
        level = await self.repository.create_customer_level(**level_dict)
        return CustomerLevel.model_validate(level)
    
    async def get_customer_level(self, level_id: int) -> Optional[CustomerLevel]:
        """获取客户等级详情"""
        level = await self.repository.get_customer_level(level_id)
        if not level:
            return None
        return CustomerLevel.model_validate(level)
    
    async def get_customer_levels(self, is_active: Optional[bool] = None) -> List[CustomerLevel]:
        """获取客户等级列表"""
        levels = await self.repository.get_customer_levels(is_active)
        return [CustomerLevel.model_validate(level) for level in levels]
    
    async def update_customer_level(self, level_id: int, level_data: CustomerLevelUpdate) -> Optional[CustomerLevel]:
        """更新客户等级"""
        update_data = level_data.model_dump(exclude_unset=True)
        level = await self.repository.update_customer_level(level_id, **update_data)
        if not level:
            return None
        return CustomerLevel.model_validate(level)
    
    async def delete_customer_level(self, level_id: int) -> bool:
        """删除客户等级"""
        return await self.repository.delete_customer_level(level_id)
    
    # 客户标签相关服务
    async def create_customer_tag(self, tag_data: CustomerTagCreate) -> CustomerTag:
        """创建客户标签"""
        tag_dict = tag_data.model_dump()
        tag = await self.repository.create_customer_tag(**tag_dict)
        return CustomerTag.model_validate(tag)
    
    async def get_customer_tag(self, tag_id: int) -> Optional[CustomerTag]:
        """获取客户标签详情"""
        tag = await self.repository.get_customer_tag(tag_id)
        if not tag:
            return None
        return CustomerTag.model_validate(tag)
    
    async def get_customer_tags(self, is_active: Optional[bool] = None) -> List[CustomerTag]:
        """获取客户标签列表"""
        tags = await self.repository.get_customer_tags(is_active)
        return [CustomerTag.model_validate(tag) for tag in tags]
    
    async def update_customer_tag(self, tag_id: int, tag_data: CustomerTagUpdate) -> Optional[CustomerTag]:
        """更新客户标签"""
        update_data = tag_data.model_dump(exclude_unset=True)
        tag = await self.repository.update_customer_tag(tag_id, **update_data)
        if not tag:
            return None
        return CustomerTag.model_validate(tag)
    
    async def delete_customer_tag(self, tag_id: int) -> bool:
        """删除客户标签"""
        return await self.repository.delete_customer_tag(tag_id)
    
    # 客户相关服务
    async def create_customer(self, customer_data: CustomerCreate) -> Customer:
        """创建客户"""
        # 处理联系人、地址和标签
        customer_dict = customer_data.model_dump()
        contacts_data = customer_dict.pop('contacts', [])
        addresses_data = customer_dict.pop('addresses', [])
        tag_ids = customer_dict.pop('tag_ids', [])
        
        # 初始化客户统计数据
        customer_dict['total_spend'] = 0.0
        customer_dict['total_orders'] = 0
        customer_dict['credit_balance'] = 0.0
        
        # 创建客户
        customer = await self.repository.create_customer(
            **customer_dict,
            contacts=contacts_data,
            addresses=addresses_data,
            tag_ids=tag_ids
        )
        
        # 自动调整客户等级
        await self.adjust_customer_level(customer.id)
        
        # 只选择基本字段，避免关联关系的异步加载问题
        customer_data = {
            "id": customer.id,
            "name": customer.name,
            "code": customer.code,
            "short_name": customer.short_name,
            "type": customer.type,
            "category_id": customer.category_id,
            "level_id": customer.level_id,
            "contact_name": customer.contact_name,
            "contact_phone": customer.contact_phone,
            "email": customer.email,
            "website": customer.website,
            "tax_no": customer.tax_no,
            "registered_capital": customer.registered_capital,
            "business_scope": customer.business_scope,
            "founding_date": customer.founding_date,
            "status": customer.status,
            "total_spend": customer.total_spend,
            "total_orders": customer.total_orders,
            "credit_limit": customer.credit_limit,
            "credit_balance": customer.credit_balance,
            "remark": customer.remark,
            "is_active": customer.is_active,
            "created_at": customer.created_at,
            "updated_at": customer.updated_at,
            "category": None,
            "level": None,
            "contacts": [],
            "addresses": [],
            "tags": []
        }
        return Customer(**customer_data)
    
    async def get_customer(self, customer_id: int) -> Optional[Customer]:
        """获取客户详情"""
        customer = await self.repository.get_customer(customer_id)
        if not customer:
            return None
        # 只选择基本字段，避免关联关系的异步加载问题
        customer_data = {
            "id": customer.id,
            "name": customer.name,
            "code": customer.code,
            "short_name": customer.short_name,
            "type": customer.type,
            "category_id": customer.category_id,
            "level_id": customer.level_id,
            "contact_name": customer.contact_name,
            "contact_phone": customer.contact_phone,
            "email": customer.email,
            "website": customer.website,
            "tax_no": customer.tax_no,
            "registered_capital": customer.registered_capital,
            "business_scope": customer.business_scope,
            "founding_date": customer.founding_date,
            "status": customer.status,
            "total_spend": customer.total_spend,
            "total_orders": customer.total_orders,
            "credit_limit": customer.credit_limit,
            "credit_balance": customer.credit_balance,
            "remark": customer.remark,
            "is_active": customer.is_active,
            "created_at": customer.created_at,
            "updated_at": customer.updated_at,
            "category": None,
            "level": None,
            "contacts": [],
            "addresses": [],
            "tags": []
        }
        return Customer(**customer_data)
    
    async def get_customers(self, 
                          category_id: Optional[int] = None,
                          level_id: Optional[int] = None,
                          status: Optional[str] = None,
                          is_active: Optional[bool] = None,
                          skip: int = 0,
                          limit: int = 100) -> List[Customer]:
        """获取客户列表"""
        customers = await self.repository.get_customers(
            category_id=category_id,
            level_id=level_id,
            status=status,
            is_active=is_active,
            skip=skip,
            limit=limit
        )
        result = []
        for customer in customers:
            # 只选择基本字段，避免关联关系的异步加载问题
            customer_data = {
                "id": customer.id,
                "name": customer.name,
                "code": customer.code,
                "short_name": customer.short_name,
                "type": customer.type,
                "category_id": customer.category_id,
                "level_id": customer.level_id,
                "contact_name": customer.contact_name,
                "contact_phone": customer.contact_phone,
                "email": customer.email,
                "website": customer.website,
                "tax_no": customer.tax_no,
                "registered_capital": customer.registered_capital,
                "business_scope": customer.business_scope,
                "founding_date": customer.founding_date,
                "status": customer.status,
                "total_spend": customer.total_spend,
                "total_orders": customer.total_orders,
                "credit_limit": customer.credit_limit,
                "credit_balance": customer.credit_balance,
                "remark": customer.remark,
                "is_active": customer.is_active,
                "created_at": customer.created_at,
                "updated_at": customer.updated_at,
                "category": None,
                "level": None,
                "contacts": [],
                "addresses": [],
                "tags": []
            }
            result.append(Customer(**customer_data))
        return result
    
    async def update_customer(self, customer_id: int, customer_data: CustomerUpdate) -> Optional[Customer]:
        """更新客户"""
        update_data = customer_data.model_dump(exclude_unset=True)
        customer = await self.repository.update_customer(customer_id, **update_data)
        if not customer:
            return None
        
        # 自动调整客户等级
        await self.adjust_customer_level(customer_id)
        
        # 只选择基本字段，避免关联关系的异步加载问题
        customer_data = {
            "id": customer.id,
            "name": customer.name,
            "code": customer.code,
            "short_name": customer.short_name,
            "type": customer.type,
            "category_id": customer.category_id,
            "level_id": customer.level_id,
            "contact_name": customer.contact_name,
            "contact_phone": customer.contact_phone,
            "email": customer.email,
            "website": customer.website,
            "tax_no": customer.tax_no,
            "registered_capital": customer.registered_capital,
            "business_scope": customer.business_scope,
            "founding_date": customer.founding_date,
            "status": customer.status,
            "total_spend": customer.total_spend,
            "total_orders": customer.total_orders,
            "credit_limit": customer.credit_limit,
            "credit_balance": customer.credit_balance,
            "remark": customer.remark,
            "is_active": customer.is_active,
            "created_at": customer.created_at,
            "updated_at": customer.updated_at,
            "category": None,
            "level": None,
            "contacts": [],
            "addresses": [],
            "tags": []
        }
        return Customer(**customer_data)
    
    async def update_customer_tags(self, customer_id: int, tags_data: CustomerUpdateTags) -> Optional[Customer]:
        """更新客户标签"""
        customer = await self.repository.update_customer_tags(customer_id, tags_data.tag_ids)
        if not customer:
            return None
        # 只选择基本字段，避免关联关系的异步加载问题
        customer_data = {
            "id": customer.id,
            "name": customer.name,
            "code": customer.code,
            "short_name": customer.short_name,
            "type": customer.type,
            "category_id": customer.category_id,
            "level_id": customer.level_id,
            "contact_name": customer.contact_name,
            "contact_phone": customer.contact_phone,
            "email": customer.email,
            "website": customer.website,
            "tax_no": customer.tax_no,
            "registered_capital": customer.registered_capital,
            "business_scope": customer.business_scope,
            "founding_date": customer.founding_date,
            "status": customer.status,
            "total_spend": customer.total_spend,
            "total_orders": customer.total_orders,
            "credit_limit": customer.credit_limit,
            "credit_balance": customer.credit_balance,
            "remark": customer.remark,
            "is_active": customer.is_active,
            "created_at": customer.created_at,
            "updated_at": customer.updated_at,
            "category": None,
            "level": None,
            "contacts": [],
            "addresses": [],
            "tags": []
        }
        return Customer(**customer_data)
    
    async def delete_customer(self, customer_id: int) -> bool:
        """删除客户"""
        return await self.repository.delete_customer(customer_id)
    
    async def adjust_customer_level(self, customer_id: int) -> Optional[Customer]:
        """根据客户消费自动调整客户等级"""
        customer = await self.repository.get_customer(customer_id)
        if not customer:
            return None
        
        # 获取所有活跃的客户等级
        levels = await self.repository.get_customer_levels(is_active=True)
        
        # 找到适合的客户等级
        suitable_level = None
        for level in sorted(levels, key=lambda x: x.min_spend, reverse=True):
            if customer.total_spend >= level.min_spend:
                suitable_level = level
                break
        
        # 如果找到适合的等级且与当前等级不同，则更新
        if suitable_level and (customer.level_id != suitable_level.id):
            customer = await self.repository.update_customer(customer_id, level_id=suitable_level.id)
        
        # 只选择基本字段，避免关联关系的异步加载问题
        customer_data = {
            "id": customer.id,
            "name": customer.name,
            "code": customer.code,
            "short_name": customer.short_name,
            "type": customer.type,
            "category_id": customer.category_id,
            "level_id": customer.level_id,
            "contact_name": customer.contact_name,
            "contact_phone": customer.contact_phone,
            "email": customer.email,
            "website": customer.website,
            "tax_no": customer.tax_no,
            "registered_capital": customer.registered_capital,
            "business_scope": customer.business_scope,
            "founding_date": customer.founding_date,
            "status": customer.status,
            "total_spend": customer.total_spend,
            "total_orders": customer.total_orders,
            "credit_limit": customer.credit_limit,
            "credit_balance": customer.credit_balance,
            "remark": customer.remark,
            "is_active": customer.is_active,
            "created_at": customer.created_at,
            "updated_at": customer.updated_at,
            "category": None,
            "level": None,
            "contacts": [],
            "addresses": [],
            "tags": []
        }
        return Customer(**customer_data)
    
    async def update_customer_spend(self, customer_id: int, amount: float) -> Optional[Customer]:
        """更新客户消费金额"""
        customer = await self.repository.get_customer(customer_id)
        if not customer:
            return None
        
        # 更新消费金额和订单数
        updated_customer = await self.repository.update_customer(
            customer_id,
            total_spend=customer.total_spend + amount,
            total_orders=customer.total_orders + 1
        )
        
        # 自动调整客户等级
        return await self.adjust_customer_level(customer_id)
    
    async def update_credit_balance(self, customer_id: int, amount: float) -> Optional[Customer]:
        """更新客户信用余额"""
        customer = await self.repository.get_customer(customer_id)
        if not customer:
            return None
        
        # 更新信用余额
        new_balance = customer.credit_balance + amount
        updated_customer = await self.repository.update_customer(
            customer_id,
            credit_balance=new_balance
        )
        
        # 只选择基本字段，避免关联关系的异步加载问题
        customer_data = {
            "id": updated_customer.id,
            "name": updated_customer.name,
            "code": updated_customer.code,
            "short_name": updated_customer.short_name,
            "type": updated_customer.type,
            "category_id": updated_customer.category_id,
            "level_id": updated_customer.level_id,
            "contact_name": updated_customer.contact_name,
            "contact_phone": updated_customer.contact_phone,
            "email": updated_customer.email,
            "website": updated_customer.website,
            "tax_no": updated_customer.tax_no,
            "registered_capital": updated_customer.registered_capital,
            "business_scope": updated_customer.business_scope,
            "founding_date": updated_customer.founding_date,
            "status": updated_customer.status,
            "total_spend": updated_customer.total_spend,
            "total_orders": updated_customer.total_orders,
            "credit_limit": updated_customer.credit_limit,
            "credit_balance": updated_customer.credit_balance,
            "remark": updated_customer.remark,
            "is_active": updated_customer.is_active,
            "created_at": updated_customer.created_at,
            "updated_at": updated_customer.updated_at,
            "category": None,
            "level": None,
            "contacts": [],
            "addresses": [],
            "tags": []
        }
        return Customer(**customer_data)
    
    # 客户联系人相关服务
    async def create_customer_contact(self, customer_id: int, contact_data: CustomerContactCreate) -> CustomerContact:
        """创建客户联系人"""
        contact_dict = contact_data.model_dump()
        contact = await self.repository.create_customer_contact(customer_id, **contact_dict)
        return CustomerContact.model_validate(contact)
    
    async def get_customer_contact(self, contact_id: int) -> Optional[CustomerContact]:
        """获取客户联系人详情"""
        contact = await self.repository.get_customer_contact(contact_id)
        if not contact:
            return None
        return CustomerContact.model_validate(contact)
    
    async def get_customer_contacts(self, customer_id: int) -> List[CustomerContact]:
        """获取客户联系人列表"""
        contacts = await self.repository.get_customer_contacts(customer_id)
        return [CustomerContact.model_validate(contact) for contact in contacts]
    
    async def update_customer_contact(self, contact_id: int, contact_data: CustomerContactUpdate) -> Optional[CustomerContact]:
        """更新客户联系人"""
        update_data = contact_data.model_dump(exclude_unset=True)
        contact = await self.repository.update_customer_contact(contact_id, **update_data)
        if not contact:
            return None
        return CustomerContact.model_validate(contact)
    
    async def delete_customer_contact(self, contact_id: int) -> bool:
        """删除客户联系人"""
        return await self.repository.delete_customer_contact(contact_id)
    
    # 客户地址相关服务
    async def create_customer_address(self, customer_id: int, address_data: CustomerAddressCreate) -> CustomerAddress:
        """创建客户地址"""
        address_dict = address_data.model_dump()
        address = await self.repository.create_customer_address(customer_id, **address_dict)
        return CustomerAddress.model_validate(address)
    
    async def get_customer_address(self, address_id: int) -> Optional[CustomerAddress]:
        """获取客户地址详情"""
        address = await self.repository.get_customer_address(address_id)
        if not address:
            return None
        return CustomerAddress.model_validate(address)
    
    async def get_customer_addresses(self, customer_id: int, 
                                   address_type: Optional[str] = None,
                                   is_active: Optional[bool] = None) -> List[CustomerAddress]:
        """获取客户地址列表"""
        addresses = await self.repository.get_customer_addresses(
            customer_id, address_type, is_active
        )
        return [CustomerAddress.model_validate(address) for address in addresses]
    
    async def update_customer_address(self, address_id: int, address_data: CustomerAddressUpdate) -> Optional[CustomerAddress]:
        """更新客户地址"""
        update_data = address_data.model_dump(exclude_unset=True)
        address = await self.repository.update_customer_address(address_id, **update_data)
        if not address:
            return None
        return CustomerAddress.model_validate(address)
    
    async def delete_customer_address(self, address_id: int) -> bool:
        """删除客户地址"""
        return await self.repository.delete_customer_address(address_id)
