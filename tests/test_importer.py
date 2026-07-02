from pathlib import Path

import pandas as pd

from app.cases.importer import import_cases_from_excel
from app.cases.repository import CaseRepository


def test_importer_skips_empty_rows_and_imports_cases(tmp_path: Path) -> None:
    xlsx_path = tmp_path / "cases.xlsx"
    db_path = tmp_path / "cases.db"
    frame = pd.DataFrame(
        [
            {
                "Проект": "AdBeam",
                "Название кейса": "Парфюм через Директ",
                "Ссылка на кейс": "https://example.com/case",
                "Ниша": "Парфюмерия",
                "Инструмент": "Яндекс Директ",
            },
            {},
        ]
    )
    frame.to_excel(xlsx_path, index=False, sheet_name="Adbeam RU")

    repository = CaseRepository(db_path)
    summary = import_cases_from_excel(xlsx_path, repository)

    assert summary.imported_count == 1
    assert repository.count() == 1
    case = repository.list_all()[0]
    assert case.title == "Парфюм через Директ"
    assert "парфюм" in case.search_text
