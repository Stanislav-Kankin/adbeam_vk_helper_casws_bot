from dataclasses import dataclass


@dataclass
class CaseItem:
    id: int | None = None
    source_sheet: str = ""
    project: str = ""
    title: str = ""
    case_url: str = ""
    niche: str = ""
    niche_extra: str = ""
    goal: str = ""
    tool: str = ""
    geo: str = ""
    audience: str = ""
    storage_url: str = ""
    search_text: str = ""
    created_at: str = ""
    updated_at: str = ""
