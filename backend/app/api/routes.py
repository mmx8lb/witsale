from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

# Create router
router = APIRouter()

# Root endpoint
@router.get("/")
async def root():
    return {"message": "Welcome to Witsale API"}

# Health check endpoint
@router.get("/health")
async def health_check():
    return {"status": "healthy"}

# Version endpoint
@router.get("/version")
async def get_version():
    return {"version": "1.0.0"}

# Test database connection endpoint
@router.get("/test-db")
async def test_database(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {"status": "database connection successful"}
    except Exception as e:
        return {"status": "database connection failed", "error": str(e)}
