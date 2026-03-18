from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Role, Permission


async def init_default_roles_and_permissions(db: AsyncSession):
    """初始化默认角色和权限"""
    # 检查是否已有角色
    from sqlalchemy.future import select
    result = await db.execute(select(Role))
    existing_roles = result.scalars().all()
    
    if existing_roles:
        return  # 已有角色，跳过初始化
    
    # 创建默认权限
    default_permissions = [
        Permission(name="查看用户", code="USER_READ"),
        Permission(name="创建用户", code="USER_CREATE"),
        Permission(name="更新用户", code="USER_UPDATE"),
        Permission(name="删除用户", code="USER_DELETE"),
        Permission(name="查看角色", code="ROLE_READ"),
        Permission(name="创建角色", code="ROLE_CREATE"),
        Permission(name="更新角色", code="ROLE_UPDATE"),
        Permission(name="删除角色", code="ROLE_DELETE"),
        Permission(name="查看权限", code="PERMISSION_READ"),
        Permission(name="创建权限", code="PERMISSION_CREATE"),
        Permission(name="更新权限", code="PERMISSION_UPDATE"),
        Permission(name="删除权限", code="PERMISSION_DELETE"),
    ]
    
    for permission in default_permissions:
        db.add(permission)
    
    await db.flush()  # 刷新以获取权限ID
    
    # 创建默认角色
    admin_role = Role(name="admin", description="系统管理员")
    user_role = Role(name="user", description="普通用户")
    
    # 给管理员角色分配所有权限
    admin_role.permissions = default_permissions
    
    # 给普通用户分配基本权限
    user_role.permissions = [p for p in default_permissions if p.code.endswith("_READ")]
    
    db.add(admin_role)
    db.add(user_role)
    
    await db.commit()
