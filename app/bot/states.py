WAITING_CASE_QUERY = "waiting_case_query"
WAITING_NICHE_QUERY = "waiting_niche_query"
WAITING_TOOL_QUERY = "waiting_tool_query"
WAITING_GOAL_QUERY = "waiting_goal_query"

user_states: dict[int, str] = {}


def set_state(user_id: int, state: str) -> None:
    user_states[user_id] = state


def get_state(user_id: int) -> str | None:
    return user_states.get(user_id)


def clear_state(user_id: int) -> None:
    user_states.pop(user_id, None)
