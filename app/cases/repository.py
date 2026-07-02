from collections import Counter
from datetime import datetime
from pathlib import Path
import sqlite3

from app.cases.models import CaseItem
from app.db.sqlite import connect_db, init_db


CASE_COLUMNS = (
    "source_sheet",
    "project",
    "title",
    "case_url",
    "niche",
    "niche_extra",
    "goal",
    "tool",
    "geo",
    "audience",
    "storage_url",
    "search_text",
    "created_at",
    "updated_at",
)


class CaseRepository:
    def __init__(self, db_path: Path) -> None:
        self.connection = connect_db(db_path)
        init_db(self.connection)

    def count(self) -> int:
        row = self.connection.execute("SELECT COUNT(*) AS total FROM cases").fetchone()
        return int(row["total"])

    def replace_all(self, cases: list[CaseItem]) -> None:
        now = datetime.now().isoformat(timespec="seconds")
        with self.connection:
            self.connection.execute("DELETE FROM cases")
            for case in cases:
                case.created_at = case.created_at or now
                case.updated_at = now
                self.connection.execute(
                    f"""
                    INSERT INTO cases ({", ".join(CASE_COLUMNS)})
                    VALUES ({", ".join("?" for _ in CASE_COLUMNS)})
                    """,
                    tuple(getattr(case, column) for column in CASE_COLUMNS),
                )
            self.set_meta("last_import_at", now)

    def list_all(self) -> list[CaseItem]:
        rows = self.connection.execute("SELECT * FROM cases ORDER BY id").fetchall()
        return [self._row_to_case(row) for row in rows]

    def stats_by_source_sheet(self) -> dict[str, int]:
        rows = self.connection.execute(
            "SELECT source_sheet, COUNT(*) AS total FROM cases GROUP BY source_sheet ORDER BY total DESC"
        ).fetchall()
        return {row["source_sheet"] or "Без листа": int(row["total"]) for row in rows}

    def top_values(self, field: str, limit: int = 10) -> list[tuple[str, int]]:
        if field not in {"niche", "tool", "goal"}:
            raise ValueError(f"Поле {field} не поддерживается для статистики")

        values: list[str] = []
        rows = self.connection.execute(f"SELECT {field} FROM cases").fetchall()
        for row in rows:
            raw_value = row[field] or ""
            parts = [part.strip() for part in raw_value.replace(";", ",").split(",")]
            values.extend(part for part in parts if part)

        return Counter(values).most_common(limit)

    def set_meta(self, key: str, value: str) -> None:
        self.connection.execute(
            "INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)",
            (key, value),
        )

    def get_meta(self, key: str, default: str = "") -> str:
        row = self.connection.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
        return str(row["value"]) if row else default

    @staticmethod
    def _row_to_case(row: sqlite3.Row) -> CaseItem:
        return CaseItem(**{key: row[key] for key in row.keys()})
