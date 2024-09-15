from aiogram.fsm.state import State, StatesGroup


class PriceCalculationStates(StatesGroup):
    waiting_for_amount = State()
    waiting_for_order_buttons = State()
