from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Client:
    id: Optional[int]
    name: str
    email: str

@dataclass
class Appointment:
    id: Optional[int]
    client_id: int
    when: datetime
    description: str
    status: str = "scheduled"

@dataclass
class Invoice:
    id: Optional[int]
    appointment_id: int
    amount: float
    issued_at: datetime
