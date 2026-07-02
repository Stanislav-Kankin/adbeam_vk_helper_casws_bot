from app.cases.models import CaseItem
from app.cases.search import SearchResult
from app.cases.use_rules import sales_tip


def format_case(case: CaseItem, index: int) -> str:
    title = " — ".join(part for part in (case.project, case.title) if part)
    lines = [f"{index}. {title or 'Без названия'}"]

    if case.niche or case.niche_extra:
        niche = " / ".join(part for part in (case.niche, case.niche_extra) if part)
        lines.append(f"Ниша: {niche}")
    if case.goal:
        lines.append(f"Цель: {case.goal}")
    if case.tool:
        lines.append(f"Инструмент: {case.tool}")
    if case.geo:
        lines.append(f"Гео: {case.geo}")
    if case.audience:
        lines.append(f"Аудитория: {case.audience}")

    lines.append("")
    lines.append("Как использовать в продаже:")
    lines.append(sales_tip(case))

    if case.case_url:
        lines.extend(("", "Ссылка:", case.case_url))
    if case.storage_url:
        lines.extend(("", "Где лежит:", case.storage_url))

    return "\n".join(lines)


def format_search_results(results: list[SearchResult]) -> str:
    if not results:
        return "Не нашёл подходящих кейсов. Попробуй другой запрос: нишу, инструмент или цель."

    items = [format_case(result.case, index) for index, result in enumerate(results, start=1)]
    text = "\n\n---\n\n".join(items)
    if len(text) > 3800 and len(results) > 3:
        items = [format_case(result.case, index) for index, result in enumerate(results[:3], start=1)]
        text = "\n\n---\n\n".join(items)
        text += "\n\nПоказал топ-3, потому что ответ получался слишком длинным."
    return text


def format_stats(
    total: int,
    by_source: dict[str, int],
    top_niches: list[tuple[str, int]],
    top_tools: list[tuple[str, int]],
    last_import_at: str,
) -> str:
    lines = [f"Всего кейсов: {total}", ""]
    lines.append("По листам Excel:")
    lines.extend(f"— {sheet}: {count}" for sheet, count in by_source.items())

    lines.extend(("", "Топ ниш:"))
    lines.extend(f"— {name}: {count}" for name, count in top_niches) if top_niches else lines.append("— пока нет данных")

    lines.extend(("", "Топ инструментов:"))
    lines.extend(f"— {name}: {count}" for name, count in top_tools) if top_tools else lines.append("— пока нет данных")

    lines.extend(("", f"Последний импорт: {last_import_at or 'нет данных'}"))
    return "\n".join(lines)


HELP_TEXT = """Я помогаю быстро найти кейсы AdBeam.

Основной сценарий:
1. Нажми кнопку «🔎 Найти кейс».
2. Напиши запрос: например, «парфюм директ», «маркетплейсы», «b2b linkedin».
3. Я покажу самые похожие кейсы.

Кнопки:
— 📂 Кейсы по нише: поиск по нише.
— 🛠 Кейсы по инструменту: Директ, Промостраницы, VK Ads и другие.
— 🎯 Кейсы по цели: лиды, покупки, ROMI, brandformance.
— 📊 Статистика базы и 🔄 Обновить базу доступны только админу.

Команды на всякий случай:
/start — главное меню
/help — помощь
/case <запрос> — поиск
/filters — список фильтров
/stats — статистика для админа
/reload_cases — обновить базу для админа"""
