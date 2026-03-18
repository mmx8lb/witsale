from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import selectinload
from datetime import datetime

from app.models.inventory import (
    Warehouse, Stock, StockMovement,
    StockTransfer, StockTransferItem,
    StockCheck, StockCheckItem
)


class InventoryRepository:
    """库存管理数据库操作类"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def _generate_transfer_no(self) -> str:
        """生成调拨单号"""
        from datetime import datetime
        import random
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        return f"TRF{timestamp}{random_suffix}"
    
    def _generate_check_no(self) -> str:
        """生成盘点单号"""
        from datetime import datetime
        import random
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        return f"CHK{timestamp}{random_suffix}"
    
    # 仓库相关操作
    async def create_warehouse(self, name: str, code: str, **kwargs) -> Warehouse:
        """创建仓库"""
        warehouse = Warehouse(
            name=name,
            code=code,
            **kwargs
        )
        self.db.add(warehouse)
        await self.db.commit()
        await self.db.refresh(warehouse)
        return warehouse
    
    async def get_warehouse(self, warehouse_id: int) -> Optional[Warehouse]:
        """获取仓库详情"""
        result = await self.db.execute(
            select(Warehouse)
            .options(selectinload(Warehouse.children))
            .where(Warehouse.id == warehouse_id)
        )
        return result.scalar_one_or_none()
    
    async def get_warehouses(self, parent_warehouse_id: Optional[int] = None, is_active: Optional[bool] = None) -> List[Warehouse]:
        """获取仓库列表"""
        query = select(Warehouse)
        if parent_warehouse_id is not None:
            query = query.where(Warehouse.parent_warehouse_id == parent_warehouse_id)
        if is_active is not None:
            query = query.where(Warehouse.is_active == is_active)
        query = query.order_by(Warehouse.level, Warehouse.id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_warehouse(self, warehouse_id: int, **kwargs) -> Optional[Warehouse]:
        """更新仓库"""
        warehouse = await self.get_warehouse(warehouse_id)
        if not warehouse:
            return None
        for key, value in kwargs.items():
            if hasattr(warehouse, key):
                setattr(warehouse, key, value)
        await self.db.commit()
        await self.db.refresh(warehouse)
        return warehouse
    
    async def delete_warehouse(self, warehouse_id: int) -> bool:
        """删除仓库"""
        result = await self.db.execute(delete(Warehouse).where(Warehouse.id == warehouse_id))
        await self.db.commit()
        return result.rowcount > 0
    
    # 库存相关操作
    async def create_stock(self, warehouse_id: int, product_id: int, product_name: str, **kwargs) -> Stock:
        """创建库存"""
        stock = Stock(
            warehouse_id=warehouse_id,
            product_id=product_id,
            product_name=product_name,
            **kwargs
        )
        self.db.add(stock)
        await self.db.commit()
        await self.db.refresh(stock)
        return stock
    
    async def get_stock(self, stock_id: int) -> Optional[Stock]:
        """获取库存详情"""
        result = await self.db.execute(
            select(Stock)
            .options(selectinload(Stock.warehouse))
            .where(Stock.id == stock_id)
        )
        return result.scalar_one_or_none()
    
    async def get_stocks(self, warehouse_id: Optional[int] = None, product_id: Optional[int] = None,
                       is_active: Optional[bool] = None, skip: int = 0, limit: int = 100) -> List[Stock]:
        """获取库存列表"""
        query = select(Stock)
        if warehouse_id is not None:
            query = query.where(Stock.warehouse_id == warehouse_id)
        if product_id is not None:
            query = query.where(Stock.product_id == product_id)
        if is_active is not None:
            query = query.where(Stock.is_active == is_active)
        query = query.options(selectinload(Stock.warehouse))
        query = query.order_by(Stock.id.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_stock(self, stock_id: int, **kwargs) -> Optional[Stock]:
        """更新库存"""
        stock = await self.get_stock(stock_id)
        if not stock:
            return None
        for key, value in kwargs.items():
            if hasattr(stock, key):
                setattr(stock, key, value)
        await self.db.commit()
        await self.db.refresh(stock)
        return stock
    
    async def adjust_stock(self, stock_id: int, adjustment_quantity: int, movement_type: str,
                        remark: Optional[str] = None, operator_id: Optional[int] = None,
                        operator_name: Optional[str] = None) -> Optional[Stock]:
        """调整库存"""
        stock = await self.get_stock(stock_id)
        if not stock:
            return None
        
        before_quantity = stock.quantity
        after_quantity = before_quantity + adjustment_quantity
        
        stock.quantity = after_quantity
        stock.available_quantity = after_quantity - stock.locked_quantity
        
        movement = StockMovement(
            stock_id=stock_id,
            movement_type=movement_type,
            quantity=adjustment_quantity,
            before_quantity=before_quantity,
            after_quantity=after_quantity,
            remark=remark,
            operator_id=operator_id,
            operator_name=operator_name
        )
        self.db.add(movement)
        
        await self.db.commit()
        await self.db.refresh(stock)
        return stock
    
    async def get_low_stock_alerts(self, warehouse_id: Optional[int] = None) -> List[Stock]:
        """获取低库存预警"""
        query = select(Stock).where(Stock.available_quantity <= Stock.min_stock)
        if warehouse_id is not None:
            query = query.where(Stock.warehouse_id == warehouse_id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    # 库存调拨相关操作
    async def create_transfer(self, from_warehouse_id: int, to_warehouse_id: int,
                           items: List[Dict[str, Any]], operator_id: Optional[int] = None,
                           operator_name: Optional[str] = None, **kwargs) -> StockTransfer:
        """创建库存调拨"""
        transfer_no = self._generate_transfer_no()
        total_quantity = sum(item.get('quantity', 0) for item in items)
        
        transfer = StockTransfer(
            transfer_no=transfer_no,
            from_warehouse_id=from_warehouse_id,
            to_warehouse_id=to_warehouse_id,
            total_quantity=total_quantity,
            operator_id=operator_id,
            operator_name=operator_name,
            transfer_status="pending",
            **kwargs
        )
        self.db.add(transfer)
        await self.db.flush()
        
        for item_data in items:
            transfer_item = StockTransferItem(
                transfer_id=transfer.id,
                product_id=item_data['product_id'],
                product_name=item_data['product_name'],
                sku_id=item_data.get('sku_id'),
                sku_code=item_data.get('sku_code'),
                quantity=item_data['quantity'],
                remark=item_data.get('remark')
            )
            self.db.add(transfer_item)
        
        await self.db.commit()
        await self.db.refresh(transfer)
        return transfer
    
    async def get_transfer(self, transfer_id: int) -> Optional[StockTransfer]:
        """获取库存调拨详情"""
        result = await self.db.execute(
            select(StockTransfer)
            .options(
                selectinload(StockTransfer.from_warehouse),
                selectinload(StockTransfer.to_warehouse),
                selectinload(StockTransfer.items)
            )
            .where(StockTransfer.id == transfer_id)
        )
        return result.scalar_one_or_none()
    
    async def update_transfer_status(self, transfer_id: int, new_status: str, **kwargs) -> Optional[StockTransfer]:
        """更新库存调拨状态"""
        transfer = await self.get_transfer(transfer_id)
        if not transfer:
            return None
        transfer.transfer_status = new_status
        for key, value in kwargs.items():
            if hasattr(transfer, key):
                setattr(transfer, key, value)
        await self.db.commit()
        await self.db.refresh(transfer)
        return transfer
    
    # 库存盘点相关操作
    async def create_check(self, warehouse_id: int, items: List[Dict[str, Any]],
                        operator_id: Optional[int] = None, operator_name: Optional[str] = None, **kwargs) -> StockCheck:
        """创建库存盘点"""
        check_no = self._generate_check_no()
        
        check = StockCheck(
            check_no=check_no,
            warehouse_id=warehouse_id,
            operator_id=operator_id,
            operator_name=operator_name,
            check_status="pending",
            **kwargs
        )
        self.db.add(check)
        await self.db.flush()
        
        for item_data in items:
            check_item = StockCheckItem(
                check_id=check.id,
                stock_id=item_data['stock_id'],
                product_id=item_data['product_id'],
                product_name=item_data['product_name'],
                sku_id=item_data.get('sku_id'),
                sku_code=item_data.get('sku_code'),
                system_quantity=item_data['system_quantity'],
                actual_quantity=item_data['actual_quantity'],
                diff_quantity=item_data['diff_quantity'],
                remark=item_data.get('remark')
            )
            self.db.add(check_item)
        
        await self.db.commit()
        await self.db.refresh(check)
        return check
    
    async def get_check(self, check_id: int) -> Optional[StockCheck]:
        """获取库存盘点详情"""
        result = await self.db.execute(
            select(StockCheck)
            .options(
                selectinload(StockCheck.warehouse),
                selectinload(StockCheck.items)
            )
            .where(StockCheck.id == check_id)
        )
        return result.scalar_one_or_none()
    
    async def update_check_status(self, check_id: int, new_status: str, **kwargs) -> Optional[StockCheck]:
        """更新库存盘点状态"""
        check = await self.get_check(check_id)
        if not check:
            return None
        check.check_status = new_status
        for key, value in kwargs.items():
            if hasattr(check, key):
                setattr(check, key, value)
        await self.db.commit()
        await self.db.refresh(check)
        return check
