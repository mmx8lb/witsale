from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.application.services.customer_service import CustomerService
from app.schemas.customer import (
    CustomerCategoryCreate, CustomerCategoryUpdate, CustomerCategory,
    CustomerLevelCreate, CustomerLevelUpdate, CustomerLevel,
    CustomerCreate, CustomerUpdate, Customer, CustomerUpdateTags,
    CustomerContactCreate, CustomerContactUpdate, CustomerContact,
    CustomerAddressCreate, CustomerAddressUpdate, CustomerAddress,
    CustomerTagCreate, CustomerTagUpdate, CustomerTag
)
from app.interfaces.api.deps import get_current_active_user
from app.models import User

router = APIRouter(prefix="/customer", tags=["customer"])


# 客户分类相关接口
@router.post("/categories", response_model=CustomerCategory)
async def create_customer_category(
    category: CustomerCategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建客户分类"""
    service = CustomerService(db)
    return await service.create_customer_category(category)


@router.get("/categories", response_model=List[CustomerCategory])
async def get_customer_categories(
    parent_category_id: Optional[int] = Query(None, description="父分类ID"),
    is_active: Optional[bool] = Query(None, description="是否激活"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取客户分类列表"""
    service = CustomerService(db)
    return await service.get_customer_categories(parent_category_id, is_active)


@router.get("/categories/{category_id}", response_model=CustomerCategory)
async def get_customer_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取客户分类详情"""
    service = CustomerService(db)
    category = await service.get_customer_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="客户分类不存在")
    return category


@router.put("/categories/{category_id}", response_model=CustomerCategory)
async def update_customer_category(
    category_id: int,
    category: CustomerCategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新客户分类"""
    service = CustomerService(db)
    updated_category = await service.update_customer_category(category_id, category)
    if not updated_category:
        raise HTTPException(status_code=404, detail="客户分类不存在")
    return updated_category


@router.delete("/categories/{category_id}")
async def delete_customer_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除客户分类"""
    service = CustomerService(db)
    deleted = await service.delete_customer_category(category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="客户分类不存在")
    return {"message": "客户分类删除成功"}


# 客户等级相关接口
@router.post("/levels", response_model=CustomerLevel)
async def create_customer_level(
    level: CustomerLevelCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建客户等级"""
    service = CustomerService(db)
    return await service.create_customer_level(level)


@router.get("/levels", response_model=List[CustomerLevel])
async def get_customer_levels(
    is_active: Optional[bool] = Query(None, description="是否激活"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取客户等级列表"""
    service = CustomerService(db)
    return await service.get_customer_levels(is_active)


@router.get("/levels/{level_id}", response_model=CustomerLevel)
async def get_customer_level(
    level_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取客户等级详情"""
    service = CustomerService(db)
    level = await service.get_customer_level(level_id)
    if not level:
        raise HTTPException(status_code=404, detail="客户等级不存在")
    return level


@router.put("/levels/{level_id}", response_model=CustomerLevel)
async def update_customer_level(
    level_id: int,
    level: CustomerLevelUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新客户等级"""
    service = CustomerService(db)
    updated_level = await service.update_customer_level(level_id, level)
    if not updated_level:
        raise HTTPException(status_code=404, detail="客户等级不存在")
    return updated_level


@router.delete("/levels/{level_id}")
async def delete_customer_level(
    level_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除客户等级"""
    service = CustomerService(db)
    deleted = await service.delete_customer_level(level_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="客户等级不存在")
    return {"message": "客户等级删除成功"}


# 客户标签相关接口
@router.post("/tags", response_model=CustomerTag)
async def create_customer_tag(
    tag: CustomerTagCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建客户标签"""
    service = CustomerService(db)
    return await service.create_customer_tag(tag)


@router.get("/tags", response_model=List[CustomerTag])
async def get_customer_tags(
    is_active: Optional[bool] = Query(None, description="是否激活"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取客户标签列表"""
    service = CustomerService(db)
    return await service.get_customer_tags(is_active)


@router.get("/tags/{tag_id}", response_model=CustomerTag)
async def get_customer_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取客户标签详情"""
    service = CustomerService(db)
    tag = await service.get_customer_tag(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="客户标签不存在")
    return tag


@router.put("/tags/{tag_id}", response_model=CustomerTag)
async def update_customer_tag(
    tag_id: int,
    tag: CustomerTagUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新客户标签"""
    service = CustomerService(db)
    updated_tag = await service.update_customer_tag(tag_id, tag)
    if not updated_tag:
        raise HTTPException(status_code=404, detail="客户标签不存在")
    return updated_tag


@router.delete("/tags/{tag_id}")
async def delete_customer_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除客户标签"""
    service = CustomerService(db)
    deleted = await service.delete_customer_tag(tag_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="客户标签不存在")
    return {"message": "客户标签删除成功"}


# 客户相关接口
@router.post("", response_model=Customer)
async def create_customer(
    customer: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建客户"""
    service = CustomerService(db)
    return await service.create_customer(customer)


@router.get("", response_model=List[Customer])
async def get_customers(
    category_id: Optional[int] = Query(None, description="客户分类ID"),
    level_id: Optional[int] = Query(None, description="客户等级ID"),
    status: Optional[str] = Query(None, description="客户状态"),
    is_active: Optional[bool] = Query(None, description="是否激活"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取客户列表"""
    service = CustomerService(db)
    return await service.get_customers(
        category_id=category_id,
        level_id=level_id,
        status=status,
        is_active=is_active,
        skip=skip,
        limit=limit
    )


@router.get("/{customer_id}", response_model=Customer)
async def get_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取客户详情"""
    service = CustomerService(db)
    customer = await service.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="客户不存在")
    return customer


@router.put("/{customer_id}", response_model=Customer)
async def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新客户"""
    service = CustomerService(db)
    updated_customer = await service.update_customer(customer_id, customer)
    if not updated_customer:
        raise HTTPException(status_code=404, detail="客户不存在")
    return updated_customer


@router.post("/{customer_id}/tags", response_model=Customer)
async def update_customer_tags(
    customer_id: int,
    tags_data: CustomerUpdateTags,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新客户标签"""
    service = CustomerService(db)
    updated_customer = await service.update_customer_tags(customer_id, tags_data)
    if not updated_customer:
        raise HTTPException(status_code=404, detail="客户不存在")
    return updated_customer


@router.delete("/{customer_id}")
async def delete_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除客户"""
    service = CustomerService(db)
    deleted = await service.delete_customer(customer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="客户不存在")
    return {"message": "客户删除成功"}


# 客户联系人相关接口
@router.post("/{customer_id}/contacts", response_model=CustomerContact)
async def create_customer_contact(
    customer_id: int,
    contact: CustomerContactCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建客户联系人"""
    service = CustomerService(db)
    return await service.create_customer_contact(customer_id, contact)


@router.get("/{customer_id}/contacts", response_model=List[CustomerContact])
async def get_customer_contacts(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取客户联系人列表"""
    service = CustomerService(db)
    return await service.get_customer_contacts(customer_id)


@router.get("/contacts/{contact_id}", response_model=CustomerContact)
async def get_customer_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取客户联系人详情"""
    service = CustomerService(db)
    contact = await service.get_customer_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="联系人不存在")
    return contact


@router.put("/contacts/{contact_id}", response_model=CustomerContact)
async def update_customer_contact(
    contact_id: int,
    contact: CustomerContactUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新客户联系人"""
    service = CustomerService(db)
    updated_contact = await service.update_customer_contact(contact_id, contact)
    if not updated_contact:
        raise HTTPException(status_code=404, detail="联系人不存在")
    return updated_contact


@router.delete("/contacts/{contact_id}")
async def delete_customer_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除客户联系人"""
    service = CustomerService(db)
    deleted = await service.delete_customer_contact(contact_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="联系人不存在")
    return {"message": "联系人删除成功"}


# 客户地址相关接口
@router.post("/{customer_id}/addresses", response_model=CustomerAddress)
async def create_customer_address(
    customer_id: int,
    address: CustomerAddressCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建客户地址"""
    service = CustomerService(db)
    return await service.create_customer_address(customer_id, address)


@router.get("/{customer_id}/addresses", response_model=List[CustomerAddress])
async def get_customer_addresses(
    customer_id: int,
    address_type: Optional[str] = Query(None, description="地址类型"),
    is_active: Optional[bool] = Query(None, description="是否激活"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取客户地址列表"""
    service = CustomerService(db)
    return await service.get_customer_addresses(
        customer_id, address_type, is_active
    )


@router.get("/addresses/{address_id}", response_model=CustomerAddress)
async def get_customer_address(
    address_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取客户地址详情"""
    service = CustomerService(db)
    address = await service.get_customer_address(address_id)
    if not address:
        raise HTTPException(status_code=404, detail="地址不存在")
    return address


@router.put("/addresses/{address_id}", response_model=CustomerAddress)
async def update_customer_address(
    address_id: int,
    address: CustomerAddressUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新客户地址"""
    service = CustomerService(db)
    updated_address = await service.update_customer_address(address_id, address)
    if not updated_address:
        raise HTTPException(status_code=404, detail="地址不存在")
    return updated_address


@router.delete("/addresses/{address_id}")
async def delete_customer_address(
    address_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除客户地址"""
    service = CustomerService(db)
    deleted = await service.delete_customer_address(address_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="地址不存在")
    return {"message": "地址删除成功"}
