"""
Données NOC — mn Zabbix API
"""
import os
from zabbix_client import ZabbixClient

# ============ ZABBIX CONFIG ============
ZABBIX_URL = os.getenv("ZABBIX_URL", "http://localhost:8080/api_jsonrpc.php")
ZABBIX_USER = os.getenv("ZABBIX_USER", "Admin")
ZABBIX_PASSWORD = os.getenv("ZABBIX_PASSWORD", "zabbix")

# ============ CLIENT ============
zabbix = ZabbixClient(ZABBIX_URL, ZABBIX_USER, ZABBIX_PASSWORD)


# ============ ALERTES ============
def get_alerts():
    """Jbed alertes mn Zabbix"""
    alerts = zabbix.get_alerts()
    if not alerts:
        return [
            {"id": 1, "sev": "INFO", "sevClass": "info", "src": "SYSTEM", "txt": "Aucune alerte active", "time": "--:--", "state": "ACK"}
        ]
    return alerts


# ============ STATS ============
def get_stats():
    """Stats mn Zabbix"""
    stats = zabbix.get_stats()
    if not stats:
        return {"hosts_total": 0, "hosts_available": 0, "hosts_down": 0, "health": 0, "alerts_critical": 0, "alerts_warning": 0, "alerts_total": 0, "availability": 0}
    return stats


# ============ HOSTS ============
def get_hosts():
    """Hôtes mn Zabbix"""
    return zabbix.get_hosts()


# ============ ACK INCIDENT ============
def acknowledge_incident(event_id):
    """ACK mn Zabbix"""
    return zabbix.acknowledge(event_id)


# ============ SIMULATE INCIDENT ============
def simulate_incident():
    """Demo"""
    from datetime import datetime
    return {
        "id": 999,
        "sev": "CRITIQUE",
        "src": "SIMULATOR",
        "txt": "Incident simulé",
        "time": datetime.now().strftime("%H:%M"),
        "state": "OPEN"
    }


# ============ USERS ============
USERS = [
    {"id": 1, "username": "admin", "password": "admin123", "role": "admin", "name": "Administrateur NOC"},
    {"id": 2, "username": "operator", "password": "operator123", "role": "operator", "name": "Opérateur NOC"},
    {"id": 3, "username": "viewer", "password": "viewer123", "role": "viewer", "name": "Consultation"}
]


def authenticate(username, password):
    """Kayverifi credentials"""
    for u in USERS:
        if u["username"] == username and u["password"] == password:
            return {"id": u["id"], "username": u["username"], "role": u["role"], "name": u["name"]}
    return None


def get_user(username):
    """Kayjbed user b username"""
    for u in USERS:
        if u["username"] == username:
            return {"id": u["id"], "username": u["username"], "role": u["role"], "name": u["name"]}
    return None