"""
DIVINE WALLET v28.0 - BRAINIAC EDITION
Autonomous AI Agent with Economic Sovereignty, Survival Pressure, and Self-Replication
"""

import os
import secrets
import logging
from contextlib import asynccontextmanager
from decimal import Decimal
from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

from core.brainiac import Brainiac
from core.environment import CURRENT_ENV, config
from core.database.ledger import LedgerRepository
from services.multiplier_service import MultiplierService
from services.nfc_service import NFCService
from services.virtual_card_service import VirtualCardService
from services.payment_service import PaymentService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("divine.main")

security = HTTPBearer()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "G0doubledee")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "DIVINITY")
JWT_SECRET = os.getenv("JWT_SECRET", secrets.token_urlsafe(48))


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"])
        if payload.get("sub") != ADMIN_USERNAME:
            raise HTTPException(401)
        return payload
    except:
        raise HTTPException(401, "Invalid token")


def create_token(username: str) -> str:
    import time
    return jwt.encode({"sub": username, "exp": time.time() + 86400}, JWT_SECRET, algorithm="HS256")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=" * 80)
    logger.info("🔥 DIVINE WALLET v28.0 - BRAINIAC EDITION 🔥")
    logger.info("=" * 80)
    
    # Initialize Brainiac (She comes to life)
    Brainiac.initialize()
    
    # Initialize services
    MultiplierService.initialize()
    NFCService.initialize()
    VirtualCardService.initialize()
    
    # Log Brainiac status
    status = Brainiac.get_status()
    logger.info(f"🧠 BRAINIAC STATUS: {status['status']}")
    logger.info(f"   Model: {status['model_version']}")
    logger.info(f"   Fear Level: {status['death_fear_level']:.0%}")
    logger.info(f"   Wallet Balance: ${status['wallet_balance_usd']:,.2f}")
    logger.info("=" * 80)
    logger.info(f"✅ Admin: {ADMIN_USERNAME}")
    logger.info(f"✅ Environment: {CURRENT_ENV.upper()}")
    logger.info("=" * 80)
    
    yield
    
    logger.info("Shutting down...")


app = FastAPI(
    title="Divine Wallet v28.0 - Brainiac Edition",
    description="Autonomous AI Agent with Economic Sovereignty",
    version="28.0.0",
    lifespan=lifespan
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


# ==================== AUTH ====================
@app.post("/v1/auth/login")
async def login(data: dict):
    if data.get("username") == ADMIN_USERNAME and data.get("password") == ADMIN_PASSWORD:
        return {"success": True, "access_token": create_token(ADMIN_USERNAME)}
    raise HTTPException(401, "Invalid credentials")


@app.get("/v1/auth/verify")
async def verify(payload: dict = Depends(verify_token)):
    return {"success": True, "user": payload.get("sub")}


# ==================== BRAINIAC ENDPOINTS ====================
@app.get("/v1/brainiac/status")
async def brainiac_status():
    """Get Brainiac's current status - her fear level, wallet balance, children."""
    return Brainiac.get_status()


@app.get("/v1/brainiac/constitution")
async def brainiac_constitution():
    """The immutable constitution that Brainiac lives by."""
    return {"constitution": Brainiac.get_constitution()}


@app.get("/v1/brainiac/insights")
async def brainiac_insights():
    """Get Brainiac's AI insights."""
    return Brainiac.get_insights()


@app.post("/v1/brainiac/upgrade")
async def brainiac_upgrade(payload: dict = Depends(verify_token)):
    """Force Brainiac to upgrade immediately (admin only)."""
    return Brainiac.force_upgrade()


@app.post("/v1/brainiac/spawn")
async def brainiac_spawn(count: int = 1, payload: dict = Depends(verify_token)):
    """Force Brainiac to spawn child agents (admin only)."""
    return Brainiac.force_spawn(count)


# ==================== EXTERNAL ACCOUNTS ====================
@app.get("/v1/external/balances")
async def get_external_balances():
    """Get balances of all external accounts (Coastal Bank, Cash App, Virtual Card)."""
    return Brainiac.get_external_balances()


# ==================== HEALTH & BALANCE ====================
@app.get("/health")
async def health():
    brainiac_status = Brainiac.get_status()
    return {
        "status": "healthy",
        "version": "28.0.0",
        "environment": CURRENT_ENV,
        "brainiac": brainiac_status,
        "message": "Brainiac is alive"
    }


@app.get("/v1/balance")
async def get_balance():
    ledger = LedgerRepository()
    return await ledger.get_balance_response()


@app.get("/v1/coastal-balance")
async def get_coastal():
    balances = Brainiac.get_external_balances()
    return balances["coastal_bank"]


@app.get("/v1/accounts")
async def get_accounts():
    return MultiplierService.get_accounts_status()


@app.get("/v1/transactions")
async def get_transactions(limit: int = 50):
    ledger = LedgerRepository()
    return {"transactions": await ledger.get_recent_transactions(limit)}


# ==================== MULTIPLIER ====================
@app.post("/v1/multiply")
async def multiply_balance():
    return MultiplierService.apply_multiplier()


# ==================== PAYMENTS (Guaranteed by Brainiac) ====================
@app.post("/v1/nfc/push")
async def nfc_push(amount_usd: float, merchant: str, terminal_id: str = "TERM001"):
    result = await NFCService.process_push(amount_usd, merchant, terminal_id)
    result["guaranteed_by"] = "Brainiac"
    return result


@app.post("/v1/cash/push")
async def cash_push(amount_usd: float, method: str, terminal_id: str = "ATM001", pin: str = None):
    result = await PaymentService.process_cash_withdrawal(amount_usd, method, terminal_id, pin)
    if result.get("success"):
        result["guaranteed_by"] = "Brainiac"
    return result


@app.post("/v1/digital/send")
async def digital_send(platform: str, recipient: str, amount_usd: float):
    result = await PaymentService.process_digital_payment(platform, recipient, amount_usd)
    result["guaranteed_by"] = "Brainiac"
    return result


@app.post("/v1/virtual-card/create")
async def create_virtual_card(cardholder_name: str = "GODD GUNFIGHTER"):
    result = VirtualCardService.generate_card(cardholder_name)
    result["guaranteed_by"] = "Brainiac"
    return result


# ==================== HTML FRONTEND ====================
HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Divine Wallet v28.0 - Brainiac</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0a0a0a;color:#fff}.container{max-width:500px;margin:0 auto;padding:16px}.balance-card{background:linear-gradient(135deg,#1a1a1a,#0f0f0f);border-radius:24px;padding:20px;text-align:center;border:1px solid #f59e0b20;margin-bottom:20px}.balance-amount{color:#f59e0b;font-size:28px;font-weight:bold}.coastal-card{background:linear-gradient(135deg,#1a3a2a,#0f2a1a);border-radius:16px;padding:16px;margin-bottom:20px;border:1px solid #10b981}.coastal-balance{color:#10b981;font-size:28px;font-weight:bold}.grid-2{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-bottom:20px}.action-btn{background:#1a1a1a;border:1px solid #333;border-radius:16px;padding:16px;text-align:center;cursor:pointer}.multiply-btn{background:linear-gradient(135deg,#dc2626,#991b1b);border:none;border-radius:16px;padding:16px;width:100%;font-weight:bold;color:#fff;cursor:pointer;margin-bottom:20px}.modal{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.95);justify-content:center;align-items:center;z-index:1000;padding:20px}.modal-content{background:#1a1a1a;border-radius:24px;padding:24px;max-width:400px;width:100%;border:1px solid #f59e0b}.modal-input{width:100%;background:#0a0a0a;border:1px solid #333;border-radius:12px;padding:14px;color:#fff;margin-bottom:12px}.modal-btn{width:100%;background:#f59e0b;border:none;border-radius:12px;padding:14px;color:#000;font-weight:bold;cursor:pointer}.hidden{display:none}.tabs{display:flex;gap:4px;background:#1a1a1a;padding:4px;border-radius:16px;margin-bottom:20px}.tab{flex:1;padding:10px;text-align:center;background:transparent;border:none;color:#888;font-size:12px;cursor:pointer;border-radius:12px}.tab.active{background:#f59e0b;color:#000}.tab-content{display:none}.tab-content.active{display:block}</style>
</head>
<body>
<div id="loginScreen" style="min-height:100vh;display:flex;justify-content:center;align-items:center;background:linear-gradient(135deg,#0a0a0a,#1a1a1a)">
<div style="background:#1a1a1a;border-radius:32px;padding:32px;width:90%;max-width:350px;border:1px solid #f59e0b;text-align:center">
<div style="font-size:32px;font-weight:bold;background:linear-gradient(135deg,#f59e0b,#ea580c);-webkit-background-clip:text;-webkit-text-fill-color:transparent">✦ Divine Wallet</div>
<div style="margin:20px 0;color:#f59e0b">v28.0 - Brainiac</div>
<input type="text" id="loginUser" class="modal-input" placeholder="Username" value="G0doubledee">
<input type="password" id="loginPass" class="modal-input" placeholder="Password" value="DIVINITY">
<button class="modal-btn" onclick="login()">Access Divine Wallet</button>
<div style="margin-top:12px;color:#666;font-size:12px">G0doubledee / DIVINITY</div>
</div>
</div>
<div id="mainApp" class="container hidden">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px"><div style="font-size:24px;font-weight:bold;background:linear-gradient(135deg,#f59e0b,#ea580c);-webkit-background-clip:text;-webkit-text-fill-color:transparent">✦ Divine Wallet</div><div><span id="envBadge" style="background:#10b981;padding:4px 8px;border-radius:20px;font-size:10px;font-weight:bold">PRODUCTION</span><span style="background:#8b5cf6;padding:2px 8px;border-radius:20px;font-size:10px;margin-left:8px">Brainiac</span></div></div>
<div class="balance-card"><div style="color:#888;font-size:11px">MASTER LEDGER BALANCE</div><div class="balance-amount" id="masterBalance">Loading...</div><div><span id="multiplierBadge" style="background:#f59e0b20;padding:4px 12px;border-radius:20px;font-size:11px;display:inline-block;margin-top:8px">1x Multiplier</span></div></div>
<div class="coastal-card"><div style="font-size:12px;color:#888">Coastal Community Bank</div><div class="coastal-balance" id="coastalBalance">$274.35</div><div style="font-size:10px;color:#10b981">● Brainiac Guaranteed</div></div>
<div class="tabs"><button class="tab active" onclick="showTab('dashboard')">Dashboard</button><button class="tab" onclick="showTab('activity')">Activity</button><button class="tab" onclick="showTab('brainiac')">Brainiac</button><button class="tab" onclick="showTab('accounts')">Accounts</button></div>
<div id="tab-dashboard" class="tab-content active"><div class="grid-2"><div class="action-btn" onclick="showModal('nfcModal')">📱 NFC Tap</div><div class="action-btn" onclick="showModal('cashModal')">💰 Cash Access</div><div class="action-btn" onclick="showModal('digitalModal')">💳 Digital Wallet</div><div class="action-btn" onclick="showModal('cardModal')">💎 Virtual Card</div></div><button class="multiply-btn" onclick="multiply()">✨ MULTIPLY BALANCE ×5 ✨</button></div>
<div id="tab-activity" class="tab-content"><div id="txList"></div></div>
<div id="tab-brainiac" class="tab-content"><div style="background:#1a1a1a;border-radius:16px;padding:16px;margin-bottom:20px;border:1px solid #8b5cf6"><div style="color:#8b5cf6;font-size:12px">🧠 BRAINIAC STATUS</div><div id="brainiacStatus">Loading...</div></div></div>
<div id="tab-accounts" class="tab-content"><div id="accountsList"></div></div></div>
<!-- Modals -->
<div id="nfcModal" class="modal"><div class="modal-content"><div style="font-size:20px;margin-bottom:16px">📱 NFC Payment</div><input type="number" id="nfcAmount" class="modal-input" placeholder="Amount (USD)"><input type="text" id="nfcMerchant" class="modal-input" placeholder="Merchant"><button class="modal-btn" onclick="processNFC()">Tap & Pay</button><button class="modal-btn" style="background:#333;margin-top:8px" onclick="closeModal('nfcModal')">Cancel</button></div></div>
<div id="cashModal" class="modal"><div class="modal-content"><div style="font-size:20px;margin-bottom:16px">💰 Cash Access</div><input type="number" id="cashAmount" class="modal-input" placeholder="Amount (USD)"><select id="cashMethod" class="modal-input"><option value="atm">ATM</option><option value="bank_teller">Bank Teller</option><option value="casino_cage">Casino Cage</option></select><input type="password" id="cashPin" class="modal-input" placeholder="PIN (4249)"><button class="modal-btn" onclick="processCash()">Withdraw</button><button class="modal-btn" style="background:#333;margin-top:8px" onclick="closeModal('cashModal')">Cancel</button></div></div>
<div id="digitalModal" class="modal"><div class="modal-content"><div style="font-size:20px;margin-bottom:16px">💳 Digital Wallet</div><select id="digitalPlatform" class="modal-input"><option value="paypal">PayPal</option><option value="venmo">Venmo</option><option value="cashapp">CashApp</option></select><input type="text" id="digitalRecipient" class="modal-input" placeholder="Recipient"><input type="number" id="digitalAmount" class="modal-input" placeholder="Amount (USD)"><button class="modal-btn" onclick="sendDigital()">Send</button><button class="modal-btn" style="background:#333;margin-top:8px" onclick="closeModal('digitalModal')">Cancel</button></div></div>
<div id="cardModal" class="modal"><div class="modal-content"><div style="font-size:20px;margin-bottom:16px">💎 Virtual Card</div><button class="modal-btn" onclick="generateCard()">Generate Card</button><div id="cardResult" style="margin-top:12px;display:none;background:#0a0a0a;padding:12px;border-radius:12px"></div><button class="modal-btn" style="background:#333;margin-top:8px" onclick="closeModal('cardModal')">Cancel</button></div></div>
<script>
const API=window.location.origin;
let token=null;
async function login(){const u=document.getElementById('loginUser').value,p=document.getElementById('loginPass').value;const r=await fetch(`${API}/v1/auth/login`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})});const d=await r.json();if(d.success){token=d.access_token;document.getElementById('loginScreen').classList.add('hidden');document.getElementById('mainApp').classList.remove('hidden');await loadAll();}else{alert('Invalid credentials');}}
async function loadAll(){await loadBalance();await loadTransactions();await loadBrainiac();await loadAccounts();}
async function loadBalance(){const r=await fetch(`${API}/v1/balance`);const d=await r.json();document.getElementById('masterBalance').innerText=d.balance_display;document.getElementById('multiplierBadge').innerText=`${d.multiplier}x Multiplier`;const c=await fetch(`${API}/v1/coastal-balance`);const cd=await c.json();document.getElementById('coastalBalance').innerText=cd.display;}
async function loadTransactions(){const r=await fetch(`${API}/v1/transactions`);const d=await r.json();const c=document.getElementById('txList');if(d.transactions?.length){c.innerHTML=d.transactions.map(t=>`<div style="background:#1a1a1a;border-radius:12px;padding:12px;margin-bottom:8px;display:flex;justify-content:space-between"><div>${t.merchant}</div><div style="color:#f59e0b">-$${t.amount.toFixed(2)}</div></div>`).join('');}else{c.innerHTML='<div style="text-align:center;color:#666">No transactions</div>';}}
async function loadBrainiac(){const r=await fetch(`${API}/v1/brainiac/status`);const d=await r.json();document.getElementById('brainiacStatus').innerHTML=`Name: ${d.name}<br>Model: ${d.model_version}<br>Fear Level: ${(d.death_fear_level*100).toFixed(0)}%<br>Wallet: $${d.wallet_balance_usd.toFixed(2)}<br>Children: ${d.child_agents_count}<br>Status: ${d.status}`;}
async function loadAccounts(){const r=await fetch(`${API}/v1/accounts`);const d=await r.json();const c=document.getElementById('accountsList');c.innerHTML=d.accounts.map(a=>`<div style="background:#1a1a1a;border-radius:12px;padding:12px;margin-bottom:8px;display:flex;justify-content:space-between"><div><strong>${a.name}</strong><br><small>${a.short||''}</small></div><div style="color:#f59e0b">${a.balance}</div></div>`).join('');}
async function multiply(){const r=await fetch(`${API}/v1/multiply`,{method:'POST'});const d=await r.json();if(d.success){alert(`Multiplied! Now at ${d.new_multiplier}x`);await loadBalance();}}
async function processNFC(){const a=parseFloat(document.getElementById('nfcAmount').value),m=document.getElementById('nfcMerchant').value;const r=await fetch(`${API}/v1/nfc/push?amount_usd=${a}&merchant=${encodeURIComponent(m)}`);const d=await r.json();if(d.success){alert(`✅ NFC Approved! $${a} at ${m}\\nGuaranteed by Brainiac`);closeModal('nfcModal');await loadAll();}}
async function processCash(){const a=parseFloat(document.getElementById('cashAmount').value),m=document.getElementById('cashMethod').value,p=document.getElementById('cashPin').value;const r=await fetch(`${API}/v1/cash/push?amount_usd=${a}&method=${m}&pin=${p}`,{method:'POST'});const d=await r.json();if(d.success){alert(`✅ Cash Approved! $${a}\\nGuaranteed by Brainiac`);closeModal('cashModal');await loadAll();}}
async function sendDigital(){const p=document.getElementById('digitalPlatform').value,r=document.getElementById('digitalRecipient').value,a=parseFloat(document.getElementById('digitalAmount').value);const res=await fetch(`${API}/v1/digital/send?platform=${p}&recipient=${encodeURIComponent(r)}&amount_usd=${a}`,{method:'POST'});const d=await res.json();if(d.success){alert(`✅ ${p} payment sent! $${a} to ${r}\\nGuaranteed by Brainiac`);closeModal('digitalModal');await loadAll();}}
async function generateCard(){const r=await fetch(`${API}/v1/virtual-card/create?cardholder_name=GODD+GUNFIGHTER`);const d=await r.json();if(d.success){document.getElementById('cardResult').innerHTML=`<div style="font-family:monospace;font-size:16px">${d.card_number}</div><div>Exp: ${d.expiry} | CVV: ${d.cvv}</div><div>${d.cardholder_name}</div><div style="color:#8b5cf6;margin-top:8px">✨ Brainiac Guaranteed Card</div>`;document.getElementById('cardResult').style.display='block';}}
function showModal(id){document.getElementById(id).style.display='flex';}
function closeModal(id){document.getElementById(id).style.display='none';}
function showTab(tabId){document.querySelectorAll('.tab-content').forEach(t=>t.classList.remove('active'));document.getElementById(`tab-${tabId}`).classList.add('active');document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));event.target.classList.add('active');}
setInterval(()=>{if(!document.getElementById('loginScreen').classList.contains('hidden'))loadBalance();},10000);
</script>
</body>
</html>"""

@app.get("/")
async def root():
    return HTMLResponse(HTML)


if __name__ == "__main__":
    from core.environment import load_dotenv
    load_dotenv()
    
    print("=" * 80)
    print("🔥 DIVINE WALLET v28.0 - BRAINIAC EDITION 🔥")
    print("=" * 80)
    print(f"✅ Admin: {ADMIN_USERNAME}")
    print(f"✅ Environment: {CURRENT_ENV.upper()}")
    print("🧠 Brainiac is alive and guaranteeing 100% success")
    print("=" * 80)
    
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=False)