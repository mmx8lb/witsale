from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.finance import Account, Transaction, Invoice, FinancialReport
from app.schemas.finance import (
    AccountCreate, AccountUpdate, Account as AccountSchema,
    TransactionCreate, TransactionUpdate, Transaction as TransactionSchema,
    InvoiceCreate, InvoiceUpdate, Invoice as InvoiceSchema,
    FinancialReportCreate, FinancialReportUpdate, FinancialReport as FinancialReportSchema
)
from app.infrastructure.persistence.finance_repository import FinanceRepository
import json


class FinanceService:
    """财务服务层"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = FinanceRepository(db)
    
    # 账户相关方法
    async def create_account(self, account_in: AccountCreate) -> AccountSchema:
        """创建账户"""
        # 检查账户代码是否已存在
        existing_account = await self.repository.get_account_by_code(account_in.code)
        if existing_account:
            raise ValueError(f"Account with code {account_in.code} already exists")
        
        # 创建账户
        account = Account(
            name=account_in.name,
            code=account_in.code,
            type=account_in.type,
            balance=account_in.balance,
            currency=account_in.currency,
            status=account_in.status,
            description=account_in.description
        )
        
        created_account = await self.repository.create_account(account)
        return AccountSchema.model_validate(created_account)
    
    async def get_account(self, account_id: int) -> Optional[AccountSchema]:
        """根据ID获取账户"""
        account = await self.repository.get_account(account_id)
        if account:
            return AccountSchema.model_validate(account)
        return None
    
    async def get_accounts(
        self,
        account_type: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AccountSchema]:
        """获取账户列表"""
        accounts = await self.repository.get_accounts(account_type, status, skip, limit)
        return [AccountSchema.model_validate(account) for account in accounts]
    
    async def update_account(self, account_id: int, account_in: AccountUpdate) -> Optional[AccountSchema]:
        """更新账户"""
        account = await self.repository.get_account(account_id)
        if not account:
            return None
        
        # 更新账户信息
        update_data = account_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(account, field, value)
        
        updated_account = await self.repository.update_account(account)
        return AccountSchema.model_validate(updated_account)
    
    async def delete_account(self, account_id: int) -> bool:
        """删除账户"""
        return await self.repository.delete_account(account_id)
    
    # 交易相关方法
    async def create_transaction(self, transaction_in: TransactionCreate) -> TransactionSchema:
        """创建交易"""
        # 生成交易编号
        transaction_no = self._generate_transaction_no()
        
        # 创建交易
        transaction = Transaction(
            transaction_no=transaction_no,
            account_id=transaction_in.account_id,
            type=transaction_in.type,
            amount=transaction_in.amount,
            currency=transaction_in.currency,
            status="pending",
            payment_method=transaction_in.payment_method,
            reference_type=transaction_in.reference_type,
            reference_id=transaction_in.reference_id,
            notes=transaction_in.notes
        )
        
        # 创建交易
        created_transaction = await self.repository.create_transaction(transaction)
        
        # 更新账户余额
        account = await self.repository.get_account(transaction_in.account_id)
        if account:
            if transaction_in.type == "income":
                account.balance += transaction_in.amount
            elif transaction_in.type == "expense":
                if account.balance < transaction_in.amount:
                    raise ValueError("Insufficient account balance")
                account.balance -= transaction_in.amount
            await self.repository.update_account(account)
        
        # 更新交易状态为完成
        created_transaction.status = "completed"
        updated_transaction = await self.repository.update_transaction(created_transaction)
        
        # 手动构建响应对象，避免加载关联关系
        return TransactionSchema(
            id=updated_transaction.id,
            transaction_no=updated_transaction.transaction_no,
            account_id=updated_transaction.account_id,
            type=updated_transaction.type,
            amount=updated_transaction.amount,
            currency=updated_transaction.currency,
            status=updated_transaction.status,
            payment_method=updated_transaction.payment_method,
            reference_type=updated_transaction.reference_type,
            reference_id=updated_transaction.reference_id,
            notes=updated_transaction.notes,
            created_at=updated_transaction.created_at,
            updated_at=updated_transaction.updated_at,
            account=None
        )
    
    async def get_transaction(self, transaction_id: int) -> Optional[TransactionSchema]:
        """根据ID获取交易"""
        transaction = await self.repository.get_transaction(transaction_id)
        if transaction:
            # 手动构建响应对象，避免加载关联关系
            return TransactionSchema(
                id=transaction.id,
                transaction_no=transaction.transaction_no,
                account_id=transaction.account_id,
                type=transaction.type,
                amount=transaction.amount,
                currency=transaction.currency,
                status=transaction.status,
                payment_method=transaction.payment_method,
                reference_type=transaction.reference_type,
                reference_id=transaction.reference_id,
                notes=transaction.notes,
                created_at=transaction.created_at,
                updated_at=transaction.updated_at,
                account=None
            )
        return None
    
    async def get_transactions(
        self,
        account_id: Optional[int] = None,
        transaction_type: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[TransactionSchema]:
        """获取交易列表"""
        transactions = await self.repository.get_transactions(account_id, transaction_type, status, skip, limit)
        # 手动构建响应对象，避免加载关联关系
        return [
            TransactionSchema(
                id=transaction.id,
                transaction_no=transaction.transaction_no,
                account_id=transaction.account_id,
                type=transaction.type,
                amount=transaction.amount,
                currency=transaction.currency,
                status=transaction.status,
                payment_method=transaction.payment_method,
                reference_type=transaction.reference_type,
                reference_id=transaction.reference_id,
                notes=transaction.notes,
                created_at=transaction.created_at,
                updated_at=transaction.updated_at,
                account=None
            )
            for transaction in transactions
        ]
    
    async def update_transaction(self, transaction_id: int, transaction_in: TransactionUpdate) -> Optional[TransactionSchema]:
        """更新交易"""
        transaction = await self.repository.get_transaction(transaction_id)
        if not transaction:
            return None
        
        # 更新交易信息
        update_data = transaction_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(transaction, field, value)
        
        updated_transaction = await self.repository.update_transaction(transaction)
        # 手动构建响应对象，避免加载关联关系
        return TransactionSchema(
            id=updated_transaction.id,
            transaction_no=updated_transaction.transaction_no,
            account_id=updated_transaction.account_id,
            type=updated_transaction.type,
            amount=updated_transaction.amount,
            currency=updated_transaction.currency,
            status=updated_transaction.status,
            payment_method=updated_transaction.payment_method,
            reference_type=updated_transaction.reference_type,
            reference_id=updated_transaction.reference_id,
            notes=updated_transaction.notes,
            created_at=updated_transaction.created_at,
            updated_at=updated_transaction.updated_at,
            account=None
        )
    
    async def delete_transaction(self, transaction_id: int) -> bool:
        """删除交易"""
        return await self.repository.delete_transaction(transaction_id)
    
    # 发票相关方法
    async def create_invoice(self, invoice_in: InvoiceCreate) -> InvoiceSchema:
        """创建发票"""
        # 生成发票编号
        invoice_no = self._generate_invoice_no()
        
        # 创建发票
        invoice = Invoice(
            invoice_no=invoice_no,
            account_id=invoice_in.account_id,
            transaction_id=invoice_in.transaction_id,
            amount=invoice_in.amount,
            currency=invoice_in.currency,
            status=invoice_in.status,
            due_date=invoice_in.due_date,
            tax_amount=invoice_in.tax_amount,
            total_amount=invoice_in.total_amount,
            notes=invoice_in.notes
        )
        
        created_invoice = await self.repository.create_invoice(invoice)
        
        # 手动构建响应对象，避免加载关联关系
        return InvoiceSchema(
            id=created_invoice.id,
            invoice_no=created_invoice.invoice_no,
            account_id=created_invoice.account_id,
            transaction_id=created_invoice.transaction_id,
            amount=created_invoice.amount,
            currency=created_invoice.currency,
            status=created_invoice.status,
            due_date=created_invoice.due_date,
            tax_amount=created_invoice.tax_amount,
            total_amount=created_invoice.total_amount,
            notes=created_invoice.notes,
            issue_date=created_invoice.issue_date,
            created_at=created_invoice.created_at,
            updated_at=created_invoice.updated_at,
            account=None,
            transaction=None
        )
    
    async def get_invoice(self, invoice_id: int) -> Optional[InvoiceSchema]:
        """根据ID获取发票"""
        invoice = await self.repository.get_invoice(invoice_id)
        if invoice:
            # 手动构建响应对象，避免加载关联关系
            return InvoiceSchema(
                id=invoice.id,
                invoice_no=invoice.invoice_no,
                account_id=invoice.account_id,
                transaction_id=invoice.transaction_id,
                amount=invoice.amount,
                currency=invoice.currency,
                status=invoice.status,
                due_date=invoice.due_date,
                tax_amount=invoice.tax_amount,
                total_amount=invoice.total_amount,
                notes=invoice.notes,
                issue_date=invoice.issue_date,
                created_at=invoice.created_at,
                updated_at=invoice.updated_at,
                account=None,
                transaction=None
            )
        return None
    
    async def get_invoices(
        self,
        account_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[InvoiceSchema]:
        """获取发票列表"""
        invoices = await self.repository.get_invoices(account_id, status, skip, limit)
        # 手动构建响应对象，避免加载关联关系
        return [
            InvoiceSchema(
                id=invoice.id,
                invoice_no=invoice.invoice_no,
                account_id=invoice.account_id,
                transaction_id=invoice.transaction_id,
                amount=invoice.amount,
                currency=invoice.currency,
                status=invoice.status,
                due_date=invoice.due_date,
                tax_amount=invoice.tax_amount,
                total_amount=invoice.total_amount,
                notes=invoice.notes,
                issue_date=invoice.issue_date,
                created_at=invoice.created_at,
                updated_at=invoice.updated_at,
                account=None,
                transaction=None
            )
            for invoice in invoices
        ]
    
    async def update_invoice(self, invoice_id: int, invoice_in: InvoiceUpdate) -> Optional[InvoiceSchema]:
        """更新发票"""
        invoice = await self.repository.get_invoice(invoice_id)
        if not invoice:
            return None
        
        # 更新发票信息
        update_data = invoice_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(invoice, field, value)
        
        updated_invoice = await self.repository.update_invoice(invoice)
        # 手动构建响应对象，避免加载关联关系
        return InvoiceSchema(
            id=updated_invoice.id,
            invoice_no=updated_invoice.invoice_no,
            account_id=updated_invoice.account_id,
            transaction_id=updated_invoice.transaction_id,
            amount=updated_invoice.amount,
            currency=updated_invoice.currency,
            status=updated_invoice.status,
            due_date=updated_invoice.due_date,
            tax_amount=updated_invoice.tax_amount,
            total_amount=updated_invoice.total_amount,
            notes=updated_invoice.notes,
            issue_date=updated_invoice.issue_date,
            created_at=updated_invoice.created_at,
            updated_at=updated_invoice.updated_at,
            account=None,
            transaction=None
        )
    
    async def delete_invoice(self, invoice_id: int) -> bool:
        """删除发票"""
        return await self.repository.delete_invoice(invoice_id)
    
    # 财务报表相关方法
    async def create_financial_report(self, report_in: FinancialReportCreate) -> FinancialReportSchema:
        """创建财务报表"""
        # 创建财务报表
        report = FinancialReport(
            report_name=report_in.report_name,
            report_type=report_in.report_type,
            period_start=report_in.period_start,
            period_end=report_in.period_end,
            status="generated",
            data=report_in.data
        )
        
        created_report = await self.repository.create_financial_report(report)
        return FinancialReportSchema.model_validate(created_report)
    
    async def generate_income_statement(self, period_start: datetime, period_end: datetime) -> FinancialReportSchema:
        """生成利润表"""
        # 获取指定期间的交易数据
        transactions = await self.repository.get_transactions()
        
        # 计算收入和支出
        income = sum(t.amount for t in transactions if t.type == "income" and period_start <= t.created_at <= period_end)
        expense = sum(t.amount for t in transactions if t.type == "expense" and period_start <= t.created_at <= period_end)
        profit = income - expense
        
        # 生成报表数据
        report_data = {
            "period": {
                "start": period_start.isoformat(),
                "end": period_end.isoformat()
            },
            "income": income,
            "expense": expense,
            "profit": profit
        }
        
        # 创建财务报表
        report = FinancialReport(
            report_name=f"利润表_{period_start.strftime('%Y%m%d')}_{period_end.strftime('%Y%m%d')}",
            report_type="income_statement",
            period_start=period_start,
            period_end=period_end,
            status="generated",
            data=json.dumps(report_data)
        )
        
        created_report = await self.repository.create_financial_report(report)
        return FinancialReportSchema.model_validate(created_report)
    
    async def get_financial_report(self, report_id: int) -> Optional[FinancialReportSchema]:
        """根据ID获取财务报表"""
        report = await self.repository.get_financial_report(report_id)
        if report:
            return FinancialReportSchema.model_validate(report)
        return None
    
    async def get_financial_reports(
        self,
        report_type: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[FinancialReportSchema]:
        """获取财务报表列表"""
        reports = await self.repository.get_financial_reports(report_type, status, skip, limit)
        return [FinancialReportSchema.model_validate(report) for report in reports]
    
    # 辅助方法
    def _generate_transaction_no(self) -> str:
        """生成交易编号"""
        import uuid
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        random_suffix = uuid.uuid4().hex[:4]
        return f"TRA{timestamp}{random_suffix}"
    
    def _generate_invoice_no(self) -> str:
        """生成发票编号"""
        import uuid
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        random_suffix = uuid.uuid4().hex[:4]
        return f"INV{timestamp}{random_suffix}"
