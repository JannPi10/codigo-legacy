from __future__ import annotations
import sqlite3
from typing import Iterable, Optional
from datetime import datetime
from ..domain import Client, Appointment, Invoice
from ..interfaces import AppointmentRepository
from .base import with_fk

class SQLiteAppointmentRepository(AppointmentRepository):
    def __init__(self, conn: sqlite3.Connection):
        self.conn = with_fk(conn)

    def add_client(self, client: Client) -> int:
        cur = self.conn.execute(
            "INSERT INTO clients(name, email) VALUES (?, ?)",
            (client.name, client.email)
        )
        return cur.lastrowid

    def get_client(self, client_id: int) -> Optional[Client]:
        cur = self.conn.execute("SELECT id, name, email FROM clients WHERE id=?", (client_id,))
        row = cur.fetchone()
        if not row:
            return None
        return Client(id=row[0], name=row[1], email=row[2])

    def get_client_email(self, client_id: int) -> str:
        cur = self.conn.execute("SELECT email FROM clients WHERE id=?", (client_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError("Client not found")
        return row[0]

    def create_appointment(self, client_id: int, when: datetime, description: str) -> int:
        cur = self.conn.execute(
            "INSERT INTO appointments(client_id, when_ts, description, status) VALUES (?,?,?,?)",
            (client_id, when.isoformat(), description, 'scheduled')
        )
        return cur.lastrowid

    def get_appointment(self, appointment_id: int) -> Optional[Appointment]:
        cur = self.conn.execute(
            "SELECT id, client_id, when_ts, description, status FROM appointments WHERE id=?",
            (appointment_id,)
        )
        row = cur.fetchone()
        if not row: return None
        return Appointment(id=row[0], client_id=row[1], when=datetime.fromisoformat(row[2]), description=row[3], status=row[4])

    def list_appointments(self) -> Iterable[Appointment]:
        cur = self.conn.execute("SELECT id, client_id, when_ts, description, status FROM appointments ORDER BY id")
        for row in cur.fetchall():
            yield Appointment(id=row[0], client_id=row[1], when=datetime.fromisoformat(row[2]), description=row[3], status=row[4])

    def create_invoice(self, appointment_id: int, amount: float, issued_at: datetime) -> int:
        cur = self.conn.execute(
            "INSERT INTO invoices(appointment_id, amount, issued_at) VALUES (?,?,?)",
            (appointment_id, amount, issued_at.isoformat())
        )
        return cur.lastrowid

    def count_appointments(self) -> int:
        cur = self.conn.execute("SELECT COUNT(*) FROM appointments")
        return int(cur.fetchone()[0])
