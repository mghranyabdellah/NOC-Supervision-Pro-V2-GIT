"""
Données demo dyal NOC
Mn ba3d ila jbti Zabbix, hadchi ghadi ytbedel b données réelles
"""
import time
from datetime import datetime


# ============ ALERTES ============
def get_alerts():
    """Kayrje3 liste dyal les alertes"""
    now = datetime.now()
    return [
        {
            "id": 1,
            "sev": "CRITIQUE",
            "src": "WAN-CORE-01",
            "txt": "Perte de connectivité WAN",
            "time": now.strftime("%H:%M"),
            "state": "OPEN"
        },
        {
            "id": 2,
            "sev": "MAJEUR",
            "src": "FW-EDGE-02",
            "txt": "CPU firewall supérieur au seuil",
            "time": "15:39",
            "state": "OPEN"
        },
        {
            "id": 3,
            "sev": "AVERT.",
            "src": "SRV-APP-15",
            "txt": "Espace disque faible",
            "time": "15:35",
            "state": "OPEN"
        },
        {
            "id": 4,
            "sev": "INFO",
            "src": "BACKUP-03",
            "txt": "Sauvegarde terminée",
            "time": "15:30",
            "state": "ACK"
        }
    ]


# ============ STATS ============
def get_stats():
    """Stats globales"""
    return {
        "hosts_total": 128,
        "hosts_available": 126,
        "hosts_down": 2,
        "health": 98.7,
        "alerts_critical": 1,
        "alerts_warning": 2,
        "alerts_total": 4,
        "availability": 99.96
    }


# ============ HOSTS ============
def get_hosts():
    """Liste dyal les serveurs"""
    return [
        {
            "id": str(i),
            "name": f"SRV-{i:03d}",
            "ip": f"10.0.0.{i}",
            "status": "OK" if i != 15 else "DOWN",
            "enabled": True
        }
        for i in range(1, 21)
    ]


# ============ ACK INCIDENT ============
def acknowledge_incident(event_id):
    """Kaydir ACK l incident (f demo, ghir kayrje3 success)"""
    print(f"✅ ACK incident #{event_id}")
    return {"success": True, "message": f"Incident #{event_id} acquitté"}


# ============ SIMULATE INCIDENT ============
def simulate_incident():
    """Kaysawb incident jdid"""
    return {
        "id": 999,
        "sev": "CRITIQUE",
        "src": "SIMULATOR",
        "txt": "Incident simulé",
        "time": datetime.now().strftime("%H:%M"),
        "state": "OPEN"
    }