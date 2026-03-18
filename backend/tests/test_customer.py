import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.customer import CustomerCategory, CustomerLevel, Customer
from app.core.database import get_db
from app.main import app
from app.core.security import create_access_token


@pytest.fixture
async def db_session():
    from app.core.database import async_session_maker
    async with async_session_maker() as session:
        yield session


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def test_token():
    return create_access_token(data={"sub": "testuser"})


async def test_create_customer_category(db_session: AsyncSession, client: AsyncClient, test_token: str):
    # 测试创建客户分类
    response = await client.post(
        "/api/v1/customers/categories",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "name": "测试分类",
            "description": "测试分类描述"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "测试分类"
    assert data["description"] == "测试分类描述"


async def test_create_customer_level(db_session: AsyncSession, client: AsyncClient, test_token: str):
    # 测试创建客户等级
    response = await client.post(
        "/api/v1/customers/levels",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "name": "测试等级",
            "min_purchase": 1000,
            "max_purchase": 5000,
            "discount_rate": 0.95
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "测试等级"
    assert data["min_purchase"] == 1000
    assert data["max_purchase"] == 5000
    assert data["discount_rate"] == 0.95


async def test_create_customer(db_session: AsyncSession, client: AsyncClient, test_token: str):
    # 先创建分类和等级
    await test_create_customer_category(db_session, client, test_token)
    await test_create_customer_level(db_session, client, test_token)
    
    # 测试创建客户
    response = await client.post(
        "/api/v1/customers",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "name": "测试客户",
            "category_id": 1,
            "contact_name": "张三",
            "contact_phone": "13800138000",
            "address": "北京市朝阳区"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "测试客户"
    assert data["category_id"] == 1
    assert data["contact_name"] == "张三"
    assert data["contact_phone"] == "13800138000"
    assert data["address"] == "北京市朝阳区"


async def test_get_customers(db_session: AsyncSession, client: AsyncClient, test_token: str):
    # 先创建客户
    await test_create_customer(db_session, client, test_token)
    
    # 测试获取客户列表
    response = await client.get(
        "/api/v1/customers",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


async def test_update_customer(db_session: AsyncSession, client: AsyncClient, test_token: str):
    # 先创建客户
    await test_create_customer(db_session, client, test_token)
    
    # 测试更新客户
    response = await client.put(
        "/api/v1/customers/1",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "name": "更新后的测试客户",
            "contact_name": "李四",
            "contact_phone": "13900139000"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "更新后的测试客户"
    assert data["contact_name"] == "李四"
    assert data["contact_phone"] == "13900139000"


async def test_delete_customer(db_session: AsyncSession, client: AsyncClient, test_token: str):
    # 先创建客户
    await test_create_customer(db_session, client, test_token)
    
    # 测试删除客户
    response = await client.delete(
        "/api/v1/customers/1",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Customer deleted successfully"
