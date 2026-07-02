from app.cases.models import CaseItem
from app.cases.use_rules import sales_tip


def test_sales_tip_for_ecom() -> None:
    text = sales_tip(CaseItem(niche="Ecom"))
    assert "рост продаж" in text


def test_sales_tip_for_direct() -> None:
    text = sales_tip(CaseItem(tool="Яндекс Директ"))
    assert "performance" in text


def test_sales_tip_for_b2b() -> None:
    text = sales_tip(CaseItem(audience="B2B"))
    assert "B2B" in text
