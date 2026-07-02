from pathlib import Path
import logging

from vkbottle.bot import Bot

from app.bot.handlers import setup_handlers
from app.cases.importer import import_cases_from_excel
from app.cases.repository import CaseRepository
from app.cases.search import CaseSearchService
from app.config import load_settings
from app.utils.logging import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    settings = load_settings()
    setup_logging(settings.log_level)

    if not settings.vk_group_token:
        raise RuntimeError("VK_GROUP_TOKEN не задан. Создай .env по примеру .env.example.")
    if not settings.allowed_vk_ids:
        logger.warning("ALLOWED_VK_IDS пустой: бот никому не даст доступ, кроме добавленных позже ID.")

    repository = CaseRepository(settings.db_path)
    _auto_import_if_needed(repository, settings.cases_xlsx_path)

    bot = Bot(token=settings.vk_group_token)
    setup_handlers(bot, settings, repository, CaseSearchService(repository))

    logger.info("Запускаю VK Long Poll бота")
    bot.run_forever()


def _auto_import_if_needed(repository: CaseRepository, xlsx_path: Path) -> None:
    if repository.count() > 0:
        return
    if not xlsx_path.exists():
        logger.warning("База пустая, Excel-файл %s не найден. Бот запустится без кейсов.", xlsx_path)
        return

    summary = import_cases_from_excel(xlsx_path, repository)
    logger.info("Первичный импорт завершён: %s кейсов", summary.imported_count)


if __name__ == "__main__":
    main()
