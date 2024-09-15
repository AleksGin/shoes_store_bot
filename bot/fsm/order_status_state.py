from aiogram.fsm.state import State, StatesGroup


class OrderStatusState(StatesGroup):
    waiting_order_number = State()
    waiting_for_view_new_order_button = State()
