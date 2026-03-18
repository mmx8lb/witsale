from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class AccountBase(BaseModel):
    """账户基础模型"""
    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=50)
    type: str = Field(..., min_length=1, max_length=50)
    balance: float = Field(default=0.0, ge=0.0)
    currency: str = Field(default="CNY", max_length=10)
    status: str = Field(default="active", max_length=20)
    description: Optional[str] = None


class AccountCreate(AccountBase):
    """账户创建模型"""
    pass


class AccountUpdate(BaseModel):
    """账户更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    type: Optional[str] = Field(None, min_length=1, max_length=50)
    balance: Optional[float] = Field(None, ge=0.0)
    currency: Optional[str] = Field(None, max_length=10)
    status: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None


class AccountInDB(AccountBase):
    """数据库中的账户模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Account(AccountInDB):
    """账户响应模型"""
    pass


class TransactionBase(BaseModel):
    """交易基础模型"""
    account_id: int
    type: str = Field(..., min_length=1, max_length=20)
    amount: float = Field(..., gt=0.0)
    currency: str = Field(default="CNY", max_length=10)
    payment_method: str = Field(..., min_length=1, max_length=50)
    reference_type: Optional[str] = Field(None, max_length=50)
    reference_id: Optional[int] = None
    notes: Optional[str] = None


class TransactionCreate(TransactionBase):
    """交易创建模型"""
    pass


class TransactionUpdate(BaseModel):
    """交易更新模型"""
    account_id: Optional[int] = None
    type: Optional[str] = Field(None, min_length=1, max_length=20)
    amount: Optional[float] = Field(None, gt=0.0)
    currency: Optional[str] = Field(None, max_length=10)
    status: Optional[str] = Field(None, max_length=20)
    payment_method: Optional[str] = Field(None, min_length=1, max_length=50)
    reference_type: Optional[str] = Field(None, max_length=50)
    reference_id: Optional[int] = None
    notes: Optional[str] = None


class TransactionInDB(TransactionBase):
    """数据库中的交易模型"""
    id: int
    transaction_no: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Transaction(TransactionInDB):
    """交易响应模型"""
    account: Optional[Account] = None


class InvoiceBase(BaseModel):
    """发票基础模型"""
    account_id: int
    transaction_id: Optional[int] = None
    amount: float = Field(..., gt=0.0)
    currency: str = Field(default="CNY", max_length=10)
    status: str = Field(default="draft", max_length=20)
    due_date: Optional[datetime] = None
    tax_amount: float = Field(default=0.0, ge=0.0)
    total_amount: float = Field(..., gt=0.0)
    notes: Optional[str] = None


class InvoiceCreate(InvoiceBase):
    """发票创建模型"""
    pass


class InvoiceUpdate(BaseModel):
    """发票更新模型"""
    account_id: Optional[int] = None
    transaction_id: Optional[int] = None
    amount: Optional[float] = Field(None, gt=0.0)
    currency: Optional[str] = Field(None, max_length=10)
    status: Optional[str] = Field(None, max_length=20)
    due_date: Optional[datetime] = None
    tax_amount: Optional[float] = Field(None, ge=0.0)
    total_amount: Optional[float] = Field(None, gt=0.0)
    notes: Optional[str] = None


class InvoiceInDB(InvoiceBase):
    """数据库中的发票模型"""
    id: int
    invoice_no: str
    issue_date: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Invoice(InvoiceInDB):
    """发票响应模型"""
    account: Optional[Account] = None
    transaction: Optional[Transaction] = None


class FinancialReportBase(BaseModel):
    """财务报表基础模型"""
    report_name: str = Field(..., min_length=1, max_length=100)
    report_type: str = Field(..., min_length=1, max_length=50)
    period_start: datetime
    period_end: datetime
    data: Optional[str] = None


class FinancialReportCreate(FinancialReportBase):
    """财务报表创建模型"""
    pass


class FinancialReportUpdate(BaseModel):
    """财务报表更新模型"""
    report_name: Optional[str] = Field(None, min_length=1, max_length=100)
    report_type: Optional[str] = Field(None, min_length=1, max_length=50)
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    status: Optional[str] = Field(None, max_length=20)
    data: Optional[str] = None


class FinancialReportInDB(FinancialReportBase):
    """数据库中的财务报表模型"""
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class FinancialReport(FinancialReportInDB):
    """财务报表响应模型"""
    pass
