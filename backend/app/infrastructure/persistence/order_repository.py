from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, func
from sqlalchemy.orm import selectinload
from datetime import datetime

from app.models.order import Order, OrderItem, OrderPayment, OrderStatusHistory, OrderRefund


class OrderRepository:
    """订单管理数据库操作类"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def _generate_order_no(self) -> str:
        """生成订单号"""
        from datetime import datetime
        import random
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        return f"ORD{timestamp}{random_suffix}"
    
    def _generate_payment_no(self) -> str:
        """生成支付单号"""
        from datetime import datetime
        import random
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        return f"PAY{timestamp}{random_suffix}"
    
    def _generate_refund_no(self) -> str:
        """生成退款单号"""
        from datetime import datetime
        import random
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        return f"REF{timestamp}{random_suffix}"
    
    # 订单相关操作
    async def create_order(self, customer_id: int, customer_name: str, items: List[Dict[str, Any]], 
                          order_type: str = "sales", order_level: str = "enterprise", 
                          parent_order_id: Optional[int] = None, shipping_address: Optional[Dict[str, Any]] = None,
                          notes: Optional[str] = None, created_by: Optional[int] = None) -> Order:
        """创建订单"""
        order_no = self._generate_order_no()
        
        total_amount = sum(item.get('total_price', 0) for item in items)
        discount_amount = sum(item.get('discount_price', 0) for item in items)
        actual_amount = total_amount - discount_amount
        
        order = Order(
            order_no=order_no,
            customer_id=customer_id,
            customer_name=customer_name,
            order_type=order_type,
            order_level=order_level,
            parent_order_id=parent_order_id,
            total_amount=total_amount,
            actual_amount=actual_amount,
            discount_amount=discount_amount,
            shipping_address=shipping_address,
            notes=notes,
            created_by=created_by,
            order_status="pending",
            payment_status="unpaid"
        )
        self.db.add(order)
        await self.db.flush()
        
        for item_data in items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data['product_id'],
                product_name=item_data['product_name'],
                sku_id=item_data.get('sku_id'),
                sku_code=item_data.get('sku_code'),
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                total_price=item_data['total_price'],
                discount_price=item_data.get('discount_price', 0.0),
                attributes=item_data.get('attributes')
            )
            self.db.add(order_item)
        
        status_history = OrderStatusHistory(
            order_id=order.id,
            status="pending",
            previous_status=None,
            description="订单创建",
            operator_id=created_by
        )
        self.db.add(status_history)
        
        await self.db.commit()
        await self.db.refresh(order)
        return order
    
    async def get_order(self, order_id: int) -> Optional[Order]:
        """获取订单详情"""
        result = await self.db.execute(
            select(Order)
            .options(
                selectinload(Order.items),
                selectinload(Order.payments),
                selectinload(Order.status_history),
                selectinload(Order.refunds)
            )
            .where(Order.id == order_id)
        )
        return result.scalar_one_or_none()
    
    async def get_order_by_no(self, order_no: str) -> Optional[Order]:
        """根据订单号获取订单"""
        result = await self.db.execute(
            select(Order)
            .options(
                selectinload(Order.items),
                selectinload(Order.payments),
                selectinload(Order.status_history),
                selectinload(Order.refunds)
            )
            .where(Order.order_no == order_no)
        )
        return result.scalar_one_or_none()
    
    async def get_orders(self, customer_id: Optional[int] = None, order_status: Optional[str] = None,
                        payment_status: Optional[str] = None, order_type: Optional[str] = None,
                        order_level: Optional[str] = None, start_date: Optional[datetime] = None,
                        end_date: Optional[datetime] = None, skip: int = 0, limit: int = 100) -> List[Order]:
        """获取订单列表"""
        query = select(Order)
        if customer_id is not None:
            query = query.where(Order.customer_id == customer_id)
        if order_status is not None:
            query = query.where(Order.order_status == order_status)
        if payment_status is not None:
            query = query.where(Order.payment_status == payment_status)
        if order_type is not None:
            query = query.where(Order.order_type == order_type)
        if order_level is not None:
            query = query.where(Order.order_level == order_level)
        if start_date is not None:
            query = query.where(Order.created_at >= start_date)
        if end_date is not None:
            query = query.where(Order.created_at <= end_date)
        query = query.order_by(Order.id.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_order(self, order_id: int, **kwargs) -> Optional[Order]:
        """更新订单"""
        order = await self.get_order(order_id)
        if not order:
            return None
        for key, value in kwargs.items():
            if hasattr(order, key):
                setattr(order, key, value)
        await self.db.commit()
        await self.db.refresh(order)
        return order
    
    async def update_order_status(self, order_id: int, new_status: str, description: Optional[str] = None,
                                 operator_id: Optional[int] = None, operator_name: Optional[str] = None) -> Optional[Order]:
        """更新订单状态"""
        order = await self.get_order(order_id)
        if not order:
            return None
        
        old_status = order.order_status
        order.order_status = new_status
        
        status_history = OrderStatusHistory(
            order_id=order.id,
            status=new_status,
            previous_status=old_status,
            description=description,
            operator_id=operator_id,
            operator_name=operator_name
        )
        self.db.add(status_history)
        
        await self.db.commit()
        await self.db.refresh(order)
        return order
    
    async def delete_order(self, order_id: int) -> bool:
        """删除订单"""
        result = await self.db.execute(delete(Order).where(Order.id == order_id))
        await self.db.commit()
        return result.rowcount > 0
    
    async def get_order_stats(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """获取订单统计数据"""
        query = select(Order)
        if start_date is not None:
            query = query.where(Order.created_at >= start_date)
        if end_date is not None:
            query = query.where(Order.created_at <= end_date)
        
        result = await self.db.execute(query)
        orders = result.scalars().all()
        
        total_orders = len(orders)
        total_amount = sum(order.total_amount for order in orders)
        paid_orders = sum(1 for order in orders if order.payment_status == "paid")
        shipped_orders = sum(1 for order in orders if order.order_status == "shipped")
        completed_orders = sum(1 for order in orders if order.order_status == "completed")
        cancelled_orders = sum(1 for order in orders if order.order_status == "cancelled")
        
        return {
            "total_orders": total_orders,
            "total_amount": total_amount,
            "paid_orders": paid_orders,
            "shipped_orders": shipped_orders,
            "completed_orders": completed_orders,
            "cancelled_orders": cancelled_orders
        }
    
    # 支付相关操作
    async def create_payment(self, order_id: int, payment_method: str, amount: float,
                            transaction_id: Optional[str] = None, notes: Optional[str] = None) -> OrderPayment:
        """创建支付记录"""
        payment_no = self._generate_payment_no()
        payment = OrderPayment(
            order_id=order_id,
            payment_no=payment_no,
            payment_method=payment_method,
            amount=amount,
            transaction_id=transaction_id,
            notes=notes,
            payment_status="pending"
        )
        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)
        return payment
    
    async def update_payment_status(self, payment_id: int, payment_status: str, paid_at: Optional[datetime] = None) -> Optional[OrderPayment]:
        """更新支付状态"""
        result = await self.db.execute(select(OrderPayment).where(OrderPayment.id == payment_id))
        payment = result.scalar_one_or_none()
        if not payment:
            return None
        payment.payment_status = payment_status
        if paid_at:
            payment.paid_at = paid_at
        await self.db.commit()
        await self.db.refresh(payment)
        return payment
    
    async def get_payments_by_order(self, order_id: int) -> List[OrderPayment]:
        """获取订单的所有支付记录"""
        result = await self.db.execute(
            select(OrderPayment)
            .where(OrderPayment.order_id == order_id)
            .order_by(OrderPayment.created_at.desc())
        )
        return result.scalars().all()
    
    # 退款相关操作
    async def create_refund(self, order_id: int, refund_type: str, refund_amount: float,
                           reason: Optional[str] = None, notes: Optional[str] = None) -> OrderRefund:
        """创建退款记录"""
        refund_no = self._generate_refund_no()
        refund = OrderRefund(
            order_id=order_id,
            refund_no=refund_no,
            refund_type=refund_type,
            refund_amount=refund_amount,
            reason=reason,
            notes=notes,
            refund_status="pending"
        )
        self.db.add(refund)
        await self.db.commit()
        await self.db.refresh(refund)
        return refund
    
    async def update_refund_status(self, refund_id: int, refund_status: str,
                                  processed_by: Optional[int] = None, notes: Optional[str] = None) -> Optional[OrderRefund]:
        """更新退款状态"""
        result = await self.db.execute(select(OrderRefund).where(OrderRefund.id == refund_id))
        refund = result.scalar_one_or_none()
        if not refund:
            return None
        refund.refund_status = refund_status
        if processed_by:
            refund.processed_by = processed_by
            refund.processed_at = datetime.utcnow()
        if notes:
            refund.notes = notes
        await self.db.commit()
        await self.db.refresh(refund)
        return refund
    
    async def get_refunds_by_order(self, order_id: int) -> List[OrderRefund]:
        """获取订单的所有退款记录"""
        result = await self.db.execute(
            select(OrderRefund)
            .where(OrderRefund.order_id == order_id)
            .order_by(OrderRefund.created_at.desc())
        )
        return result.scalars().all()
