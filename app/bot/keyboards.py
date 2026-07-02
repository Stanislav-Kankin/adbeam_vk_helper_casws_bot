from vkbottle import Keyboard, KeyboardButtonColor, Text


BTN_FIND = "🔎 Найти кейс"
BTN_BY_NICHE = "📂 Кейсы по нише"
BTN_BY_TOOL = "🛠 Кейсы по инструменту"
BTN_BY_GOAL = "🎯 Кейсы по цели"
BTN_STATS = "📊 Статистика базы"
BTN_RELOAD = "🔄 Обновить базу"
BTN_HELP = "❓ Помощь"
BTN_MENU = "⬅️ В меню"

TOOL_OPTIONS = (
    "Яндекс Директ",
    "Промостраницы",
    "VK Ads",
    "LinkedIn",
    "Email outreach",
    "SEO",
    "Telegram",
    "Другое",
)

GOAL_OPTIONS = (
    "Покупки",
    "Лиды",
    "Заявки",
    "Рост продаж",
    "ROMI / ДРР",
    "Brandformance",
    "Выход из маркетплейсов",
    "Другое",
)

DEFAULT_NICHES = (
    "Ecom",
    "Парфюмерия",
    "B2B",
    "Недвижимость",
    "Образование",
    "Медицина",
)


def main_menu_keyboard() -> str:
    keyboard = Keyboard(one_time=False, inline=False)
    keyboard.add(Text(BTN_FIND), color=KeyboardButtonColor.POSITIVE)
    keyboard.row()
    keyboard.add(Text(BTN_BY_NICHE), color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text(BTN_BY_TOOL), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text(BTN_BY_GOAL), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text(BTN_STATS), color=KeyboardButtonColor.SECONDARY)
    keyboard.add(Text(BTN_RELOAD), color=KeyboardButtonColor.SECONDARY)
    keyboard.row()
    keyboard.add(Text(BTN_HELP), color=KeyboardButtonColor.SECONDARY)
    return keyboard.get_json()


def options_keyboard(options: list[str] | tuple[str, ...]) -> str:
    keyboard = Keyboard(one_time=False, inline=False)
    for index, option in enumerate(options):
        if index and index % 2 == 0:
            keyboard.row()
        keyboard.add(Text(option), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text(BTN_MENU), color=KeyboardButtonColor.SECONDARY)
    return keyboard.get_json()


def menu_only_keyboard() -> str:
    keyboard = Keyboard(one_time=False, inline=False)
    keyboard.add(Text(BTN_MENU), color=KeyboardButtonColor.SECONDARY)
    return keyboard.get_json()
