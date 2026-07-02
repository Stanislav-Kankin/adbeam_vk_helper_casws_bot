from pathlib import Path

from openpyxl import Workbook

from app.cases.importer import import_cases_from_excel
from app.cases.repository import CaseRepository


def test_importer_skips_empty_rows_and_imports_cases(tmp_path: Path) -> None:
    xlsx_path = tmp_path / "cases.xlsx"
    db_path = tmp_path / "cases.db"
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Adbeam RU"
    worksheet.append(["Проект", "Название кейса", "Ссылка на кейс", "Ниша", "Инструмент"])
    worksheet.append(["AdBeam", "Парфюм через Директ", "https://example.com/case", "Парфюмерия", "Яндекс Директ"])
    worksheet.append([None, None, None, None, None])
    workbook.save(xlsx_path)

    repository = CaseRepository(db_path)
    summary = import_cases_from_excel(xlsx_path, repository)

    assert summary.imported_count == 1
    assert repository.count() == 1
    case = repository.list_all()[0]
    assert case.title == "Парфюм через Директ"
    assert "парфюм" in case.search_text
