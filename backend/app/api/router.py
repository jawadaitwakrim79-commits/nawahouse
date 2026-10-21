from fastapi import APIRouter
from app.api.routes import orders, events, contact, health, clicks

router = APIRouter()

router.include_router(health.router, tags=["health"])
router.include_router(orders.router, prefix="/api", tags=["orders"])
router.include_router(events.router, prefix="/api", tags=["events"])
router.include_router(contact.router, prefix="/api", tags=["contact"])
router.include_router(clicks.router, prefix="/api", tags=["clicks"])
