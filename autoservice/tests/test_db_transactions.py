import sqlite3
import pytest
from autoservice.manager import AutoServiceManager
from autoservice.email_services import SpyEmailService
from autoservice.uow import SQLiteUnitOfWork

def test_insert_appointment_persists_and_rollback(sqlite_repo, time_provider, seed_client, db_conn):
    client_id = seed_client(sqlite_repo)

    spy = SpyEmailService()
    mgr = AutoServiceManager(time=time_provider, email=spy, repo=sqlite_repo)

    with SQLiteUnitOfWork(db_conn):
        appt_id = mgr.create_appointment(client_id=client_id, description="Cambio de aceite")
        assert sqlite_repo.get_appointment(appt_id) is not None

    class ExplodingEmail:
        def send(self, *, to: str, subject: str, body: str) -> None:
            raise RuntimeError("SMTP caído")

    mgr2 = AutoServiceManager(time=time_provider, email=ExplodingEmail(), repo=sqlite_repo)
    before = sqlite_repo.count_appointments()
    with pytest.raises(RuntimeError):
        with SQLiteUnitOfWork(db_conn):
            mgr2.create_appointment_with_invoice_and_email(client_id=client_id, description="Alineación", amount=50.0)
    after = sqlite_repo.count_appointments()
    assert after == before, "Rollback debe revertir inserciones"

def test_fk_constraints_fail_on_missing_client(sqlite_repo, time_provider):
    with pytest.raises(sqlite3.IntegrityError):
        sqlite_repo.create_appointment(client_id=9999, when=time_provider.now(), description="XYZ")

def test_complex_transaction_success(sqlite_repo, time_provider, seed_client, db_conn):
    client_id = seed_client(sqlite_repo)

    from autoservice.email_services import SpyEmailService
    spy = SpyEmailService()

    mgr = AutoServiceManager(time=time_provider, email=spy, repo=sqlite_repo)
    with SQLiteUnitOfWork(db_conn):
        appt_id = mgr.create_appointment_with_invoice_and_email(
            client_id=client_id, description="Frenos", amount=120.0
        )
    assert sqlite_repo.get_appointment(appt_id) is not None
    assert any("Frenos" in c["body"] for c in spy.calls)
