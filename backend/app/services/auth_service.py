from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User, Role, Permission
from app.schemas import UserCreate, LoginRequest
from app.core.security import verify_password, get_password_hash, create_access_token
from datetime import timedelta
from app.core.config import settings


class AuthService:
    """认证服务"""
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[User]:
        """验证用户"""
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        if not user.is_active:
            return None
        
        return user
    
    @staticmethod
    async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
        """创建用户"""
        # 检查角色是否存在
        result = await db.execute(select(Role).where(Role.id == user_in.role_id))
        role = result.scalar_one_or_none()
        if not role:
            raise ValueError(f"Role with id {user_in.role_id} not found")
        
        # 检查用户名是否已存在
        result = await db.execute(select(User).where(User.username == user_in.username))
        if result.scalar_one_or_none():
            raise ValueError(f"Username {user_in.username} already exists")
        
        # 检查邮箱是否已存在
        result = await db.execute(select(User).where(User.email == user_in.email))
        if result.scalar_one_or_none():
            raise ValueError(f"Email {user_in.email} already exists")
        
        # 处理密码长度，bcrypt限制72字节
        password = user_in.password[:72] if len(user_in.password) > 72 else user_in.password
        
        # 创建用户
        db_user = User(
            username=user_in.username,
            email=user_in.email,
            password_hash=get_password_hash(password),
            phone=user_in.phone,
            role_id=user_in.role_id
        )
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        """获取用户列表"""
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()
    
    @staticmethod
    async def create_access_token_for_user(user: User) -> str:
        """为用户创建访问令牌"""
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "username": user.username},
            expires_delta=access_token_expires
        )
        return access_token


# 创建全局认证服务实例
auth_service = AuthService()
