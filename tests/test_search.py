from pathlib import Path

from app.cases.models import CaseItem
from app.cases.repository import CaseRepository
from app.cases.search import CaseSearchService
from app.utils.text import build_search_text


def _case(title: str, niche: str = "", tool: str = "", audience: str = "") -> CaseItem:
    item = CaseItem(
        source_sheet="test",
        project="AdBeam",
        title=title,
        niche=niche,
        tool=tool,
        audience=audience,
    )
    item.search_text = build_search_text((item.project, item.title, item.niche, item.tool, item.audience))
    return item


def test_search_finds_perfume_case_by_synonym(tmp_path: Path) -> None:
    repository = CaseRepository(tmp_path / "cases.db")
    repository.replace_all([_case("Aroma performance", niche="Парфюмерия", tool="Яндекс Директ")])

    results = CaseSearchService(repository).search("парфюм")

    assert results
    assert results[0].case.title == "Aroma performance"


def test_search_finds_promo_pages(tmp_path: Path) -> None:
    repository = CaseRepository(tmp_path / "cases.db")
    repository.replace_all([_case("Brandformance case", tool="Промостраницы")])

    results = CaseSearchService(repository).search("промостраницы")

    assert results
    assert results[0].case.tool == "Промостраницы"
