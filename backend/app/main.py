from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.interfaces.api.routes import api_router
from app.core.database import AsyncSessionLocal
from app.core.init_data import init_default_roles_and_permissions

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Enterprise sales management system API"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    # 初始化默认角色和权限
    async with AsyncSessionLocal() as db:
        try:
            await init_default_roles_and_permissions(db)
        except Exception as e:
            print(f"初始化默认数据失败: {e}")
    
    # 暂时注释掉Redis初始化
    # await redis_client.init_redis()
    pass


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    # 暂时注释掉Redis关闭
    # await redis_client.close()
    pass


# 包含API路由
app.include_router(api_router, prefix="/api")


# Root path
@app.get("/")
async def root():
    return {"message": "Welcome to Witsale API"}

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Version endpoint
@app.get("/version")
async def get_version():
    return {"version": settings.VERSION}
