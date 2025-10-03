import sqlite3
import pytest
from datetime import datetime
from autoservice.time_providers import FakeTimeProvider
from autoservice.repositories.base import init_schema, with_fk
from autoservice.repositories.sqlite_repo import SQLiteAppointmentRepository
from autoservice.repositories.memory_repo import InMemoryAppointmentRepository
from autoservice.domain import Client

@pytest.fixture(scope="session")
def fixed_time():
    return datetime(2025, 1, 1, 10, 0, 0)

@pytest.fixture()
def time_provider(fixed_time):
    return FakeTimeProvider(fixed_time)

@pytest.fixture()
def db_conn():
    conn = sqlite3.connect(":memory:")
    conn.isolation_level = None 
    with_fk(conn)
    init_schema(conn)
    yield conn
    conn.close()

@pytest.fixture()
def sqlite_repo(db_conn):
    return SQLiteAppointmentRepository(db_conn)

@pytest.fixture()
def memory_repo():
    return InMemoryAppointmentRepository()

@pytest.fixture()
def seed_client(sqlite_repo, memory_repo):
    def _seed(repo):
        return repo.add_client(Client(id=None, name="Jann", email="jann@example.com"))
    return _seed
