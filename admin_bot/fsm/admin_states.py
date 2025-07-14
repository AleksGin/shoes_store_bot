from aiogram.fsm.state import (
    State,
    StatesGroup,
)

class AdminManagementStates(StatesGroup):
    waiting_for_add_admin_id = State()
    waiting_for_remove_admin_id = State()
    waiting_for_rate_input = State()
    waiting_for_date_input = State()