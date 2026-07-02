import re
from typing import Iterable


SYNONYM_GROUPS: tuple[tuple[str, ...], ...] = (
    ("мп", "маркетплейс", "маркетплейсы", "wb", "wildberries", "ozon"),
    ("директ", "яндекс директ", "yandex direct"),
    ("промо", "промостраницы", "promo pages"),
    ("еком", "ecom", "e-commerce", "интернет-магазин"),
    ("b2b", "б2б", "бтуби"),
    ("b2c", "б2с"),
    ("лиды", "лидоген", "leadgen", "lead generation"),
    ("бот", "linkedin bot", "outreach", "аутрич"),
    ("парфюм", "парфюмерия", "духи", "aroma"),
)


def normalize_text(value: object) -> str:
    if value is None:
        return ""
    text = str(value).replace("ё", "е").replace("Ё", "Е").lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_column_name(value: object) -> str:
    text = normalize_text(value)
    text = text.replace("\n", " ")
    text = re.sub(r"[^a-zа-я0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def build_search_text(values: Iterable[object]) -> str:
    return normalize_text(" ".join(str(value) for value in values if value))


def expand_query(query: str) -> list[str]:
    normalized = normalize_text(query)
    variants = {normalized}

    for group in SYNONYM_GROUPS:
        if any(term in normalized for term in group):
            variants.update(group)

    return [variant for variant in variants if variant]
