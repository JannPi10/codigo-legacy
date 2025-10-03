from autoservice.manager import AutoServiceManager
from autoservice.repositories.memory_repo import InMemoryAppointmentRepository
from autoservice.email_services import SpyEmailService
from autoservice.time_providers import FakeTimeProvider
from autoservice.domain import Client
from datetime import datetime

def test_dependencies_are_injected_and_replaceable():
    repo = InMemoryAppointmentRepository()
    cid = repo.add_client(Client(id=None, name="Jann", email="jann@example.com"))
    tp = FakeTimeProvider(datetime(2025,1,1,8,0,0))
    spy = SpyEmailService()
    mgr = AutoServiceManager(time=tp, email=spy, repo=repo)

    appt_id = mgr.create_appointment(client_id=cid, description="Diagnóstico")
    assert repo.get_appointment(appt_id) is not None
    assert spy.calls[0]["to"] == "jann@example.com"
