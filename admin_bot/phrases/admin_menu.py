class AdminMenu:
    change_rate: str = "💹Изменить курс"
    change_closest_date: str = "📆Изменить дату отправки"
    restart_bot: str = "🔄Перезапустить бота"
    statistics: str = "📊Статистика"
    control_admins: str = "👥Управление админами"
    back_to_admin_menu: str = "🏠На главную"
    admin_menu: str = "⚙️Админ-панель:"


class AdminManagementMenu:
    add_admin: str = "✅Добавить админа"
    delete_admin: str = "❌Удалить админа"
    admins_list: str = "📋Список админов"


class DefaultPhrases:
    welcome_text: str = "⚙️Администрирование и модерирование 🤖@crossw0rld_bot"
    permission_error: str = "🚫Отказано в доступе. У Вас нет доступа к данному боту."
    current_rate_in_cache: str = (
        "📍Курс в кроссике: {}\n\n"
        "<i>Допустимый формат: 10.1 / 10 / 10.0</i>\n\n"
        "📝Введите новый курс:"
    )
    current_date_in_cache: str = (
        "📍Дата в кроссике: {}\n\n"
        "<i>Допустимый формат: 20.12.2000</i>\n\n"
        "📝Введите новую дату:"
    )
    admin_ids: str = (
        "👥 Количество админов: {}\n\n"
        "📋 Админы:\n\n{}"
    )
    ask_for_input_admin_id: str = (
        "<i>ID пользователя состоит из 7-10 цифр</i>\n\n"
        "✏️Введите ID пользователя:"
    )
    empty_message_error: str = "❌Сообщение не содержит текста"
    save_into_cache_error: str = "❌Ошибка при сохранении курса"
    something_went_wrong: str = "❌Что-то пошло не так..."
    value_error: str = "❌Неверный формат. Допустимый формат: 10.1 / 10 / 10.0"
    date_value_error: str = "❌Неверный формат даты. Используйте формат: ДД.ММ.ГГГГ (например: 25.12.2000)"
    admin_value_error: str = "❌Неверный формат ID. ID должен состоять из цифр!"
    past_date_error: str = "❌Дата {} уже прошла! Укажите дату не раньше: {}"
    date_is_too_long: str = "❌Дата {} слишком далеко в будущем! Укажите дату в пределах года."
    save_into_cache_date_error: str = "❌Ошибка при сохранении даты"
    save_into_cache_admin_error: str = "❌Ошибка при сохранении админа"
    delete_from_cache_admin_error: str = "❌Ошибка при удалении админа"
    restart_bot_admin_error: str = "❌Произошла ошибка при перезапуске..."
    container_not_found_admin_error: str = "❌ Контейнер 'cros_bot' не найден"
    no_admin_notification: str = "👥 Админы не найдены"
    no_logs_notification: str = "🗑Тут пока ничего нет..."
    success_change_rate: str = "✅Курс успешно изменен"
    success_change_date: str = "✅Дата успешно изменена"
    success_add_admin: str = "✅Пользователь: {} успешно добавлен в админы"
    success_remove_admin: str = "✅Пользователь: {} успешно удален из админов"
    success_reload_bot: str = "✅Бот успешно перезапущен"
    action_name_rate: str = "💹Изменение курса"
    action_name_date: str = "📆Изменение даты отправки"
    action_name_add_admin: str = "➕👤Добавление админа"
    action_name_delete_admin: str = "➖👤Удаление админа"
    action_name_restart_bot: str = "🔄Перезапуск бота"
    
    
