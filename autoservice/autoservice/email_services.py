from __future__ import annotations
from typing import List, Dict

class ConsoleEmailService:
    def send(self, *, to: str, subject: str, body: str) -> None:
        print(f"EMAIL -> to={to} subject={subject} body={body}")

class MockEmailService:
    def __init__(self, expected: Dict[str, str]):
        self.expected = expected
        self.called = False

    def send(self, *, to: str, subject: str, body: str) -> None:
        assert to == self.expected["to"], f"to != {self.expected['to']}"
        assert subject == self.expected["subject"], f"subject != {self.expected['subject']}"
        assert body == self.expected["body"], f"body != {self.expected['body']}"
        self.called = True

class SpyEmailService:
    def __init__(self):
        self.calls: List[Dict[str,str]] = []

    def send(self, *, to: str, subject: str, body: str) -> None:
        self.calls.append({"to": to, "subject": subject, "body": body})
