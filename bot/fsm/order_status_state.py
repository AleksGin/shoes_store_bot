from aiogram.fsm.state import (
    State,
    StatesGroup,
)


class OrderStatusState(StatesGroup):
    waiting_order_number = State()
    waiting_order_number_to_delete = State()
    waiting_for_press_tracker_button = State()
    all_tracker_deleted_notification = State()
