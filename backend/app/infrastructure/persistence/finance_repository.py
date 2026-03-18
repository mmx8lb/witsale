from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.finance import Account, Transaction, Invoice, FinancialReport


class FinanceRepository:
    """财务仓储层"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # 账户相关方法
    async def create_account(self, account: Account) -> Account:
        """创建账户"""
        self.db.add(account)
        await self.db.commit()
        await self.db.refresh(account)
        return account
    
    async def get_account(self, account_id: int) -> Optional[Account]:
        """根据ID获取账户"""
        result = await self.db.execute(select(Account).where(Account.id == account_id))
        return result.scalar_one_or_none()
    
    async def get_account_by_code(self, code: str) -> Optional[Account]:
        """根据代码获取账户"""
        result = await self.db.execute(select(Account).where(Account.code == code))
        return result.scalar_one_or_none()
    
    async def get_accounts(
        self,
        account_type: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Account]:
        """获取账户列表"""
        query = select(Account)
        if account_type:
            query = query.where(Account.type == account_type)
        if status:
            query = query.where(Account.status == status)
        result = await self.db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()
    
    async def update_account(self, account: Account) -> Account:
        """更新账户"""
        self.db.add(account)
        await self.db.commit()
        await self.db.refresh(account)
        return account
    
    async def delete_account(self, account_id: int) -> bool:
        """删除账户"""
        result = await self.db.execute(select(Account).where(Account.id == account_id))
        account = result.scalar_one_or_none()
        if account:
            await self.db.delete(account)
            await self.db.commit()
            return True
        return False
    
    # 交易相关方法
    async def create_transaction(self, transaction: Transaction) -> Transaction:
        """创建交易"""
        self.db.add(transaction)
        await self.db.commit()
        await self.db.refresh(transaction)
        return transaction
    
    async def get_transaction(self, transaction_id: int) -> Optional[Transaction]:
        """根据ID获取交易"""
        result = await self.db.execute(select(Transaction).where(Transaction.id == transaction_id))
        return result.scalar_one_or_none()
    
    async def get_transaction_by_no(self, transaction_no: str) -> Optional[Transaction]:
        """根据交易编号获取交易"""
        result = await self.db.execute(select(Transaction).where(Transaction.transaction_no == transaction_no))
        return result.scalar_one_or_none()
    
    async def get_transactions(
        self,
        account_id: Optional[int] = None,
        transaction_type: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Transaction]:
        """获取交易列表"""
        query = select(Transaction)
        if account_id:
            query = query.where(Transaction.account_id == account_id)
        if transaction_type:
            query = query.where(Transaction.type == transaction_type)
        if status:
            query = query.where(Transaction.status == status)
        result = await self.db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()
    
    async def update_transaction(self, transaction: Transaction) -> Transaction:
        """更新交易"""
        self.db.add(transaction)
        await self.db.commit()
        await self.db.refresh(transaction)
        return transaction
    
    async def delete_transaction(self, transaction_id: int) -> bool:
        """删除交易"""
        result = await self.db.execute(select(Transaction).where(Transaction.id == transaction_id))
        transaction = result.scalar_one_or_none()
        if transaction:
            await self.db.delete(transaction)
            await self.db.commit()
            return True
        return False
    
    # 发票相关方法
    async def create_invoice(self, invoice: Invoice) -> Invoice:
        """创建发票"""
        self.db.add(invoice)
        await self.db.commit()
        await self.db.refresh(invoice)
        return invoice
    
    async def get_invoice(self, invoice_id: int) -> Optional[Invoice]:
        """根据ID获取发票"""
        result = await self.db.execute(select(Invoice).where(Invoice.id == invoice_id))
        return result.scalar_one_or_none()
    
    async def get_invoice_by_no(self, invoice_no: str) -> Optional[Invoice]:
        """根据发票编号获取发票"""
        result = await self.db.execute(select(Invoice).where(Invoice.invoice_no == invoice_no))
        return result.scalar_one_or_none()
    
    async def get_invoices(
        self,
        account_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Invoice]:
        """获取发票列表"""
        query = select(Invoice)
        if account_id:
            query = query.where(Invoice.account_id == account_id)
        if status:
            query = query.where(Invoice.status == status)
        result = await self.db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()
    
    async def update_invoice(self, invoice: Invoice) -> Invoice:
        """更新发票"""
        self.db.add(invoice)
        await self.db.commit()
        await self.db.refresh(invoice)
        return invoice
    
    async def delete_invoice(self, invoice_id: int) -> bool:
        """删除发票"""
        result = await self.db.execute(select(Invoice).where(Invoice.id == invoice_id))
        invoice = result.scalar_one_or_none()
        if invoice:
            await self.db.delete(invoice)
            await self.db.commit()
            return True
        return False
    
    # 财务报表相关方法
    async def create_financial_report(self, report: FinancialReport) -> FinancialReport:
        """创建财务报表"""
        self.db.add(report)
        await self.db.commit()
        await self.db.refresh(report)
        return report
    
    async def get_financial_report(self, report_id: int) -> Optional[FinancialReport]:
        """根据ID获取财务报表"""
        result = await self.db.execute(select(FinancialReport).where(FinancialReport.id == report_id))
        return result.scalar_one_or_none()
    
    async def get_financial_reports(
        self,
        report_type: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[FinancialReport]:
        """获取财务报表列表"""
        query = select(FinancialReport)
        if report_type:
            query = query.where(FinancialReport.report_type == report_type)
        if status:
            query = query.where(FinancialReport.status == status)
        result = await self.db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()
    
    async def update_financial_report(self, report: FinancialReport) -> FinancialReport:
        """更新财务报表"""
        self.db.add(report)
        await self.db.commit()
        await self.db.refresh(report)
        return report
    
    async def delete_financial_report(self, report_id: int) -> bool:
        """删除财务报表"""
        result = await self.db.execute(select(FinancialReport).where(FinancialReport.id == report_id))
        report = result.scalar_one_or_none()
        if report:
            await self.db.delete(report)
            await self.db.commit()
            return True
        return False
