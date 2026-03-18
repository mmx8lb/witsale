import httpx
import asyncio
from app.core.security import create_access_token
from app.core.database import AsyncSessionLocal
from app.schemas import UserCreate
from app.services.auth_service import auth_service
from datetime import datetime

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

async def test_finance_api():
    # 创建测试用户
    test_user = await create_test_user()
    # 使用用户ID创建JWT令牌
    token = create_access_token(data={'sub': str(test_user.id)})
    
    async with httpx.AsyncClient(base_url='http://localhost:8001') as client:
        try:
            # 测试获取账户列表，使用已存在的账户
            print("=== 测试获取账户列表 ===")
            response = await client.get(
                '/api/v1/finance/accounts',
                headers={'Authorization': f'Bearer {token}'}
            )
            print('获取账户列表:', response.status_code, len(response.json()))
            
            if len(response.json()) > 0:
                # 使用已存在的账户
                account_id = response.json()[0]['id']
                print(f"使用已存在的账户ID: {account_id}")
            else:
                # 创建新账户
                print("=== 测试创建账户 ===")
                import uuid
                unique_code = f'TEST_ACCOUNT_{uuid.uuid4().hex[:8]}'
                response = await client.post(
                    '/api/v1/finance/accounts',
                    headers={'Authorization': f'Bearer {token}'},
                    json={'name': '测试企业账户', 'code': unique_code, 'type': 'enterprise', 'balance': 10000.00}
                )
                print('创建账户:', response.status_code, response.json())
                account_id = response.json()['id']
            
            # 测试创建收入交易
            print("\n=== 测试创建收入交易 ===")
            response = await client.post(
                '/api/v1/finance/transactions',
                headers={'Authorization': f'Bearer {token}'},
                json={'account_id': account_id, 'type': 'income', 'amount': 5000.00, 'payment_method': 'online', 'reference_type': 'order', 'reference_id': 1, 'notes': '订单收入'}
            )
            print('创建收入交易:', response.status_code, response.json())
            transaction_id = response.json()['id']
            
            # 测试创建支出交易
            print("\n=== 测试创建支出交易 ===")
            response = await client.post(
                '/api/v1/finance/transactions',
                headers={'Authorization': f'Bearer {token}'},
                json={'account_id': account_id, 'type': 'expense', 'amount': 2000.00, 'payment_method': 'online', 'reference_type': 'purchase', 'reference_id': 1, 'notes': '采购支出'}
            )
            print('创建支出交易:', response.status_code, response.json())
            
            # 测试创建发票
            print("\n=== 测试创建发票 ===")
            response = await client.post(
                '/api/v1/finance/invoices',
                headers={'Authorization': f'Bearer {token}'},
                json={'account_id': account_id, 'transaction_id': transaction_id, 'amount': 5000.00, 'total_amount': 5500.00, 'tax_amount': 500.00, 'status': 'issued'}
            )
            print('创建发票:', response.status_code, response.json())
            
            # 测试生成利润表
            print("\n=== 测试生成利润表 ===")
            today = datetime.utcnow()
            last_month = today.replace(month=today.month-1) if today.month > 1 else today.replace(year=today.year-1, month=12)
            
            response = await client.post(
                f'/api/v1/finance/reports/income-statement?period_start={last_month.isoformat()}&period_end={today.isoformat()}',
                headers={'Authorization': f'Bearer {token}'}
            )
            print('生成利润表:', response.status_code, response.json())
            
            # 测试获取账户列表
            print("\n=== 测试获取账户列表 ===")
            response = await client.get(
                '/api/v1/finance/accounts',
                headers={'Authorization': f'Bearer {token}'}
            )
            print('获取账户列表:', response.status_code, len(response.json()))
            
            # 测试获取交易列表
            print("\n=== 测试获取交易列表 ===")
            response = await client.get(
                f'/api/v1/finance/transactions?account_id={account_id}',
                headers={'Authorization': f'Bearer {token}'}
            )
            print('获取交易列表:', response.status_code, len(response.json()))
            
        except Exception as e:
            print('错误:', e)

if __name__ == '__main__':
    asyncio.run(test_finance_api())
