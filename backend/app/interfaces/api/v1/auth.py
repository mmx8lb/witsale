from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas import (
    User, UserCreate, UserUpdate, LoginRequest, LoginResponse, Token,
    Role, RoleCreate, RoleUpdate, Permission, PermissionCreate, PermissionUpdate
)
from app.services.auth_service import auth_service
from app.interfaces.api.deps import get_current_active_user
from app.models import User as UserModel, Role as RoleModel, Permission as PermissionModel
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """用户登录"""
    user = await auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = await auth_service.create_access_token_for_user(user)
    
    # 加载用户角色信息，使用selectinload预加载权限
    result = await db.execute(
        select(UserModel).options(
            selectinload(UserModel.role).selectinload(RoleModel.permissions)
        ).where(UserModel.id == user.id)
    )
    user_with_role = result.scalar_one()
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=30 * 60,  # 30分钟
        user=user_with_role
    )


@router.post("/register", response_model=User)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """用户注册"""
    try:
        user = await auth_service.create_user(db, user_in)
        
        # 加载用户角色信息，使用selectinload预加载权限
        result = await db.execute(
            select(UserModel).options(
                selectinload(UserModel.role).selectinload(RoleModel.permissions)
            ).where(UserModel.id == user.id)
        )
        user_with_role = result.scalar_one()
        
        return user_with_role
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取当前用户信息"""
    # 加载用户角色信息，使用selectinload预加载权限
    result = await db.execute(
        select(UserModel).options(
            selectinload(UserModel.role).selectinload(RoleModel.permissions)
        ).where(UserModel.id == current_user.id)
    )
    user_with_role = result.scalar_one()
    return user_with_role


@router.get("/users", response_model=List[User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """获取用户列表"""
    # 使用selectinload预加载角色和权限
    result = await db.execute(
        select(UserModel).options(
            selectinload(UserModel.role).selectinload(RoleModel.permissions)
        ).offset(skip).limit(limit)
    )
    users = result.scalars().all()
    return users


@router.get("/roles", response_model=List[Role])
async def get_roles(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """获取角色列表"""
    # 使用selectinload预加载权限
    result = await db.execute(
        select(RoleModel).options(selectinload(RoleModel.permissions))
    )
    roles = result.scalars().all()
    return roles


@router.post("/roles", response_model=Role)
async def create_role(
    role_in: RoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """创建角色"""
    # 检查角色名称是否已存在
    result = await db.execute(select(RoleModel).where(RoleModel.name == role_in.name))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role name {role_in.name} already exists"
        )
    
    db_role = RoleModel(
        name=role_in.name,
        description=role_in.description
    )
    
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    return db_role


@router.get("/permissions", response_model=List[Permission])
async def get_permissions(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """获取权限列表"""
    result = await db.execute(select(PermissionModel))
    return result.scalars().all()


@router.post("/permissions", response_model=Permission)
async def create_permission(
    permission_in: PermissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """创建权限"""
    # 检查权限名称是否已存在
    result = await db.execute(select(PermissionModel).where(PermissionModel.name == permission_in.name))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Permission name {permission_in.name} already exists"
        )
    
    # 检查权限代码是否已存在
    result = await db.execute(select(PermissionModel).where(PermissionModel.code == permission_in.code))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Permission code {permission_in.code} already exists"
        )
    
    db_permission = PermissionModel(
        name=permission_in.name,
        code=permission_in.code,
        description=permission_in.description
    )
    
    db.add(db_permission)
    await db.commit()
    await db.refresh(db_permission)
    return db_permission
