from app.config import Settings


ACCESS_DENIED_TEXT = "Это внутренний бот AdBeam. Доступ ограничен."
ADMIN_ONLY_TEXT = "Эта функция доступна только администратору."


def is_allowed(settings: Settings, user_id: int) -> bool:
    return user_id in settings.allowed_vk_ids


def is_admin(settings: Settings, user_id: int) -> bool:
    return user_id in settings.admin_vk_ids
