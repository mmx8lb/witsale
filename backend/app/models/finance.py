from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class Account(Base):
    """账户模型"""
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    type = Column(String(50), nullable=False, index=True)  # enterprise, customer, bank, etc.
    balance = Column(Float, default=0.0)
    currency = Column(String(10), default="CNY")
    status = Column(String(20), default="active", index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    transactions = relationship("Transaction", back_populates="account")
    invoices = relationship("Invoice", back_populates="account")


class Transaction(Base):
    """交易模型"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_no = Column(String(50), nullable=False, unique=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    type = Column(String(20), nullable=False, index=True)  # income, expense, transfer
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="CNY")
    status = Column(String(20), default="pending", index=True)  # pending, processing, completed, failed
    payment_method = Column(String(50), nullable=False)  # online, offline, credit, etc.
    reference_type = Column(String(50), nullable=True)  # order, refund, etc.
    reference_id = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    account = relationship("Account", back_populates="transactions")
    invoice = relationship("Invoice", back_populates="transaction")


class Invoice(Base):
    """发票模型"""
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_no = Column(String(50), nullable=False, unique=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="CNY")
    status = Column(String(20), default="draft", index=True)  # draft, issued, paid, cancelled
    issue_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    tax_amount = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    account = relationship("Account", back_populates="invoices")
    transaction = relationship("Transaction", back_populates="invoice")


class FinancialReport(Base):
    """财务报表模型"""
    __tablename__ = "financial_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    report_name = Column(String(100), nullable=False)
    report_type = Column(String(50), nullable=False, index=True)  # income_statement, balance_sheet, cash_flow
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    status = Column(String(20), default="generated", index=True)  # generated, processing, failed
    data = Column(Text, nullable=True)  # JSON format
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
