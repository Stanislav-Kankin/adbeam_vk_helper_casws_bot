CREATE TABLE IF NOT EXISTS cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_sheet TEXT,
    project TEXT,
    title TEXT,
    case_url TEXT,
    niche TEXT,
    niche_extra TEXT,
    goal TEXT,
    tool TEXT,
    geo TEXT,
    audience TEXT,
    storage_url TEXT,
    search_text TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT
);
