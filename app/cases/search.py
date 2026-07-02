from dataclasses import dataclass

from rapidfuzz import fuzz

from app.cases.models import CaseItem
from app.cases.repository import CaseRepository
from app.utils.text import build_search_text, expand_query, normalize_text


FIELD_MAP = {
    "niche": ("niche", "niche_extra"),
    "tool": ("tool",),
    "goal": ("goal",),
}


@dataclass
class SearchResult:
    case: CaseItem
    score: int


class CaseSearchService:
    def __init__(self, repository: CaseRepository) -> None:
        self.repository = repository

    def search(self, query: str, limit: int = 5, field: str | None = None) -> list[SearchResult]:
        query_variants = expand_query(query)
        if not query_variants:
            return []

        results: list[SearchResult] = []
        for case in self.repository.list_all():
            haystack = self._case_field_text(case, field)
            if not haystack:
                continue

            best_score = max(self._score(variant, haystack) for variant in query_variants)
            if best_score >= 55:
                results.append(SearchResult(case=case, score=best_score))

        results.sort(key=lambda item: item.score, reverse=True)
        return results[:limit]

    @staticmethod
    def _score(query: str, haystack: str) -> int:
        normalized_query = normalize_text(query)
        if not normalized_query:
            return 0
        if normalized_query == haystack:
            return 100
        if normalized_query in haystack:
            return 95
        return int(fuzz.token_set_ratio(normalized_query, haystack))

    @staticmethod
    def _case_field_text(case: CaseItem, field: str | None) -> str:
        if not field:
            return case.search_text or build_search_text(
                (
                    case.project,
                    case.title,
                    case.case_url,
                    case.niche,
                    case.niche_extra,
                    case.goal,
                    case.tool,
                    case.geo,
                    case.audience,
                    case.storage_url,
                )
            )

        fields = FIELD_MAP.get(field)
        if not fields:
            raise ValueError(f"Неизвестное поле поиска: {field}")
        return build_search_text(getattr(case, attr) for attr in fields)
