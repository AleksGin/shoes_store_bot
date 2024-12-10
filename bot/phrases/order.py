from phrases import Misc


class Order:
    ask_for_order_text: str = "~               Оформим заказ?               ~"
    agree_order_text: str = "✅Да"
    not_agree_order_text: str = "❌Нет"
    calculate_again_text: str = "🔄Посчитать еще раз"
    ask_for_amount_text: str = "💴Введите сумму в ¥:"
    wrong_value_text: str = "<i>Введите целое число</i>"
    wrong_less_then_0_text: str = "<i>Число должно быть больше нуля</i>"
    wrong_waiting_for_order_buttons: str = "<i>Пожалуйста, воспользуйтесь кнопками под сообщением или вернитесь 🏠На главную</i>"
    wrong_waiting_for_tracker_button_: str = (
        "<i>Если необходимо удалить еще один трекер - воспользуйтесь кнопкой, </i>"
        "<i>либо вернитесь 🏠На главную</i>"
    )
    all_tracker_deleted_notification_text: str = (
        "<i>Все трекеры отключены!\n\n" "Вернитесь 🏠На главную</i>"
    )
    calculating_process_text: str = "<b>💬Считаю стоимость Вашего заказа...</b>"
    total_amount: str = (
        "✨Итоговая сумма: <b>{}₽</b>✨\n\n"
        "В стоимость входит:\n\n"
        f"🖇<b>Курс ¥</b> - {Misc.rate}₽\n\n"
        "🖇<b>Доставка</b> - {}₽\n\n"
        "🖇<b>Комиссия</b> - {}₽"
    )
    make_order_text: str = (
        "📌Для того, чтобы оформить заказ <u>необходима</u> следующая информация:\n\n"
        "📎ссылка на товар/скриншот товара\n\n"
        "📎размер\n\n"
        "📎цвет\n\n"
        "📎город получения заказа\n\n"
        "<b>Сделать заказ можно тут:</b>\n"
        ""  # LINK
    )
    ask_for_order_number_text: str = "🖋Введите номер, который Вам выдали при заказе:"
    order_number_status_text: str = "Статус для заказа {}: <b>{}</b>"
    wrong_order_number_text: str = (
        "Заказа с номером <b>{}</b> не существует, либо ему еще не присвоили статус...\n\n"
        "Пожалуйста, ожидайте 😊\n\n"
        "Также Вы можете посмотреть статус другого заказа:"
    )
    wrong_value_order_number_text: str = (
        "Неправильный номер заказа❗️\n\n"
        "(<i>Номер заказа состоит <u>исключительно</u> из целых чисел</i>)\n\n"
        "🖋Введите номер, который Вам выдали при заказе:"
    )
    wrong_value_order_number_for_delete: str = (
        "Неправильный номер заказа❗️\n\n"
        "(<i>Номер заказа состоит <u>исключительно</u> из целых чисел</i>)\n\n"
        "🖋Введите номер заказа, который хотите удалить"
    )
    search_order_text: str = "<b>🔎Ищу Ваш заказ...</b>"
    ask_for_view_new_order_text: str = "Хотите посмотреть статус другого заказа?"
    ask_for_track_text: str = "📍Отслеживать этот заказ"
    notification_about_status_order: str = (
        "💫Статус заказа <b>№{}</b> изменился на:<b>{}</b>💫"
    )
    order_tracked_text: str = (
        "📍Заказ с номером {} теперь отслеживается!\n\n"
        "<i>Когда статус заказа поменяется - Кроссик оповестит Вас!\n"
        "Отключить трекер можно в разделе</i> 📋Мои заказы"
    )
    already_tracking_text: str = "✅Данный заказ уже отслеживается"
    empty_tracking_list_text: str = "🥲Сейчас у Вас нет отслеживаемых заказов"
    count_tracking_orders = "<b>📃 Ваши отслеживаемые заказы:</b> {}\n\n"
    tracking_list_for_user: str = "📍<b>Заказ №{}</b> - статус: <b>{}</b>"
    tracking_list_error: str = "😢Не удалось получить данные о заказах"
    delete_a_specific_one_text: str = "🖌️Отключить трекер заказа(ов)"
    delete_a_specific_one_more_text: str = "🖌️Отключить еще один трекер"
    delete_all_tracking_orders_text: str = "❌Отключить все трекеры"
    text_about_tracking_orders: str = "<i>При удалении трекера бот больше не будет уведомлять Вас об изменениях статуса❗</i>"
    ask_for_order_number_to_delete: str = (
        "🖋Введите номер заказа, который хотите удалить:"
    )
    another_delivery_button_status_check_text: str = (
        "🤔Посмотреть статус другого заказа"
    )
    inline_button_status_check_text: str = "🤔Посмотреть статус заказа"
    specific_order_deleted_text: str = "✅Заказ №{} больше не отслеживается"
    all_orders_deleted_text: str = "✅Все трекеры отключены"
    delete_order_error: str = (
        "❌Данный заказ отсутствует в списке отслеживаемых!\n\n"
        "🖋Введите номер заказа, который хотите удалить:"
    )
