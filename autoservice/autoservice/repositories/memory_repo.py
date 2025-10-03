from __future__ import annotations
from typing import Iterable, Optional, Dict, List
from datetime import datetime
from ..domain import Client, Appointment, Invoice
from ..interfaces import AppointmentRepository

class InMemoryAppointmentRepository(AppointmentRepository):
    def __init__(self):
        self._clients: Dict[int, Client] = {}
        self._appointments: Dict[int, Appointment] = {}
        self._invoices: Dict[int, Invoice] = {}
        self._id_c = 1
        self._id_a = 1
        self._id_i = 1

    def add_client(self, client: Client) -> int:
        cid = self._id_c; self._id_c += 1
        self._clients[cid] = Client(id=cid, name=client.name, email=client.email)
        return cid

    def get_client(self, client_id: int) -> Optional[Client]:
        return self._clients.get(client_id)

    def get_client_email(self, client_id: int) -> str:
        c = self._clients.get(client_id)
        if not c: raise ValueError("Client not found")
        return c.email

    def create_appointment(self, client_id: int, when: datetime, description: str) -> int:
        if client_id not in self._clients:
            raise ValueError("Client not found")
        aid = self._id_a; self._id_a += 1
        self._appointments[aid] = Appointment(id=aid, client_id=client_id, when=when, description=description)
        return aid

    def get_appointment(self, appointment_id: int) -> Optional[Appointment]:
        return self._appointments.get(appointment_id)

    def list_appointments(self) -> Iterable[Appointment]:
        for k in sorted(self._appointments.keys()):
            yield self._appointments[k]

    def create_invoice(self, appointment_id: int, amount: float, issued_at: datetime) -> int:
        if appointment_id not in self._appointments:
            raise ValueError("Appointment not found")
        iid = self._id_i; self._id_i += 1
        self._invoices[iid] = Invoice(id=iid, appointment_id=appointment_id, amount=amount, issued_at=issued_at)
        return iid

    def count_appointments(self) -> int:
        return len(self._appointments)
