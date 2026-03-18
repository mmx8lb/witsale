from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.inventory_repository import InventoryRepository
from app.schemas.inventory import (
    WarehouseCreate, WarehouseUpdate, Warehouse,
    StockCreate, StockUpdate, Stock,
    StockTransferCreate, StockTransfer,
    StockCheckCreate, StockCheck,
    StockAdjustmentRequest
)


class InventoryService:
    """库存管理服务层"""
    
    def __init__(self, db: AsyncSession):
        self.repository = InventoryRepository(db)
    
    # 仓库相关服务
    async def create_warehouse(self, warehouse_data: WarehouseCreate) -> Warehouse:
        """创建仓库"""
        # 将WarehouseCreate转换为字典，只传递非空值
        warehouse_dict = warehouse_data.model_dump(exclude_unset=True)
        warehouse = await self.repository.create_warehouse(**warehouse_dict)
        # 只选择基本字段，避免children关系的异步加载问题
        warehouse_data = {
            "id": warehouse.id,
            "name": warehouse.name,
            "code": warehouse.code,
            "address": warehouse.address,
            "contact_person": warehouse.contact_person,
            "contact_phone": warehouse.contact_phone,
            "warehouse_type": warehouse.warehouse_type,
            "level": warehouse.level,
            "parent_warehouse_id": warehouse.parent_warehouse_id,
            "is_active": warehouse.is_active,
            "created_at": warehouse.created_at,
            "updated_at": warehouse.updated_at
        }
        return Warehouse(**warehouse_data)
    
    async def get_warehouse(self, warehouse_id: int) -> Optional[Warehouse]:
        """获取仓库详情"""
        warehouse = await self.repository.get_warehouse(warehouse_id)
        if not warehouse:
            return None
        # 只选择基本字段，避免children关系的异步加载问题
        warehouse_data = {
            "id": warehouse.id,
            "name": warehouse.name,
            "code": warehouse.code,
            "address": warehouse.address,
            "contact_person": warehouse.contact_person,
            "contact_phone": warehouse.contact_phone,
            "warehouse_type": warehouse.warehouse_type,
            "level": warehouse.level,
            "parent_warehouse_id": warehouse.parent_warehouse_id,
            "is_active": warehouse.is_active,
            "created_at": warehouse.created_at,
            "updated_at": warehouse.updated_at
        }
        return Warehouse(**warehouse_data)
    
    async def get_warehouses(self, parent_warehouse_id: Optional[int] = None, is_active: Optional[bool] = None) -> List[Warehouse]:
        """获取仓库列表"""
        warehouses = await self.repository.get_warehouses(parent_warehouse_id, is_active)
        result = []
        for warehouse in warehouses:
            # 只选择基本字段，避免children关系的异步加载问题
            warehouse_data = {
                "id": warehouse.id,
                "name": warehouse.name,
                "code": warehouse.code,
                "address": warehouse.address,
                "contact_person": warehouse.contact_person,
                "contact_phone": warehouse.contact_phone,
                "warehouse_type": warehouse.warehouse_type,
                "level": warehouse.level,
                "parent_warehouse_id": warehouse.parent_warehouse_id,
                "is_active": warehouse.is_active,
                "created_at": warehouse.created_at,
                "updated_at": warehouse.updated_at
            }
            result.append(Warehouse(**warehouse_data))
        return result
    
    async def update_warehouse(self, warehouse_id: int, warehouse_data: WarehouseUpdate) -> Optional[Warehouse]:
        """更新仓库"""
        update_data = warehouse_data.model_dump(exclude_unset=True)
        warehouse = await self.repository.update_warehouse(warehouse_id, **update_data)
        if not warehouse:
            return None
        # 只选择基本字段，避免children关系的异步加载问题
        warehouse_data = {
            "id": warehouse.id,
            "name": warehouse.name,
            "code": warehouse.code,
            "address": warehouse.address,
            "contact_person": warehouse.contact_person,
            "contact_phone": warehouse.contact_phone,
            "warehouse_type": warehouse.warehouse_type,
            "level": warehouse.level,
            "parent_warehouse_id": warehouse.parent_warehouse_id,
            "is_active": warehouse.is_active,
            "created_at": warehouse.created_at,
            "updated_at": warehouse.updated_at
        }
        return Warehouse(**warehouse_data)
    
    async def delete_warehouse(self, warehouse_id: int) -> bool:
        """删除仓库"""
        return await self.repository.delete_warehouse(warehouse_id)
    
    # 库存相关服务
    async def create_stock(self, stock_data: StockCreate) -> Stock:
        """创建库存"""
        stock = await self.repository.create_stock(
            warehouse_id=stock_data.warehouse_id,
            product_id=stock_data.product_id,
            product_name=stock_data.product_name,
            sku_id=stock_data.sku_id,
            sku_code=stock_data.sku_code,
            quantity=stock_data.quantity,
            available_quantity=stock_data.available_quantity,
            locked_quantity=stock_data.locked_quantity,
            cost_price=stock_data.cost_price,
            min_stock=stock_data.min_stock,
            max_stock=stock_data.max_stock,
            batch_no=stock_data.batch_no,
            expiry_date=stock_data.expiry_date,
            attributes=stock_data.attributes,
            is_active=stock_data.is_active
        )
        return Stock.model_validate(stock)
    
    async def get_stock(self, stock_id: int) -> Optional[Stock]:
        """获取库存详情"""
        stock = await self.repository.get_stock(stock_id)
        if not stock:
            return None
        return Stock.model_validate(stock)
    
    async def get_stocks(self, warehouse_id: Optional[int] = None, product_id: Optional[int] = None,
                       is_active: Optional[bool] = None, skip: int = 0, limit: int = 100) -> List[Stock]:
        """获取库存列表"""
        stocks = await self.repository.get_stocks(warehouse_id, product_id, is_active, skip, limit)
        return [Stock.model_validate(stock) for stock in stocks]
    
    async def update_stock(self, stock_id: int, stock_data: StockUpdate) -> Optional[Stock]:
        """更新库存"""
        update_data = stock_data.model_dump(exclude_unset=True)
        stock = await self.repository.update_stock(stock_id, **update_data)
        if not stock:
            return None
        return Stock.model_validate(stock)
    
    async def adjust_stock(self, adjustment_data: StockAdjustmentRequest, operator_id: Optional[int] = None,
                          operator_name: Optional[str] = None) -> Optional[Stock]:
        """调整库存"""
        movement_type = "in" if adjustment_data.adjustment_quantity > 0 else "out"
        stock = await self.repository.adjust_stock(
            stock_id=adjustment_data.stock_id,
            adjustment_quantity=adjustment_data.adjustment_quantity,
            movement_type=movement_type,
            remark=adjustment_data.remark,
            operator_id=operator_id,
            operator_name=operator_name
        )
        if not stock:
            return None
        return Stock.model_validate(stock)
    
    async def get_low_stock_alerts(self, warehouse_id: Optional[int] = None) -> List[Stock]:
        """获取低库存预警"""
        stocks = await self.repository.get_low_stock_alerts(warehouse_id)
        return [Stock.model_validate(stock) for stock in stocks]
    
    # 库存调拨相关服务
    async def create_transfer(self, transfer_data: StockTransferCreate, operator_id: Optional[int] = None,
                             operator_name: Optional[str] = None) -> StockTransfer:
        """创建库存调拨"""
        items_data = [item.model_dump() for item in transfer_data.items]
        transfer = await self.repository.create_transfer(
            from_warehouse_id=transfer_data.from_warehouse_id,
            to_warehouse_id=transfer_data.to_warehouse_id,
            items=items_data,
            operator_id=operator_id,
            operator_name=operator_name,
            transfer_type=transfer_data.transfer_type,
            remark=transfer_data.remark
        )
        return StockTransfer.model_validate(transfer)
    
    async def get_transfer(self, transfer_id: int) -> Optional[StockTransfer]:
        """获取库存调拨详情"""
        transfer = await self.repository.get_transfer(transfer_id)
        if not transfer:
            return None
        return StockTransfer.model_validate(transfer)
    
    async def approve_transfer(self, transfer_id: int, approved_by: Optional[int] = None) -> Optional[StockTransfer]:
        """审批库存调拨"""
        from datetime import datetime
        transfer = await self.repository.update_transfer_status(
            transfer_id,
            new_status="approved",
            approved_by=approved_by,
            approved_at=datetime.utcnow()
        )
        if not transfer:
            return None
        return StockTransfer.model_validate(transfer)
    
    async def ship_transfer(self, transfer_id: int) -> Optional[StockTransfer]:
        """库存调拨发货"""
        from datetime import datetime
        transfer = await self.repository.update_transfer_status(
            transfer_id,
            new_status="shipped",
            shipped_at=datetime.utcnow()
        )
        if not transfer:
            return None
        return StockTransfer.model_validate(transfer)
    
    async def receive_transfer(self, transfer_id: int) -> Optional[StockTransfer]:
        """库存调拨收货"""
        from datetime import datetime
        transfer = await self.repository.update_transfer_status(
            transfer_id,
            new_status="received",
            received_at=datetime.utcnow()
        )
        if not transfer:
            return None
        return StockTransfer.model_validate(transfer)
    
    # 库存盘点相关服务
    async def create_check(self, check_data: StockCheckCreate, operator_id: Optional[int] = None,
                          operator_name: Optional[str] = None) -> StockCheck:
        """创建库存盘点"""
        items_data = [item.model_dump() for item in check_data.items]
        check = await self.repository.create_check(
            warehouse_id=check_data.warehouse_id,
            items=items_data,
            operator_id=operator_id,
            operator_name=operator_name,
            check_type=check_data.check_type,
            remark=check_data.remark
        )
        return StockCheck.model_validate(check)
    
    async def get_check(self, check_id: int) -> Optional[StockCheck]:
        """获取库存盘点详情"""
        check = await self.repository.get_check(check_id)
        if not check:
            return None
        return StockCheck.model_validate(check)
    
    async def start_check(self, check_id: int) -> Optional[StockCheck]:
        """开始库存盘点"""
        from datetime import datetime
        check = await self.repository.update_check_status(
            check_id,
            new_status="in_progress",
            started_at=datetime.utcnow()
        )
        if not check:
            return None
        return StockCheck.model_validate(check)
    
    async def complete_check(self, check_id: int) -> Optional[StockCheck]:
        """完成库存盘点"""
        from datetime import datetime
        check = await self.repository.update_check_status(
            check_id,
            new_status="completed",
            completed_at=datetime.utcnow()
        )
        if not check:
            return None
        return StockCheck.model_validate(check)
