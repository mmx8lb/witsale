from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, JSON, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


# 客户-标签关联表
customer_tag_relation = Table(
    'customer_tag_relations',
    Base.metadata,
    Column('customer_id', Integer, ForeignKey('customers.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('customer_tags.id'), primary_key=True),
    Column('created_at', DateTime, default=datetime.utcnow)
)


class CustomerCategory(Base):
    """客户分类模型"""
    __tablename__ = "customer_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    parent_category_id = Column(Integer, ForeignKey('customer_categories.id'), nullable=True)
    level = Column(Integer, nullable=False, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    parent = relationship("CustomerCategory", remote_side=[id], backref="children")
    customers = relationship("Customer", back_populates="category")


class CustomerLevel(Base):
    """客户等级模型"""
    __tablename__ = "customer_levels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    min_spend = Column(Float, nullable=False, default=0.0)
    max_spend = Column(Float, nullable=True)
    discount_rate = Column(Float, nullable=False, default=1.0)
    priority = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    customers = relationship("Customer", back_populates="level")


class Customer(Base):
    """客户模型"""
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), nullable=False, unique=True, index=True)
    short_name = Column(String(100), nullable=True)
    type = Column(String(20), nullable=False, default="enterprise")  # enterprise, individual, etc.
    category_id = Column(Integer, ForeignKey('customer_categories.id'), nullable=True)
    level_id = Column(Integer, ForeignKey('customer_levels.id'), nullable=True)
    contact_name = Column(String(100), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)
    website = Column(String(200), nullable=True)
    tax_no = Column(String(50), nullable=True)
    registered_capital = Column(Float, nullable=True)
    business_scope = Column(Text, nullable=True)
    founding_date = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False, default="active")  # active, inactive, suspended
    total_spend = Column(Float, nullable=False, default=0.0)
    total_orders = Column(Integer, nullable=False, default=0)
    credit_limit = Column(Float, nullable=True)
    credit_balance = Column(Float, nullable=False, default=0.0)
    remark = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    category = relationship("CustomerCategory", back_populates="customers")
    level = relationship("CustomerLevel", back_populates="customers")
    contacts = relationship("CustomerContact", back_populates="customer", cascade="all, delete-orphan")
    addresses = relationship("CustomerAddress", back_populates="customer", cascade="all, delete-orphan")
    tags = relationship("CustomerTag", secondary=customer_tag_relation, back_populates="customers")


class CustomerContact(Base):
    """客户联系人模型"""
    __tablename__ = "customer_contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    name = Column(String(100), nullable=False)
    position = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=False)
    email = Column(String(100), nullable=True)
    is_primary = Column(Boolean, default=False)
    remark = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    customer = relationship("Customer", back_populates="contacts")


class CustomerAddress(Base):
    """客户地址模型"""
    __tablename__ = "customer_addresses"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    type = Column(String(20), nullable=False, default="billing")  # billing, shipping, etc.
    province = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    address = Column(String(500), nullable=False)
    zip_code = Column(String(20), nullable=True)
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    customer = relationship("Customer", back_populates="addresses")


class CustomerTag(Base):
    """客户标签模型"""
    __tablename__ = "customer_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    color = Column(String(20), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    customers = relationship("Customer", secondary=customer_tag_relation, back_populates="tags")
