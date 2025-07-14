class AdminMenu:
    change_rate: str = "💹Изменить курс"
    change_closest_date: str = "📆Изменить дату отправки"
    restart_bot: str = "🔄Перезапустить бота"
    statistics: str = "📊Статистика"
    control_admins: str = "👥Управление админами"
    back_to_admin_menu: str = "🏠На главную"
    admin_menu: str = "⚙️Админ-панель:"
    
    
class AdminManagementMenu: 
    add_admin: str = "🟢Добавить админа"
    delete_admin: str = "🔴Удалить админа"
    admins_list: str = "📋Список админов"
    
    
    
class DefaultPhrases:
    welcome_text: str = "⚙️Администрирование и модерирование 🤖@crossw0rld_bot"
    permission_error: str = "🚫Отказано в доступе. У Вас нет доступа к данному боту."
    current_rate_in_cache: str = "Курс в кроссике на данный момент: {}"
    set_new_rate: str = (
        "Введите новый курс:\n\n"
        "<i>Вводить нужно в формате: 10.1 / 10 / 10.0"
    )
    
