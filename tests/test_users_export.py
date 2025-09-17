from __future__ import annotations
import asyncio
import csv
import io
import sys
import types
from datetime import datetime, timezone
from pathlib import Path
from typing import Generic, TypeVar

sys.path.append(str(Path(__file__).resolve().parents[1]))

sqlalchemy_stub = types.ModuleType("sqlalchemy")
sqlalchemy_stub.BigInteger = int


def _text(value: str) -> str:
    return value


sqlalchemy_stub.text = _text
orm_stub = types.ModuleType("sqlalchemy.orm")
_T = TypeVar("_T")


class _DeclarativeBase:  # pragma: no cover - stub class
    pass


def _mapped_column(*args: object, **kwargs: object) -> None:  # pragma: no cover - stub function
    return None


class _Mapped(Generic[_T]):  # pragma: no cover - stub class
    pass


orm_stub.DeclarativeBase = _DeclarativeBase
orm_stub.Mapped = _Mapped
orm_stub.mapped_column = _mapped_column
sqlalchemy_stub.orm = orm_stub
sys.modules.setdefault("sqlalchemy", sqlalchemy_stub)
sys.modules.setdefault("sqlalchemy.orm", orm_stub)

aiogram_stub = types.ModuleType("aiogram")
types_stub = types.ModuleType("aiogram.types")


class _BufferedInputFile:  # pragma: no cover - stub class
    def __init__(self, *, file: bytes, filename: str) -> None:
        self.file = file
        self.filename = filename


types_stub.BufferedInputFile = _BufferedInputFile
aiogram_stub.types = types_stub
sys.modules.setdefault("aiogram", aiogram_stub)
sys.modules.setdefault("aiogram.types", types_stub)

from bot.utils.users_export import convert_users_to_csv  # noqa: E402


class DummyColumn:
    def __init__(self, name: str) -> None:
        self.name = name


class DummyUserModel:
    column_names = [
        "id",
        "first_name",
        "last_name",
        "username",
        "language_code",
        "referrer",
        "created_at",
        "is_admin",
        "is_suspicious",
        "is_block",
        "is_premium",
    ]
    __table__ = types.SimpleNamespace(columns=[DummyColumn(name) for name in column_names])

    def __init__(self, **kwargs: object) -> None:
        for column in self.__table__.columns:
            setattr(self, column.name, kwargs.get(column.name))


convert_users_to_csv.__globals__["UserModel"] = DummyUserModel


def test_convert_users_to_csv_writes_column_names() -> None:
    user = DummyUserModel(
        id=1,
        first_name="Alice",
        last_name=None,
        username="alice",
        language_code="en",
        referrer=None,
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        is_admin=False,
        is_suspicious=False,
        is_block=False,
        is_premium=True,
    )

    csv_file = asyncio.run(convert_users_to_csv([user]))

    content = csv_file.file.decode("utf-8")
    rows = list(csv.reader(io.StringIO(content)))
    expected_header = [column.name for column in DummyUserModel.__table__.columns]

    assert rows[0] == expected_header
    assert rows[1][expected_header.index("first_name")] == "Alice"
