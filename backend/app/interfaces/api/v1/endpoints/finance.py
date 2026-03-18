from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.application.services.finance_service import FinanceService
from app.schemas.finance import (
    AccountCreate, AccountUpdate, Account,
    TransactionCreate, TransactionUpdate, Transaction,
    InvoiceCreate, InvoiceUpdate, Invoice,
    FinancialReportCreate, FinancialReport, FinancialReportUpdate
)
from app.interfaces.api.deps import get_current_active_user
from app.models import User
from datetime import datetime

router = APIRouter(prefix="/finance", tags=["finance"])


# 账户相关接口
@router.post("/accounts", response_model=Account)
async def create_account(
    account: AccountCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建账户"""
    service = FinanceService(db)
    try:
        return await service.create_account(account)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/accounts", response_model=List[Account])
async def get_accounts(
    account_type: Optional[str] = Query(None, description="账户类型"),
    status: Optional[str] = Query(None, description="账户状态"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取账户列表"""
    service = FinanceService(db)
    return await service.get_accounts(account_type, status, skip, limit)


@router.get("/accounts/{account_id}", response_model=Account)
async def get_account(
    account_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取账户详情"""
    service = FinanceService(db)
    account = await service.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="账户不存在")
    return account


@router.put("/accounts/{account_id}", response_model=Account)
async def update_account(
    account_id: int,
    account: AccountUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新账户"""
    service = FinanceService(db)
    updated_account = await service.update_account(account_id, account)
    if not updated_account:
        raise HTTPException(status_code=404, detail="账户不存在")
    return updated_account


@router.delete("/accounts/{account_id}")
async def delete_account(
    account_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除账户"""
    service = FinanceService(db)
    deleted = await service.delete_account(account_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="账户不存在")
    return {"message": "账户删除成功"}


# 交易相关接口
@router.post("/transactions", response_model=Transaction)
async def create_transaction(
    transaction: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建交易"""
    service = FinanceService(db)
    try:
        return await service.create_transaction(transaction)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/transactions", response_model=List[Transaction])
async def get_transactions(
    account_id: Optional[int] = Query(None, description="账户ID"),
    type: Optional[str] = Query(None, description="交易类型"),
    status: Optional[str] = Query(None, description="交易状态"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取交易列表"""
    service = FinanceService(db)
    return await service.get_transactions(account_id, type, status, skip, limit)


@router.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取交易详情"""
    service = FinanceService(db)
    transaction = await service.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="交易不存在")
    return transaction


@router.put("/transactions/{transaction_id}", response_model=Transaction)
async def update_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新交易"""
    service = FinanceService(db)
    updated_transaction = await service.update_transaction(transaction_id, transaction)
    if not updated_transaction:
        raise HTTPException(status_code=404, detail="交易不存在")
    return updated_transaction


@router.delete("/transactions/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除交易"""
    service = FinanceService(db)
    deleted = await service.delete_transaction(transaction_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="交易不存在")
    return {"message": "交易删除成功"}


# 发票相关接口
@router.post("/invoices", response_model=Invoice)
async def create_invoice(
    invoice: InvoiceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建发票"""
    service = FinanceService(db)
    return await service.create_invoice(invoice)


@router.get("/invoices", response_model=List[Invoice])
async def get_invoices(
    account_id: Optional[int] = Query(None, description="账户ID"),
    status: Optional[str] = Query(None, description="发票状态"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取发票列表"""
    service = FinanceService(db)
    return await service.get_invoices(account_id, status, skip, limit)


@router.get("/invoices/{invoice_id}", response_model=Invoice)
async def get_invoice(
    invoice_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取发票详情"""
    service = FinanceService(db)
    invoice = await service.get_invoice(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="发票不存在")
    return invoice


@router.put("/invoices/{invoice_id}", response_model=Invoice)
async def update_invoice(
    invoice_id: int,
    invoice: InvoiceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新发票"""
    service = FinanceService(db)
    updated_invoice = await service.update_invoice(invoice_id, invoice)
    if not updated_invoice:
        raise HTTPException(status_code=404, detail="发票不存在")
    return updated_invoice


@router.delete("/invoices/{invoice_id}")
async def delete_invoice(
    invoice_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除发票"""
    service = FinanceService(db)
    deleted = await service.delete_invoice(invoice_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="发票不存在")
    return {"message": "发票删除成功"}


# 财务报表相关接口
@router.post("/reports", response_model=FinancialReport)
async def create_financial_report(
    report: FinancialReportCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建财务报表"""
    service = FinanceService(db)
    return await service.create_financial_report(report)


@router.post("/reports/income-statement", response_model=FinancialReport)
async def generate_income_statement(
    period_start: datetime = Query(..., description="开始日期"),
    period_end: datetime = Query(..., description="结束日期"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """生成利润表"""
    service = FinanceService(db)
    return await service.generate_income_statement(period_start, period_end)


@router.get("/reports", response_model=List[FinancialReport])
async def get_financial_reports(
    report_type: Optional[str] = Query(None, description="报表类型"),
    status: Optional[str] = Query(None, description="报表状态"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取财务报表列表"""
    service = FinanceService(db)
    return await service.get_financial_reports(report_type, status, skip, limit)


@router.get("/reports/{report_id}", response_model=FinancialReport)
async def get_financial_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取财务报表详情"""
    service = FinanceService(db)
    report = await service.get_financial_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="财务报表不存在")
    return report
