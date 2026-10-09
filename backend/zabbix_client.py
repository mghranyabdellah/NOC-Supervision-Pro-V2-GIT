"""
Zabbix Client — Connecti m3a Zabbix API
"""
from pyzabbix import ZabbixAPI
import time


class ZabbixClient:
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password
        self.zapi = None
        self._connect()

    def _connect(self):
        """Connecti m3a Zabbix"""
        try:
            self.zapi = ZabbixAPI(self.url)
            self.zapi.login(self.user, self.password)
            print(f"✅ Connecté à Zabbix: {self.url}")
        except Exception as e:
            print(f"❌ Erreur connexion Zabbix: {e}")
            self.zapi = None

    SEVERITY_MAP = {
        "0": ("INFO", "info"),
        "1": ("INFO", "info"),
        "2": ("AVERT.", "warn"),
        "3": ("MAJEUR", "warn"),
        "4": ("CRITIQUE", "crit"),
        "5": ("CRITIQUE", "crit"),
    }

    def get_alerts(self, limit=20):
        """Jbed les alertes (problems) mn Zabbix"""
        if not self.zapi:
            return []
        try:
            problems = self.zapi.problem.get(
                output="extend",
                selectHosts=["host"],
                recent=True,
                sortfield=["eventid"],
                sortorder="DESC",
                limit=limit
            )
            alerts = []
            for p in problems:
                sev_text, sev_class = self.SEVERITY_MAP.get(
                    p.get("severity", "0"), ("INFO", "info")
                )
                host = (p.get("hosts") or [{}])[0].get("host", "UNKNOWN")
                clock = int(p.get("clock", time.time()))
                alerts.append({
                    "id": int(p.get("eventid", 0)),
                    "sev": sev_text,
                    "sevClass": sev_class,
                    "src": host,
                    "txt": p.get("name", "Alerte"),
                    "time": time.strftime("%H:%M", time.localtime(clock)),
                    "state": "ACK" if p.get("acknowledged") == "1" else "OPEN"
                })
            return alerts
        except Exception as e:
            print(f"⚠️ Erreur get_alerts: {e}")
            return []

    def get_hosts(self):
        """Jbed la liste dyal les hôtes"""
        if not self.zapi:
            return []
        try:
            hosts = self.zapi.host.get(
                output=["hostid", "host", "status", "available"],
                selectInterfaces=["ip"]
            )
            result = []
            for h in hosts:
                ifaces = h.get("interfaces") or [{}]
                result.append({
                    "id": h.get("hostid"),
                    "name": h.get("host"),
                    "ip": ifaces[0].get("ip", "N/A"),
                    "status": "OK" if h.get("available") == "1" else "DOWN",
                    "enabled": h.get("status") == "0"
                })
            return result
        except Exception as e:
            print(f"⚠️ Erreur get_hosts: {e}")
            return []

    def get_stats(self):
        """Stats globales"""
        if not self.zapi:
            return None
        try:
            hosts = self.zapi.host.get(output=["hostid", "available"])
            total = len(hosts)
            available = sum(1 for h in hosts if h.get("available") == "1")
            problems = self.zapi.problem.get(recent=True)
            critical = sum(1 for p in problems if int(p.get("severity", 0)) >= 4)
            warning = sum(1 for p in problems if 2 <= int(p.get("severity", 0)) < 4)
            pct = round((available / total * 100), 2) if total else 0
            return {
                "hosts_total": total,
                "hosts_available": available,
                "hosts_down": total - available,
                "health": pct,
                "alerts_critical": critical,
                "alerts_warning": warning,
                "alerts_total": len(problems),
                "availability": pct,
            }
        except Exception as e:
            print(f"⚠️ Erreur get_stats: {e}")
            return None

    def acknowledge(self, event_id, message="ACK from NOC"):
        """ACK wahed incident"""
        if not self.zapi:
            return {"success": False, "error": "Zabbix mashi connecté"}
        try:
            self.zapi.event.acknowledge(
                eventids=[event_id], action=6, message=message
            )
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}