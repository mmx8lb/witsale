import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.core.config import settings
from app.main import app
from app.models import User, Role
from app.services.auth_service import auth_service
from app.schemas import UserCreate
from app.schemas.product import (
    CategoryCreate, CategoryUpdate, Category,
    ProductCreate, ProductUpdate, Product,
    ProductSKUCreate, ProductSKUUpdate, ProductSKU,
    ProductPriceCreate, ProductPriceUpdate, ProductPrice,
    ProductAttributeCreate, ProductAttribute
)

# 创建测试数据库引擎
# 替换为异步数据库URL格式
async_db_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(
    async_db_url,
    echo=False
)

# 创建测试会话工厂
TestingSessionLocal = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 覆盖依赖项
def override_get_db():
    async def _get_db():
        async with TestingSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()
    return _get_db

app.dependency_overrides[get_db] = override_get_db()

@pytest.fixture(scope="module", autouse=True)
async def setup_database():
    """设置测试数据库"""
    # 创建所有表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 创建测试角色
    async with TestingSessionLocal() as session:
        # 创建管理员角色
        admin_role = Role(name="admin", description="管理员")
        session.add(admin_role)
        await session.commit()
        await session.refresh(admin_role)
        
        # 创建测试用户
        test_user = UserCreate(
            username="test_user",
            email="test@example.com",
            password="test_password",
            phone="13800138000",
            role_id=admin_role.id
        )
        await auth_service.create_user(session, test_user)
    
    yield
    
    # 清理数据库
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def get_token():
    """获取测试用户的token"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/auth/login",
            data={"username": "test_user", "password": "test_password"}
        )
        assert response.status_code == 200
        return response.json()["access_token"]


# 分类测试
def test_create_category(get_token):
    """测试创建分类"""
    response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "测试分类", "parent_id": None, "level": 1, "sort": 0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "测试分类"
    assert data["parent_id"] is None
    assert data["level"] == 1


def test_get_categories(get_token):
    """测试获取分类列表"""
    response = client.get(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_category(get_token):
    """测试获取分类详情"""
    # 先创建一个分类
    create_response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "测试分类2", "parent_id": None, "level": 1, "sort": 1}
    )
    category_id = create_response.json()["id"]
    
    # 获取分类详情
    response = client.get(
        f"/api/v1/products/categories/{category_id}",
        headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == category_id
    assert data["name"] == "测试分类2"


def test_update_category(get_token):
    """测试更新分类"""
    # 先创建一个分类
    create_response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "测试分类3", "parent_id": None, "level": 1, "sort": 2}
    )
    category_id = create_response.json()["id"]
    
    # 更新分类
    response = client.put(
        f"/api/v1/products/categories/{category_id}",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "更新后的分类", "sort": 3}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == category_id
    assert data["name"] == "更新后的分类"
    assert data["sort"] == 3


def test_delete_category(get_token):
    """测试删除分类"""
    # 先创建一个分类
    create_response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "测试分类4", "parent_id": None, "level": 1, "sort": 4}
    )
    category_id = create_response.json()["id"]
    
    # 删除分类
    response = client.delete(
        f"/api/v1/products/categories/{category_id}",
        headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "分类删除成功"


# 商品测试
def test_create_product(get_token):
    """测试创建商品"""
    # 先创建一个分类
    create_category_response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "商品分类", "parent_id": None, "level": 1, "sort": 0}
    )
    category_id = create_category_response.json()["id"]
    
    # 创建商品
    response = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "name": "测试商品",
            "description": "测试商品描述",
            "category_id": category_id,
            "brand": "测试品牌",
            "model": "测试型号",
            "is_active": True
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "测试商品"
    assert data["category_id"] == category_id


def test_get_products(get_token):
    """测试获取商品列表"""
    response = client.get(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_product(get_token):
    """测试获取商品详情"""
    # 先创建一个分类
    create_category_response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "商品分类2", "parent_id": None, "level": 1, "sort": 1}
    )
    category_id = create_category_response.json()["id"]
    
    # 创建商品
    create_response = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "name": "测试商品2",
            "description": "测试商品描述2",
            "category_id": category_id,
            "brand": "测试品牌",
            "model": "测试型号",
            "is_active": True
        }
    )
    product_id = create_response.json()["id"]
    
    # 获取商品详情
    response = client.get(
        f"/api/v1/products/{product_id}",
        headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "测试商品2"


def test_update_product(get_token):
    """测试更新商品"""
    # 先创建一个分类
    create_category_response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "商品分类3", "parent_id": None, "level": 1, "sort": 2}
    )
    category_id = create_category_response.json()["id"]
    
    # 创建商品
    create_response = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "name": "测试商品3",
            "description": "测试商品描述3",
            "category_id": category_id,
            "brand": "测试品牌",
            "model": "测试型号",
            "is_active": True
        }
    )
    product_id = create_response.json()["id"]
    
    # 更新商品
    response = client.put(
        f"/api/v1/products/{product_id}",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "更新后的商品", "description": "更新后的描述"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "更新后的商品"
    assert data["description"] == "更新后的描述"


def test_delete_product(get_token):
    """测试删除商品"""
    # 先创建一个分类
    create_category_response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "商品分类4", "parent_id": None, "level": 1, "sort": 3}
    )
    category_id = create_category_response.json()["id"]
    
    # 创建商品
    create_response = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "name": "测试商品4",
            "description": "测试商品描述4",
            "category_id": category_id,
            "brand": "测试品牌",
            "model": "测试型号",
            "is_active": True
        }
    )
    product_id = create_response.json()["id"]
    
    # 删除商品
    response = client.delete(
        f"/api/v1/products/{product_id}",
        headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "商品删除成功"


# SKU测试
def test_create_sku(get_token):
    """测试创建SKU"""
    # 先创建一个分类和商品
    create_category_response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "SKU分类", "parent_id": None, "level": 1, "sort": 0}
    )
    category_id = create_category_response.json()["id"]
    
    create_product_response = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "name": "SKU商品",
            "description": "SKU商品描述",
            "category_id": category_id,
            "brand": "测试品牌",
            "model": "测试型号",
            "is_active": True
        }
    )
    product_id = create_product_response.json()["id"]
    
    # 创建SKU
    response = client.post(
        f"/api/v1/products/{product_id}/skus",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "sku_code": "SKU001",
            "attributes": {"color": "red", "size": "M"},
            "stock": 100
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["sku_code"] == "SKU001"
    assert data["attributes"] == {"color": "red", "size": "M"}
    assert data["stock"] == 100


def test_get_skus(get_token):
    """测试获取商品的SKU列表"""
    # 先创建一个分类和商品
    create_category_response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "SKU分类2", "parent_id": None, "level": 1, "sort": 1}
    )
    category_id = create_category_response.json()["id"]
    
    create_product_response = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "name": "SKU商品2",
            "description": "SKU商品描述2",
            "category_id": category_id,
            "brand": "测试品牌",
            "model": "测试型号",
            "is_active": True
        }
    )
    product_id = create_product_response.json()["id"]
    
    # 创建SKU
    client.post(
        f"/api/v1/products/{product_id}/skus",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "sku_code": "SKU002",
            "attributes": {"color": "blue", "size": "L"},
            "stock": 200
        }
    )
    
    # 获取SKU列表
    response = client.get(
        f"/api/v1/products/{product_id}/skus",
        headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_sku(get_token):
    """测试获取SKU详情"""
    # 先创建一个分类和商品
    create_category_response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "SKU分类3", "parent_id": None, "level": 1, "sort": 2}
    )
    category_id = create_category_response.json()["id"]
    
    create_product_response = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "name": "SKU商品3",
            "description": "SKU商品描述3",
            "category_id": category_id,
            "brand": "测试品牌",
            "model": "测试型号",
            "is_active": True
        }
    )
    product_id = create_product_response.json()["id"]
    
    # 创建SKU
    create_sku_response = client.post(
        f"/api/v1/products/{product_id}/skus",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "sku_code": "SKU003",
            "attributes": {"color": "green", "size": "S"},
            "stock": 300
        }
    )
    sku_id = create_sku_response.json()["id"]
    
    # 获取SKU详情
    response = client.get(
        f"/api/v1/products/skus/{sku_id}",
        headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sku_id
    assert data["sku_code"] == "SKU003"


def test_update_sku(get_token):
    """测试更新SKU"""
    # 先创建一个分类和商品
    create_category_response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "SKU分类4", "parent_id": None, "level": 1, "sort": 3}
    )
    category_id = create_category_response.json()["id"]
    
    create_product_response = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "name": "SKU商品4",
            "description": "SKU商品描述4",
            "category_id": category_id,
            "brand": "测试品牌",
            "model": "测试型号",
            "is_active": True
        }
    )
    product_id = create_product_response.json()["id"]
    
    # 创建SKU
    create_sku_response = client.post(
        f"/api/v1/products/{product_id}/skus",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "sku_code": "SKU004",
            "attributes": {"color": "yellow", "size": "XL"},
            "stock": 400
        }
    )
    sku_id = create_sku_response.json()["id"]
    
    # 更新SKU
    response = client.put(
        f"/api/v1/products/skus/{sku_id}",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"stock": 500, "attributes": {"color": "yellow", "size": "XXL"}}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sku_id
    assert data["stock"] == 500
    assert data["attributes"] == {"color": "yellow", "size": "XXL"}


def test_delete_sku(get_token):
    """测试删除SKU"""
    # 先创建一个分类和商品
    create_category_response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "SKU分类5", "parent_id": None, "level": 1, "sort": 4}
    )
    category_id = create_category_response.json()["id"]
    
    create_product_response = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "name": "SKU商品5",
            "description": "SKU商品描述5",
            "category_id": category_id,
            "brand": "测试品牌",
            "model": "测试型号",
            "is_active": True
        }
    )
    product_id = create_product_response.json()["id"]
    
    # 创建SKU
    create_sku_response = client.post(
        f"/api/v1/products/{product_id}/skus",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "sku_code": "SKU005",
            "attributes": {"color": "black", "size": "M"},
            "stock": 500
        }
    )
    sku_id = create_sku_response.json()["id"]
    
    # 删除SKU
    response = client.delete(
        f"/api/v1/products/skus/{sku_id}",
        headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "SKU删除成功"


# 价格测试
def test_create_price(get_token):
    """测试创建价格"""
    # 先创建一个分类、商品和SKU
    create_category_response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "价格分类", "parent_id": None, "level": 1, "sort": 0}
    )
    category_id = create_category_response.json()["id"]
    
    create_product_response = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "name": "价格商品",
            "description": "价格商品描述",
            "category_id": category_id,
            "brand": "测试品牌",
            "model": "测试型号",
            "is_active": True
        }
    )
    product_id = create_product_response.json()["id"]
    
    create_sku_response = client.post(
        f"/api/v1/products/{product_id}/skus",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "sku_code": "PRICE_SKU001",
            "attributes": {"color": "red", "size": "M"},
            "stock": 100
        }
    )
    sku_id = create_sku_response.json()["id"]
    
    # 创建价格
    response = client.post(
        f"/api/v1/products/skus/{sku_id}/prices",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "price_type": "retail",
            "price": 99.99,
            "min_quantity": 1,
            "max_quantity": 9
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["price_type"] == "retail"
    assert data["price"] == 99.99
    assert data["min_quantity"] == 1
    assert data["max_quantity"] == 9


def test_get_prices(get_token):
    """测试获取SKU的价格列表"""
    # 先创建一个分类、商品和SKU
    create_category_response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "价格分类2", "parent_id": None, "level": 1, "sort": 1}
    )
    category_id = create_category_response.json()["id"]
    
    create_product_response = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "name": "价格商品2",
            "description": "价格商品描述2",
            "category_id": category_id,
            "brand": "测试品牌",
            "model": "测试型号",
            "is_active": True
        }
    )
    product_id = create_product_response.json()["id"]
    
    create_sku_response = client.post(
        f"/api/v1/products/{product_id}/skus",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "sku_code": "PRICE_SKU002",
            "attributes": {"color": "blue", "size": "L"},
            "stock": 200
        }
    )
    sku_id = create_sku_response.json()["id"]
    
    # 创建价格
    client.post(
        f"/api/v1/products/skus/{sku_id}/prices",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "price_type": "wholesale",
            "price": 89.99,
            "min_quantity": 10,
            "max_quantity": None
        }
    )
    
    # 获取价格列表
    response = client.get(
        f"/api/v1/products/skus/{sku_id}/prices",
        headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_update_price(get_token):
    """测试更新价格"""
    # 先创建一个分类、商品和SKU
    create_category_response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "价格分类3", "parent_id": None, "level": 1, "sort": 2}
    )
    category_id = create_category_response.json()["id"]
    
    create_product_response = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "name": "价格商品3",
            "description": "价格商品描述3",
            "category_id": category_id,
            "brand": "测试品牌",
            "model": "测试型号",
            "is_active": True
        }
    )
    product_id = create_product_response.json()["id"]
    
    create_sku_response = client.post(
        f"/api/v1/products/{product_id}/skus",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "sku_code": "PRICE_SKU003",
            "attributes": {"color": "green", "size": "S"},
            "stock": 300
        }
    )
    sku_id = create_sku_response.json()["id"]
    
    # 创建价格
    create_price_response = client.post(
        f"/api/v1/products/skus/{sku_id}/prices",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "price_type": "retail",
            "price": 79.99,
            "min_quantity": 1,
            "max_quantity": 9
        }
    )
    price_id = create_price_response.json()["id"]
    
    # 更新价格
    response = client.put(
        f"/api/v1/products/prices/{price_id}",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"price": 69.99, "min_quantity": 1}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == price_id
    assert data["price"] == 69.99
    assert data["min_quantity"] == 1


def test_delete_price(get_token):
    """测试删除价格"""
    # 先创建一个分类、商品和SKU
    create_category_response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "价格分类4", "parent_id": None, "level": 1, "sort": 3}
    )
    category_id = create_category_response.json()["id"]
    
    create_product_response = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "name": "价格商品4",
            "description": "价格商品描述4",
            "category_id": category_id,
            "brand": "测试品牌",
            "model": "测试型号",
            "is_active": True
        }
    )
    product_id = create_product_response.json()["id"]
    
    create_sku_response = client.post(
        f"/api/v1/products/{product_id}/skus",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "sku_code": "PRICE_SKU004",
            "attributes": {"color": "yellow", "size": "XL"},
            "stock": 400
        }
    )
    sku_id = create_sku_response.json()["id"]
    
    # 创建价格
    create_price_response = client.post(
        f"/api/v1/products/skus/{sku_id}/prices",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "price_type": "wholesale",
            "price": 59.99,
            "min_quantity": 10,
            "max_quantity": None
        }
    )
    price_id = create_price_response.json()["id"]
    
    # 删除价格
    response = client.delete(
        f"/api/v1/products/prices/{price_id}",
        headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "价格删除成功"


# 属性测试
def test_create_attribute(get_token):
    """测试创建商品属性"""
    # 先创建一个分类和商品
    create_category_response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "属性分类", "parent_id": None, "level": 1, "sort": 0}
    )
    category_id = create_category_response.json()["id"]
    
    create_product_response = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "name": "属性商品",
            "description": "属性商品描述",
            "category_id": category_id,
            "brand": "测试品牌",
            "model": "测试型号",
            "is_active": True
        }
    )
    product_id = create_product_response.json()["id"]
    
    # 创建属性
    response = client.post(
        f"/api/v1/products/{product_id}/attributes",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "材质", "value": "纯棉"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "材质"
    assert data["value"] == "纯棉"


def test_get_attributes(get_token):
    """测试获取商品的属性列表"""
    # 先创建一个分类和商品
    create_category_response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "属性分类2", "parent_id": None, "level": 1, "sort": 1}
    )
    category_id = create_category_response.json()["id"]
    
    create_product_response = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "name": "属性商品2",
            "description": "属性商品描述2",
            "category_id": category_id,
            "brand": "测试品牌",
            "model": "测试型号",
            "is_active": True
        }
    )
    product_id = create_product_response.json()["id"]
    
    # 创建属性
    client.post(
        f"/api/v1/products/{product_id}/attributes",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "颜色", "value": "红色"}
    )
    
    # 获取属性列表
    response = client.get(
        f"/api/v1/products/{product_id}/attributes",
        headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_delete_attribute(get_token):
    """测试删除商品属性"""
    # 先创建一个分类和商品
    create_category_response = client.post(
        "/api/v1/products/categories",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "属性分类3", "parent_id": None, "level": 1, "sort": 2}
    )
    category_id = create_category_response.json()["id"]
    
    create_product_response = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {get_token}"},
        json={
            "name": "属性商品3",
            "description": "属性商品描述3",
            "category_id": category_id,
            "brand": "测试品牌",
            "model": "测试型号",
            "is_active": True
        }
    )
    product_id = create_product_response.json()["id"]
    
    # 创建属性
    create_attribute_response = client.post(
        f"/api/v1/products/{product_id}/attributes",
        headers={"Authorization": f"Bearer {get_token}"},
        json={"name": "尺寸", "value": "M"}
    )
    attribute_id = create_attribute_response.json()["id"]
    
    # 删除属性
    response = client.delete(
        f"/api/v1/products/attributes/{attribute_id}",
        headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "属性删除成功"
