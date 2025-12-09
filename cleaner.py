import sqlite3
import json
import re

DB_PATH = "x-ui.db"  

UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}$"
)

class XUIcleaner:

    def __init__(self, db_path: str):
        self.db_path = db_path

        self.uuid: str | None = None
        self.email: str | None = None


    def delete_client(self, identifier: str) -> dict:
        found = self._resolve_client(identifier)
        if not found:
            return {
                "status": "not_found",
                "identifier": identifier
            }

        inbounds_deleted = self._delete_from_inbounds()
        tables_result = self._delete_by_email()

        return {
            "status": "ok",
            "uuid": self.uuid,
            "email": self.email,
            "inbounds_deleted": inbounds_deleted,
            "tables_deleted": tables_result
        }


    def _resolve_client(self, identifier: str) -> bool:
        is_uuid = bool(UUID_RE.match(identifier))

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT settings FROM inbounds")
        rows = cursor.fetchall()

        for (settings_raw,) in rows:
            if not settings_raw:
                continue

            try:
                settings = json.loads(settings_raw)
            except json.JSONDecodeError:
                continue

            for c in settings.get("clients", []):
                if is_uuid and c.get("id") == identifier:
                    self.uuid = c.get("id")
                    self.email = c.get("email")
                    conn.close()
                    return True

                if not is_uuid and c.get("email") == identifier:
                    self.uuid = c.get("id")
                    self.email = c.get("email")
                    conn.close()
                    return True

        conn.close()
        return False


    def _delete_from_inbounds(self) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id, settings FROM inbounds")
        rows = cursor.fetchall()

        deleted = 0

        for inbound_id, settings_raw in rows:
            if not settings_raw:
                continue

            try:
                settings = json.loads(settings_raw)
            except json.JSONDecodeError:
                continue

            clients = settings.get("clients", [])
            before = len(clients)

            clients = [
                c for c in clients
                if c.get("id") != self.uuid
                and c.get("email") != self.email
            ]

            if len(clients) == before:
                continue

            settings["clients"] = clients

            cursor.execute(
                "UPDATE inbounds SET settings = ? WHERE id = ?",
                (json.dumps(settings, ensure_ascii=False), inbound_id)
            )

            deleted += 1

        conn.commit()
        conn.close()

        return deleted



    def _delete_by_email(self) -> dict:
        if not self.email:
            return {"inbound_client_ips": 0, "client_traffics": 0}

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM inbound_client_ips WHERE email = ?",
            (self.email,)
        )
        ips_deleted = cursor.rowcount

        cursor.execute(
            "DELETE FROM client_traffics WHERE email = ?",
            (self.email,)
        )
        traffics_deleted = cursor.rowcount

        conn.commit()
        conn.close()

        return {
            "inbound_client_ips": ips_deleted,
            "client_traffics": traffics_deleted,
        }