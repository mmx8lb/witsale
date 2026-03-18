from app.core.security import get_password_hash, verify_password

# 测试密码哈希功能
try:
    password = "pass123"
    print(f"测试密码: {password}")
    print(f"密码长度: {len(password)}")
    
    hashed = get_password_hash(password)
    print(f"哈希结果: {hashed}")
    
    verified = verify_password(password, hashed)
    print(f"验证结果: {verified}")
    
    print("测试成功!")
except Exception as e:
    print(f"测试失败: {e}")
