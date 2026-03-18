from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.application.services.order_service import OrderService
from app.schemas.order import (
    OrderCreate, OrderUpdate, Order, OrderList,
    OrderItem, OrderPayment, OrderRefund,
    OrderStats, OrderStatusUpdate,
    OrderPaymentRequest, OrderShipRequest, OrderCancelRequest
)
from app.interfaces.api.deps import get_current_active_user
from app.models import User

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=Order)
async def create_order(
    order: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建订单"""
    service = OrderService(db)
    return await service.create_order(order, created_by=current_user.id)


@router.get("", response_model=List[OrderList])
async def get_orders(
    customer_id: Optional[int] = Query(None, description="客户ID"),
    order_status: Optional[str] = Query(None, description="订单状态"),
    payment_status: Optional[str] = Query(None, description="支付状态"),
    order_type: Optional[str] = Query(None, description="订单类型"),
    order_level: Optional[str] = Query(None, description="订单级别"),
    start_date: Optional[datetime] = Query(None, description="开始日期"),
    end_date: Optional[datetime] = Query(None, description="结束日期"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取订单列表"""
    service = OrderService(db)
    return await service.get_orders(
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


@router.get("/{order_id}", response_model=Order)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取订单详情"""
    service = OrderService(db)
    order = await service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return order


@router.get("/no/{order_no}", response_model=Order)
async def get_order_by_no(
    order_no: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """根据订单号获取订单"""
    service = OrderService(db)
    order = await service.get_order_by_no(order_no)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return order


@router.put("/{order_id}", response_model=Order)
async def update_order(
    order_id: int,
    order: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新订单"""
    service = OrderService(db)
    updated_order = await service.update_order(order_id, order)
    if not updated_order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return updated_order


@router.post("/{order_id}/status", response_model=Order)
async def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新订单状态"""
    service = OrderService(db)
    updated_order = await service.update_order_status(
        order_id,
        status_data,
        operator_id=current_user.id,
        operator_name=current_user.username
    )
    if not updated_order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return updated_order


@router.post("/{order_id}/pay", response_model=Order)
async def pay_order(
    order_id: int,
    payment_data: OrderPaymentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """订单支付"""
    service = OrderService(db)
    updated_order = await service.pay_order(
        order_id,
        payment_data,
        operator_id=current_user.id
    )
    if not updated_order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return updated_order


@router.post("/{order_id}/ship", response_model=Order)
async def ship_order(
    order_id: int,
    ship_data: OrderShipRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """订单发货"""
    service = OrderService(db)
    updated_order = await service.ship_order(
        order_id,
        ship_data,
        operator_id=current_user.id,
        operator_name=current_user.username
    )
    if not updated_order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return updated_order


@router.post("/{order_id}/confirm", response_model=Order)
async def confirm_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """确认收货"""
    service = OrderService(db)
    updated_order = await service.confirm_order(
        order_id,
        operator_id=current_user.id,
        operator_name=current_user.username
    )
    if not updated_order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return updated_order


@router.post("/{order_id}/cancel", response_model=Order)
async def cancel_order(
    order_id: int,
    cancel_data: OrderCancelRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """取消订单"""
    service = OrderService(db)
    updated_order = await service.cancel_order(
        order_id,
        cancel_data,
        operator_id=current_user.id,
        operator_name=current_user.username
    )
    if not updated_order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return updated_order


@router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除订单"""
    service = OrderService(db)
    deleted = await service.delete_order(order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="订单不存在")
    return {"message": "订单删除成功"}


@router.get("/stats/summary", response_model=OrderStats)
async def get_order_stats(
    start_date: Optional[datetime] = Query(None, description="开始日期"),
    end_date: Optional[datetime] = Query(None, description="结束日期"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取订单统计数据"""
    service = OrderService(db)
    return await service.get_order_stats(start_date, end_date)


@router.get("/{order_id}/payments", response_model=List[OrderPayment])
async def get_order_payments(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取订单的支付记录"""
    service = OrderService(db)
    return await service.get_payments_by_order(order_id)


@router.get("/{order_id}/refunds", response_model=List[OrderRefund])
async def get_order_refunds(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取订单的退款记录"""
    service = OrderService(db)
    return await service.get_refunds_by_order(order_id)


@router.post("/{order_id}/refunds", response_model=OrderRefund)
async def create_refund(
    order_id: int,
    refund_type: str = Query(..., description="退款类型"),
    refund_amount: float = Query(..., description="退款金额"),
    reason: Optional[str] = Query(None, description="退款原因"),
    notes: Optional[str] = Query(None, description="备注"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建退款申请"""
    service = OrderService(db)
    return await service.create_refund(order_id, refund_type, refund_amount, reason, notes)


@router.post("/refunds/{refund_id}/approve", response_model=OrderRefund)
async def approve_refund(
    refund_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """审批退款"""
    service = OrderService(db)
    refund = await service.approve_refund(refund_id, processed_by=current_user.id)
    if not refund:
        raise HTTPException(status_code=404, detail="退款记录不存在")
    return refund


@router.post("/refunds/{refund_id}/reject", response_model=OrderRefund)
async def reject_refund(
    refund_id: int,
    reason: str = Query(..., description="拒绝原因"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """拒绝退款"""
    service = OrderService(db)
    refund = await service.reject_refund(refund_id, reason, processed_by=current_user.id)
    if not refund:
        raise HTTPException(status_code=404, detail="退款记录不存在")
    return refund
