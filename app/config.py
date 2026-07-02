from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


def _parse_ids(raw_value: str) -> set[int]:
    ids: set[int] = set()
    for part in raw_value.split(","):
        value = part.strip()
        if not value:
            continue
        try:
            ids.add(int(value))
        except ValueError:
            raise ValueError(f"VK ID должен быть числом, получено: {value}") from None
    return ids


@dataclass(frozen=True)
class Settings:
    vk_group_token: str
    admin_vk_ids: set[int]
    allowed_vk_ids: set[int]
    cases_xlsx_path: Path
    db_path: Path
    log_level: str = "INFO"


def load_settings() -> Settings:
    load_dotenv()

    admin_ids = _parse_ids(os.getenv("ADMIN_VK_IDS", ""))
    allowed_ids = _parse_ids(os.getenv("ALLOWED_VK_IDS", ""))

    return Settings(
        vk_group_token=os.getenv("VK_GROUP_TOKEN", "").strip(),
        admin_vk_ids=admin_ids,
        allowed_vk_ids=allowed_ids | admin_ids,
        cases_xlsx_path=Path(os.getenv("CASES_XLSX_PATH", "data/cases.xlsx")),
        db_path=Path(os.getenv("DB_PATH", "data/cases.db")),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )
