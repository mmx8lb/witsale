import httpx
import asyncio
from app.core.security import create_access_token
from app.core.database import AsyncSessionLocal
from app.schemas import UserCreate
from app.services.auth_service import auth_service

async def create_test_user():
    """创建测试用户"""
    async with AsyncSessionLocal() as db:
        # 检查是否已有测试用户
        user = await auth_service.get_user_by_username(db, "testuser")
        if not user:
            # 创建测试用户
            user_in = UserCreate(
                username="testuser",
                email="test@example.com",
                password="testpassword",
                phone="13800138000",
                role_id=1  # 假设1是管理员角色
            )
            user = await auth_service.create_user(db, user_in)
        return user

async def test_customer_api():
    # 创建测试用户
    test_user = await create_test_user()
    # 使用用户ID创建JWT令牌
    token = create_access_token(data={'sub': str(test_user.id)})
    
    async with httpx.AsyncClient(base_url='http://localhost:8001') as client:
        try:
            # 测试创建客户分类
            response = await client.post(
                '/api/v1/customer/categories',
                headers={'Authorization': f'Bearer {token}'},
                json={'name': '测试分类', 'code': 'TEST_CATEGORY', 'description': '测试分类描述'}
            )
            print('创建分类:', response.status_code, response.json())
            
            # 测试创建客户等级
            response = await client.post(
                '/api/v1/customer/levels',
                headers={'Authorization': f'Bearer {token}'},
                json={'name': '测试等级', 'code': 'TEST_LEVEL', 'min_spend': 1000, 'max_spend': 5000, 'discount_rate': 0.95}
            )
            print('创建等级:', response.status_code, response.json())
            
            # 测试创建客户
            response = await client.post(
                '/api/v1/customer',
                headers={'Authorization': f'Bearer {token}'},
                json={'name': '测试客户', 'code': 'TEST_CUSTOMER', 'category_id': 1, 'contact_name': '张三', 'contact_phone': '13800138000', 'address': '北京市朝阳区'}
            )
            print('创建客户:', response.status_code, response.json())
            
            # 测试获取客户列表
            response = await client.get(
                '/api/v1/customer',
                headers={'Authorization': f'Bearer {token}'}
            )
            print('获取客户列表:', response.status_code, len(response.json()))
            
        except Exception as e:
            print('错误:', e)

if __name__ == '__main__':
    asyncio.run(test_customer_api())
