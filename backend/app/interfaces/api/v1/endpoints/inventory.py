from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.application.services.inventory_service import InventoryService
from app.schemas.inventory import (
    WarehouseCreate, WarehouseUpdate, Warehouse,
    StockCreate, StockUpdate, Stock,
    StockTransferCreate, StockTransfer,
    StockCheckCreate, StockCheck,
    StockAdjustmentRequest
)
from app.interfaces.api.deps import get_current_active_user
from app.models import User

router = APIRouter(prefix="/inventory", tags=["inventory"])


# 仓库相关接口
@router.post("/warehouses", response_model=Warehouse)
async def create_warehouse(
    warehouse: WarehouseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建仓库"""
    service = InventoryService(db)
    return await service.create_warehouse(warehouse)


@router.get("/warehouses", response_model=List[Warehouse])
async def get_warehouses(
    parent_warehouse_id: Optional[int] = Query(None, description="父仓库ID"),
    is_active: Optional[bool] = Query(None, description="是否激活"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取仓库列表"""
    service = InventoryService(db)
    return await service.get_warehouses(parent_warehouse_id, is_active)


@router.get("/warehouses/{warehouse_id}", response_model=Warehouse)
async def get_warehouse(
    warehouse_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取仓库详情"""
    service = InventoryService(db)
    warehouse = await service.get_warehouse(warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="仓库不存在")
    return warehouse


@router.put("/warehouses/{warehouse_id}", response_model=Warehouse)
async def update_warehouse(
    warehouse_id: int,
    warehouse: WarehouseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新仓库"""
    service = InventoryService(db)
    updated_warehouse = await service.update_warehouse(warehouse_id, warehouse)
    if not updated_warehouse:
        raise HTTPException(status_code=404, detail="仓库不存在")
    return updated_warehouse


@router.delete("/warehouses/{warehouse_id}")
async def delete_warehouse(
    warehouse_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除仓库"""
    service = InventoryService(db)
    deleted = await service.delete_warehouse(warehouse_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="仓库不存在")
    return {"message": "仓库删除成功"}


# 库存相关接口
@router.post("/stocks", response_model=Stock)
async def create_stock(
    stock: StockCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建库存"""
    service = InventoryService(db)
    return await service.create_stock(stock)


@router.get("/stocks", response_model=List[Stock])
async def get_stocks(
    warehouse_id: Optional[int] = Query(None, description="仓库ID"),
    product_id: Optional[int] = Query(None, description="商品ID"),
    is_active: Optional[bool] = Query(None, description="是否激活"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取库存列表"""
    service = InventoryService(db)
    return await service.get_stocks(warehouse_id, product_id, is_active, skip, limit)


@router.get("/stocks/{stock_id}", response_model=Stock)
async def get_stock(
    stock_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取库存详情"""
    service = InventoryService(db)
    stock = await service.get_stock(stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="库存不存在")
    return stock


@router.put("/stocks/{stock_id}", response_model=Stock)
async def update_stock(
    stock_id: int,
    stock: StockUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新库存"""
    service = InventoryService(db)
    updated_stock = await service.update_stock(stock_id, stock)
    if not updated_stock:
        raise HTTPException(status_code=404, detail="库存不存在")
    return updated_stock


@router.post("/stocks/adjust", response_model=Stock)
async def adjust_stock(
    adjustment_data: StockAdjustmentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """调整库存"""
    service = InventoryService(db)
    stock = await service.adjust_stock(
        adjustment_data,
        operator_id=current_user.id,
        operator_name=current_user.username
    )
    if not stock:
        raise HTTPException(status_code=404, detail="库存不存在")
    return stock


@router.get("/stocks/alerts/low", response_model=List[Stock])
async def get_low_stock_alerts(
    warehouse_id: Optional[int] = Query(None, description="仓库ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取低库存预警"""
    service = InventoryService(db)
    return await service.get_low_stock_alerts(warehouse_id)


# 库存调拨相关接口
@router.post("/transfers", response_model=StockTransfer)
async def create_transfer(
    transfer: StockTransferCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建库存调拨"""
    service = InventoryService(db)
    return await service.create_transfer(
        transfer,
        operator_id=current_user.id,
        operator_name=current_user.username
    )


@router.get("/transfers/{transfer_id}", response_model=StockTransfer)
async def get_transfer(
    transfer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取库存调拨详情"""
    service = InventoryService(db)
    transfer = await service.get_transfer(transfer_id)
    if not transfer:
        raise HTTPException(status_code=404, detail="库存调拨不存在")
    return transfer


@router.post("/transfers/{transfer_id}/approve", response_model=StockTransfer)
async def approve_transfer(
    transfer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """审批库存调拨"""
    service = InventoryService(db)
    transfer = await service.approve_transfer(transfer_id, approved_by=current_user.id)
    if not transfer:
        raise HTTPException(status_code=404, detail="库存调拨不存在")
    return transfer


@router.post("/transfers/{transfer_id}/ship", response_model=StockTransfer)
async def ship_transfer(
    transfer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """库存调拨发货"""
    service = InventoryService(db)
    transfer = await service.ship_transfer(transfer_id)
    if not transfer:
        raise HTTPException(status_code=404, detail="库存调拨不存在")
    return transfer


@router.post("/transfers/{transfer_id}/receive", response_model=StockTransfer)
async def receive_transfer(
    transfer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """库存调拨收货"""
    service = InventoryService(db)
    transfer = await service.receive_transfer(transfer_id)
    if not transfer:
        raise HTTPException(status_code=404, detail="库存调拨不存在")
    return transfer


# 库存盘点相关接口
@router.post("/checks", response_model=StockCheck)
async def create_check(
    check: StockCheckCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建库存盘点"""
    service = InventoryService(db)
    return await service.create_check(
        check,
        operator_id=current_user.id,
        operator_name=current_user.username
    )


@router.get("/checks/{check_id}", response_model=StockCheck)
async def get_check(
    check_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取库存盘点详情"""
    service = InventoryService(db)
    check = await service.get_check(check_id)
    if not check:
        raise HTTPException(status_code=404, detail="库存盘点不存在")
    return check


@router.post("/checks/{check_id}/start", response_model=StockCheck)
async def start_check(
    check_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """开始库存盘点"""
    service = InventoryService(db)
    check = await service.start_check(check_id)
    if not check:
        raise HTTPException(status_code=404, detail="库存盘点不存在")
    return check


@router.post("/checks/{check_id}/complete", response_model=StockCheck)
async def complete_check(
    check_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """完成库存盘点"""
    service = InventoryService(db)
    check = await service.complete_check(check_id)
    if not check:
        raise HTTPException(status_code=404, detail="库存盘点不存在")
    return check
