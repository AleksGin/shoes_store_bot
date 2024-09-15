from bot.menus.miscellaneous import Misc


class Order:
    ask_for_order_text = "~               Оформим заказ?               ~"
    agree_order_text = "✅Да"
    not_agree_order_text = "❌Нет"
    calculate_again_text = "🔄Посчитать еще раз"
    ask_for_amount_text = "💴Введите сумму в ¥:"
    wrong_value_text = "<i>Введите целое число</i>"
    wrong_less_then_0_text = "<i>Число должно быть больше нуля</i>"
    wrong_waiting_for_order_buttons = (
        "<i>Пожалуйста, воспользуйтесь кнопками под сообщением</i>"
    )
    calculating_process_text = "<b>💬Считаю стоимость Вашего заказа...</b>"
    total_amount = (
        "✨Итоговая сумма: <b>{}₽</b>✨\n\n"
        "В стоимость входит:\n\n"
        f"🖇<b>Курс ¥</b> - {Misc.rate}₽\n\n"
        "🖇<b>Доставка</b> - {}₽\n\n"
        "🖇<b>Комиссия</b> - {}₽"
    )
    make_order_text = (
        "📌Для того, чтобы оформить заказ <u>необходима</u> следующая информация:\n\n"
        "📎ссылка на товар/скриншот товара\n\n"
        "📎размер\n\n"
        "📎цвет\n\n"
        "📎город получения заказа\n\n"
        "<b>Сделать заказ можно тут:</b>\n"
        ""  # LINK
    )
    ask_for_order_number_text = "🖋Введите номер, который Вам выдали при заказе:"
    order_number_status_text = "Статус для заказа {}: <b>{}</b>"
    wrong_order_number_text = (
        "Заказа с номером <b>{}</b> не существует, либо ему еще не присвоили статус...\n\n"
        "Пожалуйста, ожидайте 😊\n\n"
        "Также Вы можете посмотреть статус другого заказа:"
    )
    wrong_value_order_number_text = (
        "Неправильный номер заказа❗️\n\n"
        "(<i>Номер заказа состоит <u>исключительно</u> из целых чисел</i>)\n\n"
        "🖋Введите номер, который Вам выдали при заказе:"
    )
    search_order_text = "<b>🔎Ищу Ваш заказ...</b>"
    ask_for_view_new_order_text = "Хотите посмотреть статус другого заказа?"
