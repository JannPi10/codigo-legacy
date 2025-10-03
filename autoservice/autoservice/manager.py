from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .interfaces import (
    TimeProvider, EmailService, AppointmentRepository, PaymentGateway, NotificationService
)

@dataclass
class AutoServiceManager:
    time: TimeProvider
    email: EmailService
    repo: AppointmentRepository
    payments: Optional[PaymentGateway] = None
    notifier: Optional[NotificationService] = None

    def create_appointment(self, *, client_id: int, description: str, send_confirmation: bool=True) -> int:
        now = self.time.now()
        appt_id = self.repo.create_appointment(client_id=client_id, when=now, description=description)
        if send_confirmation:
            to_email = self.repo.get_client_email(client_id)
            self.email.send(to=to_email, subject="Confirmación de cita", body=f"Su cita es {now.isoformat()} - {description}")
        if self.notifier:
            self.notifier.notify(channel="appointments", payload={"client_id": client_id, "appointment_id": appt_id})
        return appt_id

    def create_appointment_with_invoice_and_email(self, *, client_id: int, description: str, amount: float) -> int:
        when = self.time.now()
        appt_id = self.repo.create_appointment(client_id=client_id, when=when, description=description)
        self.repo.create_invoice(appointment_id=appt_id, amount=amount, issued_at=when)
        to_email = self.repo.get_client_email(client_id)
        self.email.send(
    to=to_email,
    subject="Cita creada",
    body=f"Su cita '{description}' fue creada y la factura emitida por {amount}."
)
        if self.payments:
            ok = self.payments.charge(client_id=client_id, amount=amount)
            if not ok:
                raise RuntimeError("Pago rechazado")
        return appt_id
