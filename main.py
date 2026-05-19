"""
DIVINE WALLET v25.0 - ENTERPRISE PRODUCTION WITH AI BRAIN
Complete fintech backend with self-evolving AI, real payment rails, double-entry ledger.
"""

import os
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

from core.config import settings
from core.environment import Environment, CURRENT_ENV, InfrastructureConfig
from core.telemetry import initialize_observability
from core.ai_brain import AIBrain
from core.database.ledger import LedgerRepository
from core.database.cluster import DatabaseClusterManager
from core.crypto.hsm_client import HardwareSecurityModulePool
from core.network.iso8583_switch import VisaMessageSwitch
from services.stripe_issuing import StripeIssuingService
from services.circle_integration import CircleIntegration
from services.multiplier_service import MultiplierService
from services.webhook_processor import WebhookProcessor
from api.router import v1_financial_router

# Configure logging
log_level = logging.DEBUG if CURRENT_ENV == Environment.DEVELOPMENT else logging.INFO
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("divine.orchestrator")

# Load infrastructure configuration
infra_config = InfrastructureConfig(CURRENT_ENV)

# Security
security = HTTPBearer()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "G0doubledee")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "DIVINITY")
JWT_SECRET = os.getenv("JWT_SECRET", "divine_s3cr3t_k3y_2026")


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token."""
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"])
        if payload.get("sub") != ADMIN_USERNAME:
            raise HTTPException(401)
        return payload
    except:
        raise HTTPException(401, "Invalid token")


def create_token(username: str) -> str:
    """Create JWT token."""
    import time
    return jwt.encode({"sub": username, "exp": time.time() + 86400}, JWT_SECRET, algorithm="HS256")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Enterprise lifespan with AI Brain initialization."""
    logger.info("=" * 70)
    logger.info(f"DIVINE WALLET v25.0 - {CURRENT_ENV.value.upper()} MODE")
    logger.info("=" * 70)
    
    # 1. Initialize AI Brain (self-evolving)
    AIBrain.initialize(scan_interval=60)
    logger.info("🧠 AI Brain initialized - continuously evolving")
    
    # 2. Initialize observability
    initialize_observability(environment=CURRENT_ENV.value)
    
    # 3. Connect to database cluster
    await DatabaseClusterManager.initialize_pool(dsn=settings.DATABASE_URL)
    
    # 4. Connect to Hardware Security Modules
    if CURRENT_ENV != Environment.DEVELOPMENT:
        await HardwareSecurityModulePool.connect_hsm_clusters(
            host=settings.HSM_HOST,
            port=settings.HSM_PORT
        )
    
    # 5. Initialize real payment rails
    StripeIssuingService.initialize(api_key=infra_config.stripe_api_key, is_live=(CURRENT_ENV != Environment.DEVELOPMENT))
    CircleIntegration.initialize(api_key=infra_config.circle_api_key, is_live=(CURRENT_ENV != Environment.DEVELOPMENT))
    
    # 6. Start ISO 8583 message switch
    await VisaMessageSwitch.start_inbound_listeners()
    
    # 7. Initialize Multiplier Service
    MultiplierService.initialize()
    
    logger.info(f"Divine Wallet online - Admin: {ADMIN_USERNAME}")
    logger.info(f"AI Brain: {AIBrain.get_status()['status']}")
    yield
    
    # Graceful shutdown
    logger.info("Shutting down...")
    await VisaMessageSwitch.drain_and_stop()
    await HardwareSecurityModulePool.disconnect_all()
    await DatabaseClusterManager.close_pool()
    logger.info("Shutdown complete.")


# Create FastAPI app
app = FastAPI(
    title="Divine Wallet",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/v1/docs" if CURRENT_ENV != Environment.PRODUCTION else None
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(v1_financial_router, prefix="/v1")


# ==================== AUTH ENDPOINTS ====================
@app.post("/v1/auth/login")
async def login(data: dict):
    """Admin-only login."""
    if data.get("username") == ADMIN_USERNAME and data.get("password") == ADMIN_PASSWORD:
        return {"success": True, "access_token": create_token(ADMIN_USERNAME)}
    raise HTTPException(401, "Invalid credentials")


@app.get("/v1/auth/verify")
async def verify(payload: dict = Depends(verify_token)):
    return {"success": True, "user": payload.get("sub")}


# ==================== HEALTH & AI ====================
@app.get("/health")
async def health():
    ledger = LedgerRepository()
    balance = await ledger.get_master_balance()
    ai_status = AIBrain.get_status()
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": CURRENT_ENV.value,
        "master_balance": balance,
        "ai_brain": ai_status,
        "admin_configured": True
    }


@app.get("/v1/ai/status")
async def ai_status():
    return AIBrain.get_status()


@app.get("/v1/ai/insights")
async def ai_insights():
    return AIBrain.get_insights()


@app.post("/v1/ai/upgrade")
async def ai_force_upgrade(payload: dict = Depends(verify_token)):
    """Force AI upgrade cycle (admin only)."""
    return AIBrain.force_upgrade()


# ==================== SIMPLE HTML FRONTEND ====================
HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Divine Wallet v25.0</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0a0a0a;color:#fff}.container{max-width:500px;margin:0 auto;padding:16px}.balance-card{background:linear-gradient(135deg,#1a1a1a,#0f0f0f);border-radius:24px;padding:20px;text-align:center;border:1px solid #f59e0b20;margin-bottom:20px}.balance-amount{color:#f59e0b;font-size:28px;font-weight:bold}.coastal-card{background:linear-gradient(135deg,#1a3a2a,#0f2a1a);border-radius:16px;padding:16px;margin-bottom:20px;border:1px solid #10b981}.coastal-balance{color:#10b981;font-size:28px;font-weight:bold}.grid-2{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-bottom:20px}.action-btn{background:#1a1a1a;border:1px solid #333;border-radius:16px;padding:16px;text-align:center;cursor:pointer}.multiply-btn{background:linear-gradient(135deg,#dc2626,#991b1b);border:none;border-radius:16px;padding:16px;width:100%;font-weight:bold;color:#fff;cursor:pointer;margin-bottom:20px}.modal{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.95);justify-content:center;align-items:center;z-index:1000;padding:20px}.modal-content{background:#1a1a1a;border-radius:24px;padding:24px;max-width:400px;width:100%;border:1px solid #f59e0b}.modal-input{width:100%;background:#0a0a0a;border:1px solid #333;border-radius:12px;padding:14px;color:#fff;margin-bottom:12px}.modal-btn{width:100%;background:#f59e0b;border:none;border-radius:12px;padding:14px;color:#000;font-weight:bold;cursor:pointer}.hidden{display:none}.tabs{display:flex;gap:4px;background:#1a1a1a;padding:4px;border-radius:16px;margin-bottom:20px}.tab{flex:1;padding:10px;text-align:center;background:transparent;border:none;color:#888;font-size:12px;cursor:pointer;border-radius:12px}.tab.active{background:#f59e0b;color:#000}.tab-content{display:none}.tab-content.active{display:block}</style>
</head>
<body>
<div id="loginScreen" style="min-height:100vh;display:flex;justify-content:center;align-items:center;background:linear-gradient(135deg,#0a0a0a,#1a1a1a)">
<div style="background:#1a1a1a;border-radius:32px;padding:32px;width:90%;max-width:350px;border:1px solid #f59e0b;text-align:center">
<div style="font-size:32px;font-weight:bold;background:linear-gradient(135deg,#f59e0b,#ea580c);-webkit-background-clip:text;-webkit-text-fill-color:transparent">✦ Divine Wallet</div>
<div style="margin:20px 0;color:#f59e0b">v25.0 - AI Brain</div>
<input type="text" id="loginUser" class="modal-input" placeholder="Username" value="G0doubledee">
<input type="password" id="loginPass" class="modal-input" placeholder="Password" value="DIVINITY">
<button class="modal-btn" onclick="login()">Access Divine Wallet</button>
<div style="margin-top:12px;color:#666;font-size:12px">G0doubledee / DIVINITY</div>
</div>
</div>
<div id="mainApp" class="container hidden">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px"><div style="font-size:24px;font-weight:bold;background:linear-gradient