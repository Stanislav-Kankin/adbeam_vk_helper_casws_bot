from app.cases.models import CaseItem
from app.utils.text import normalize_text


DEFAULT_TIP = "Использовать как дополнительное доказательство экспертизы AdBeam в похожей нише или инструменте."


def sales_tip(case: CaseItem) -> str:
    niche = normalize_text(f"{case.niche} {case.niche_extra}")
    tool = normalize_text(case.tool)
    audience = normalize_text(case.audience)

    if any(marker in niche for marker in ("ecom", "еком", "интернет-магазин")):
        return "Использовать, когда клиенту важно показать рост продаж, direct-канал, ДРР, ROMI или e-commerce экспертизу."
    if "директ" in tool:
        return "Аргумент для разговора про управляемый performance и продажи в собственном канале."
    if "промостраницы" in tool:
        return "Аргумент для разговора про brandformance, прогрев спроса и рост брендовых запросов."
    if "b2b" in audience or "б2б" in audience:
        return "Использовать в B2B-сделках, где важны лиды, длинный цикл, доверие и качество диалогов."
    if any(marker in tool for marker in ("linkedin", "email outreach", "бот", "outreach", "аутрич")):
        return "Использовать как доказательство экспертизы в outbound / B2B lead generation."
    return DEFAULT_TIP
