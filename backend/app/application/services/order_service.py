from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.order_repository import OrderRepository
from app.schemas.order import (
    OrderCreate, OrderUpdate, Order, OrderList,
    OrderItem, OrderPayment, OrderRefund,
    OrderStatusHistory, OrderStats,
    OrderStatusUpdate, OrderPaymentRequest,
    OrderShipRequest, OrderCancelRequest
)


class OrderService:
    """订单管理服务层"""
    
    def __init__(self, db: AsyncSession):
        self.repository = OrderRepository(db)
    
    # 订单相关服务
    async def create_order(self, order_data: OrderCreate, created_by: Optional[int] = None) -> Order:
        """创建订单"""
        items_data = [item.model_dump() for item in order_data.items]
        order = await self.repository.create_order(
            customer_id=order_data.customer_id,
            customer_name=order_data.customer_name,
            items=items_data,
            order_type=order_data.order_type,
            order_level=order_data.order_level,
            parent_order_id=order_data.parent_order_id,
            shipping_address=order_data.shipping_address,
            notes=order_data.notes,
            created_by=created_by
        )
        return Order.model_validate(order)
    
    async def get_order(self, order_id: int) -> Optional[Order]:
        """获取订单详情"""
        order = await self.repository.get_order(order_id)
        if not order:
            return None
        return Order.model_validate(order)
    
    async def get_order_by_no(self, order_no: str) -> Optional[Order]:
        """根据订单号获取订单"""
        order = await self.repository.get_order_by_no(order_no)
        if not order:
            return None
        return Order.model_validate(order)
    
    async def get_orders(self, customer_id: Optional[int] = None, order_status: Optional[str] = None,
                        payment_status: Optional[str] = None, order_type: Optional[str] = None,
                        order_level: Optional[str] = None, start_date: Optional[datetime] = None,
                        end_date: Optional[datetime] = None, skip: int = 0, limit: int = 100) -> List[OrderList]:
        """获取订单列表"""
        orders = await self.repository.get_orders(
            customer_id=customer_id,
            order_status=order_status,
            payment_status=payment_status,
            order_type=order_type,
            order_level=order_level,
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            limit=limit
        )
        return [OrderList.model_validate(order) for order in orders]
    
    async def update_order(self, order_id: int, order_data: OrderUpdate) -> Optional[Order]:
        """更新订单"""
        update_data = order_data.model_dump(exclude_unset=True)
        order = await self.repository.update_order(order_id, **update_data)
        if not order:
            return None
        return Order.model_validate(order)
    
    async def update_order_status(self, order_id: int, status_data: OrderStatusUpdate,
                                  operator_id: Optional[int] = None, operator_name: Optional[str] = None) -> Optional[Order]:
        """更新订单状态"""
        order = await self.repository.update_order_status(
            order_id=order_id,
            new_status=status_data.order_status,
            description=status_data.description,
            operator_id=operator_id,
            operator_name=operator_name
        )
        if not order:
            return None
        return Order.model_validate(order)
    
    async def pay_order(self, order_id: int, payment_data: OrderPaymentRequest,
                       operator_id: Optional[int] = None) -> Optional[Order]:
        """订单支付"""
        order = await self.repository.get_order(order_id)
        if not order:
            return None
        
        payment = await self.repository.create_payment(
            order_id=order_id,
            payment_method=payment_data.payment_method,
            amount=order.actual_amount,
            transaction_id=payment_data.transaction_id,
            notes=payment_data.notes
        )
        
        payment = await self.repository.update_payment_status(
            payment.id,
            payment_status="paid",
            paid_at=datetime.utcnow()
        )
        
        order = await self.repository.update_order(
            order_id,
            payment_method=payment_data.payment_method,
            payment_status="paid"
        )
        
        order = await self.repository.update_order_status(
            order_id,
            new_status="paid",
            description="订单支付成功",
            operator_id=operator_id
        )
        
        return Order.model_validate(order)
    
    async def ship_order(self, order_id: int, ship_data: OrderShipRequest,
                        operator_id: Optional[int] = None, operator_name: Optional[str] = None) -> Optional[Order]:
        """订单发货"""
        order = await self.repository.update_order(
            order_id,
            logistics_company=ship_data.logistics_company,
            tracking_number=ship_data.tracking_number
        )
        if not order:
            return None
        
        order = await self.repository.update_order_status(
            order_id,
            new_status="shipped",
            description=f"订单已发货，物流：{ship_data.logistics_company}，单号：{ship_data.tracking_number}",
            operator_id=operator_id,
            operator_name=operator_name
        )
        return Order.model_validate(order)
    
    async def confirm_order(self, order_id: int, operator_id: Optional[int] = None,
                           operator_name: Optional[str] = None) -> Optional[Order]:
        """确认收货"""
        order = await self.repository.update_order_status(
            order_id,
            new_status="completed",
            description="订单确认收货",
            operator_id=operator_id,
            operator_name=operator_name
        )
        if not order:
            return None
        return Order.model_validate(order)
    
    async def cancel_order(self, order_id: int, cancel_data: OrderCancelRequest,
                          operator_id: Optional[int] = None, operator_name: Optional[str] = None) -> Optional[Order]:
        """取消订单"""
        order = await self.repository.update_order_status(
            order_id,
            new_status="cancelled",
            description=f"订单取消：{cancel_data.reason}",
            operator_id=operator_id,
            operator_name=operator_name
        )
        if not order:
            return None
        return Order.model_validate(order)
    
    async def delete_order(self, order_id: int) -> bool:
        """删除订单"""
        return await self.repository.delete_order(order_id)
    
    async def get_order_stats(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> OrderStats:
        """获取订单统计数据"""
        stats = await self.repository.get_order_stats(start_date, end_date)
        return OrderStats(**stats)
    
    # 支付相关服务
    async def create_payment(self, order_id: int, payment_method: str, amount: float,
                            transaction_id: Optional[str] = None, notes: Optional[str] = None) -> OrderPayment:
        """创建支付记录"""
        payment = await self.repository.create_payment(
            order_id=order_id,
            payment_method=payment_method,
            amount=amount,
            transaction_id=transaction_id,
            notes=notes
        )
        return OrderPayment.model_validate(payment)
    
    async def get_payments_by_order(self, order_id: int) -> List[OrderPayment]:
        """获取订单的所有支付记录"""
        payments = await self.repository.get_payments_by_order(order_id)
        return [OrderPayment.model_validate(payment) for payment in payments]
    
    # 退款相关服务
    async def create_refund(self, order_id: int, refund_type: str, refund_amount: float,
                           reason: Optional[str] = None, notes: Optional[str] = None) -> OrderRefund:
        """创建退款记录"""
        refund = await self.repository.create_refund(
            order_id=order_id,
            refund_type=refund_type,
            refund_amount=refund_amount,
            reason=reason,
            notes=notes
        )
        return OrderRefund.model_validate(refund)
    
    async def approve_refund(self, refund_id: int, processed_by: Optional[int] = None) -> Optional[OrderRefund]:
        """审批退款"""
        refund = await self.repository.update_refund_status(
            refund_id,
            refund_status="approved",
            processed_by=processed_by
        )
        if not refund:
            return None
        return OrderRefund.model_validate(refund)
    
    async def reject_refund(self, refund_id: int, reason: str, processed_by: Optional[int] = None) -> Optional[OrderRefund]:
        """拒绝退款"""
        refund = await self.repository.update_refund_status(
            refund_id,
            refund_status="rejected",
            processed_by=processed_by,
            notes=reason
        )
        if not refund:
            return None
        return OrderRefund.model_validate(refund)
    
    async def get_refunds_by_order(self, order_id: int) -> List[OrderRefund]:
        """获取订单的所有退款记录"""
        refunds = await self.repository.get_refunds_by_order(order_id)
        return [OrderRefund.model_validate(refund) for refund in refunds]
