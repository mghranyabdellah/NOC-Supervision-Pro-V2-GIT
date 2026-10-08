"""
NOC Backend API — FastAPI
Kaytjbed données o kay3tihom l frontend
"""
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import data
import time
import secrets


# ============ APP ============
app = FastAPI(
    title="NOC Supervision API",
    description="Backend dyal NOC — données demo + Zabbix ready",
    version="1.0.0"
)


# ============ CORS ============
# Bach l'frontend (fichier HTML) y9der yappel API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ MODELS ============
class AckRequest(BaseModel):
    event_id: int
    message: Optional[str] = "ACK from NOC dashboard"
class LoginRequest(BaseModel):
    username: str
    password: str

# ============ ROUTES ============

@app.get("/")
def root():
    """Page d'accueil dyal API"""
    return {
        "service": "NOC Supervision API",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs"
    }

# ============ LOGIN ============
active_tokens = {}  # { token: user_info }


@app.post("/api/login")
def api_login(req: LoginRequest):
    """Login dyal user"""
    user = data.authenticate(req.username, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Username wla password ghalet")

    token = secrets.token_hex(32)
    active_tokens[token] = user

    return {
        "success": True,
        "token": token,
        "user": user
    }


@app.post("/api/logout")
def api_logout(token: str = Header(default="", alias="X-Auth-Token")):
    """Logout"""
    if token in active_tokens:
        del active_tokens[token]
    return {"success": True}


@app.get("/api/me")
def api_me(token: str = Header(default="", alias="X-Auth-Token")):
    """Kayrje3 info dyal user li m'connecté"""
    if token not in active_tokens:
        raise HTTPException(status_code=401, detail="Mashi connecté")
    return active_tokens[token]
@app.get("/api/login /api/health")
def health():
    """Check ila API khddam"""
    return {
        "api": "ok",
        "zabbix": "demo",
        "timestamp": int(time.time())
    }


@app.get("/api/alerts")
def api_alerts(limit: int = 20):
    """Jbed les alertes"""
    alerts = data.get_alerts()
    return {"alerts": alerts[:limit], "total": len(alerts)}


@app.get("/api/stats")
def api_stats():
    """Jbed les stats"""
    return data.get_stats()


@app.get("/api/hosts")
def api_hosts():
    """Jbed liste dyal les hôtes"""
    hosts = data.get_hosts()
    return {"hosts": hosts, "total": len(hosts)}


@app.get("/api/dashboard")
def api_dashboard():
    """Kolchi b requête wahda"""
    return {
        "stats": data.get_stats(),
        "alerts": data.get_alerts()[:10],
        "hosts": data.get_hosts()[:20],
        "timestamp": int(time.time())
    }


@app.post("/api/acknowledge")
def api_acknowledge(req: AckRequest):
    """ACK wahed incident"""
    try:
        result = data.acknowledge_incident(req.event_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/simulate")
def api_simulate():
    """Sawb incident simulé"""
    return data.simulate_incident()


# ============ LANCEMENT ============
# ============ LANCEMENT ============
if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("🚀 Démarrage NOC Backend API...")
    print("=" * 50)
    print("📖 Docs:  http://localhost:8000/docs")
    print("🌐 API:   http://localhost:8000")
    print("=" * 50)
    uvicorn.run("main:app", host="0.0.0.0", port=8000,)
