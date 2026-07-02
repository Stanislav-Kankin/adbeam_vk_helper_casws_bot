from pathlib import Path
import logging

from vkbottle.bot import Bot, Message

from app.bot.access import ACCESS_DENIED_TEXT, ADMIN_ONLY_TEXT, is_admin, is_allowed
from app.bot.formatters import EMPTY_DATABASE_TEXT, HELP_TEXT, format_search_results, format_stats
from app.bot.keyboards import (
    BTN_BY_GOAL,
    BTN_BY_NICHE,
    BTN_BY_TOOL,
    BTN_FIND,
    BTN_HELP,
    BTN_MENU,
    BTN_RELOAD,
    BTN_STATS,
    DEFAULT_NICHES,
    GOAL_OPTIONS,
    TOOL_OPTIONS,
    main_menu_keyboard,
    menu_only_keyboard,
    options_keyboard,
)
from app.bot.states import (
    WAITING_CASE_QUERY,
    WAITING_GOAL_QUERY,
    WAITING_NICHE_QUERY,
    WAITING_TOOL_QUERY,
    clear_state,
    get_state,
    set_state,
)
from app.cases.importer import import_cases_from_excel
from app.cases.repository import CaseRepository
from app.cases.search import CaseSearchService
from app.config import Settings
from app.utils.text import normalize_text

logger = logging.getLogger(__name__)


START_WORDS = {"/start", "start", "начать", "привет", "здравствуй", "здравствуйте", "меню"}


def setup_handlers(
    bot: Bot,
    settings: Settings,
    repository: CaseRepository,
    search_service: CaseSearchService,
) -> None:
    @bot.on.message()
    async def handle_message(message: Message) -> None:
        user_id = int(message.from_id)
        text = (message.text or "").strip()
        normalized = normalize_text(text)

        if not is_allowed(settings, user_id):
            await message.answer(ACCESS_DENIED_TEXT)
            return

        if normalized in START_WORDS or text == BTN_MENU:
            clear_state(user_id)
            await message.answer(
                "Привет! Я помогу найти подходящий кейс AdBeam. Выбери действие:",
                keyboard=main_menu_keyboard(),
            )
            return

        if text == BTN_HELP or normalized == "/help":
            clear_state(user_id)
            await message.answer(HELP_TEXT, keyboard=main_menu_keyboard())
            return

        if text == BTN_FIND:
            set_state(user_id, WAITING_CASE_QUERY)
            await message.answer(
                "Напиши, какой кейс ищем.\n\nПримеры:\n— парфюм директ\n— маркетплейсы\n— промостраницы\n— b2b linkedin\n— ecom romi",
                keyboard=menu_only_keyboard(),
            )
            return

        if text == BTN_BY_NICHE:
            if repository.count() == 0:
                await message.answer(EMPTY_DATABASE_TEXT, keyboard=main_menu_keyboard())
                return

            set_state(user_id, WAITING_NICHE_QUERY)
            niches = _top_option_names(repository.top_values("niche", limit=8), DEFAULT_NICHES)
            await message.answer(
                "Выбери нишу или напиши свою:",
                keyboard=options_keyboard(niches),
            )
            return

        if text == BTN_BY_TOOL:
            if repository.count() == 0:
                await message.answer(EMPTY_DATABASE_TEXT, keyboard=main_menu_keyboard())
                return

            set_state(user_id, WAITING_TOOL_QUERY)
            await message.answer("Выбери инструмент или напиши свой:", keyboard=options_keyboard(TOOL_OPTIONS))
            return

        if text == BTN_BY_GOAL:
            if repository.count() == 0:
                await message.answer(EMPTY_DATABASE_TEXT, keyboard=main_menu_keyboard())
                return

            set_state(user_id, WAITING_GOAL_QUERY)
            await message.answer("Выбери цель или напиши свою:", keyboard=options_keyboard(GOAL_OPTIONS))
            return

        if text == BTN_STATS or normalized == "/stats":
            await _send_stats(message, settings, repository)
            return

        if text == BTN_RELOAD or normalized == "/reload_cases":
            await _reload_cases(message, settings, repository)
            return

        if normalized.startswith("/case"):
            query = text[5:].strip()
            if not query:
                set_state(user_id, WAITING_CASE_QUERY)
                await message.answer("Напиши запрос после команды или следующим сообщением.", keyboard=menu_only_keyboard())
                return
            await _send_search_results(message, search_service, query)
            return

        if normalized == "/filters":
            clear_state(user_id)
            await message.answer(
                "Фильтры доступны кнопками: ниша, инструмент, цель. Можно также просто написать запрос через /case <запрос>.",
                keyboard=main_menu_keyboard(),
            )
            return

        state = get_state(user_id)
        if state:
            await _handle_state_query(message, user_id, state, search_service, text)
            return

        await message.answer("Я не понял команду. Выбери действие в меню.", keyboard=main_menu_keyboard())


async def _handle_state_query(
    message: Message,
    user_id: int,
    state: str,
    search_service: CaseSearchService,
    query: str,
) -> None:
    field = None
    if state == WAITING_NICHE_QUERY:
        field = "niche"
    elif state == WAITING_TOOL_QUERY:
        field = "tool"
    elif state == WAITING_GOAL_QUERY:
        field = "goal"
    elif state != WAITING_CASE_QUERY:
        logger.warning("Неизвестное состояние пользователя %s: %s", user_id, state)

    clear_state(user_id)
    await _send_search_results(message, search_service, query, field=field)


async def _send_search_results(
    message: Message,
    search_service: CaseSearchService,
    query: str,
    field: str | None = None,
) -> None:
    if search_service.repository.count() == 0:
        await message.answer(EMPTY_DATABASE_TEXT, keyboard=main_menu_keyboard())
        return

    results = search_service.search(query, limit=5, field=field)
    await message.answer(format_search_results(results), keyboard=main_menu_keyboard())


async def _send_stats(message: Message, settings: Settings, repository: CaseRepository) -> None:
    if not is_admin(settings, int(message.from_id)):
        await message.answer(ADMIN_ONLY_TEXT, keyboard=main_menu_keyboard())
        return

    await message.answer(
        format_stats(
            total=repository.count(),
            by_source=repository.stats_by_source_sheet(),
            top_niches=repository.top_values("niche"),
            top_tools=repository.top_values("tool"),
            last_import_at=repository.get_meta("last_import_at"),
        ),
        keyboard=main_menu_keyboard(),
    )


async def _reload_cases(message: Message, settings: Settings, repository: CaseRepository) -> None:
    if not is_admin(settings, int(message.from_id)):
        await message.answer(ADMIN_ONLY_TEXT, keyboard=main_menu_keyboard())
        return

    try:
        summary = import_cases_from_excel(Path(settings.cases_xlsx_path), repository)
    except FileNotFoundError:
        await message.answer(
            f"Не нашёл Excel-файл: {settings.cases_xlsx_path}\nПоложи файл в data/cases.xlsx и попробуй ещё раз.",
            keyboard=main_menu_keyboard(),
        )
        return
    except Exception as error:
        logger.exception("Ошибка при обновлении базы")
        await message.answer(f"Не удалось обновить базу: {error}", keyboard=main_menu_keyboard())
        return

    await message.answer(
        f"База обновлена.\nЗагружено кейсов: {summary.imported_count}.\nЛисты: {', '.join(summary.source_sheets)}.",
        keyboard=main_menu_keyboard(),
    )


def _top_option_names(values: list[tuple[str, int]], fallback: tuple[str, ...]) -> list[str]:
    options = [name for name, _ in values if name]
    return options[:8] if options else list(fallback)
