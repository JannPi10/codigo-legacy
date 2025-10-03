from autoservice.manager import AutoServiceManager
from autoservice.email_services import MockEmailService, SpyEmailService
from autoservice.time_providers import FakeTimeProvider
from autoservice.repositories.memory_repo import InMemoryAppointmentRepository
from autoservice.domain import Client
from datetime import datetime

class FakePaymentGateway:
    def __init__(self, ok_for_ids=None):
        self.ok_for_ids = ok_for_ids or set()
        self.charges = []

    def charge(self, *, client_id: int, amount: float) -> bool:
        self.charges.append((client_id, amount))
        return client_id in self.ok_for_ids

class NotificationSpy:
    def __init__(self):
        self.events = []

    def notify(self, *, channel: str, payload: dict) -> None:
        self.events.append((channel, payload))

def base_setup():
    repo = InMemoryAppointmentRepository()
    cid = repo.add_client(Client(id=None, name="Jann", email="jann@example.com"))
    tp = FakeTimeProvider(datetime(2025,1,1,12,0,0))
    return repo, cid, tp

def test_mock_email_called_with_exact_payload():
    repo, cid, tp = base_setup()
    expected = {
        "to": "jann@example.com",
        "subject": "Confirmación de cita",
        "body": "Su cita es 2025-01-01T12:00:00 - Revisión general",
    }
    mock = MockEmailService(expected)
    mgr = AutoServiceManager(time=tp, email=mock, repo=repo)
    mgr.create_appointment(client_id=cid, description="Revisión general")
    assert mock.called is True

def test_spy_captures_notifications():
    repo, cid, tp = base_setup()
    spy_email = SpyEmailService()
    notifier = NotificationSpy()

    mgr = AutoServiceManager(time=tp, email=spy_email, repo=repo, notifier=notifier)
    mgr.create_appointment(client_id=cid, description="Alineación")

    assert len(spy_email.calls) == 1
    assert notifier.events and notifier.events[0][0] == "appointments"
    assert notifier.events[0][1]["client_id"] == cid

def test_fake_payment_gateway_controls_flow():
    repo, cid, tp = base_setup()
    spy_email = SpyEmailService()
    pay_ok = FakePaymentGateway(ok_for_ids={cid})

    mgr = AutoServiceManager(time=tp, email=spy_email, repo=repo, payments=pay_ok)
    mgr.create_appointment_with_invoice_and_email(client_id=cid, description="Cambio aceite", amount=30.0)

    assert pay_ok.charges == [(cid, 30.0)]

def test_fake_payment_gateway_rejects_and_raises():
    repo, cid, tp = base_setup()
    spy_email = SpyEmailService()
    pay_fail = FakePaymentGateway(ok_for_ids=set())

    mgr = AutoServiceManager(time=tp, email=spy_email, repo=repo, payments=pay_fail)
    import pytest
    with pytest.raises(RuntimeError):
        mgr.create_appointment_with_invoice_and_email(client_id=cid, description="Cambio aceite", amount=30.0)
