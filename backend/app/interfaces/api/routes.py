from fastapi import APIRouter
from app.interfaces.api.v1 import auth
from app.interfaces.api.v1.endpoints import product, order, inventory, customer, finance

api_router = APIRouter()

# 认证相关路由
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# 商品管理相关路由
api_router.include_router(product.router, prefix="/v1", tags=["products"])

# 订单管理相关路由
api_router.include_router(order.router, prefix="/v1", tags=["orders"])

# 库存管理相关路由
api_router.include_router(inventory.router, prefix="/v1", tags=["inventory"])

# 客户管理相关路由
api_router.include_router(customer.router, prefix="/v1", tags=["customer"])

# 财务管理相关路由
api_router.include_router(finance.router, prefix="/v1", tags=["finance"])
