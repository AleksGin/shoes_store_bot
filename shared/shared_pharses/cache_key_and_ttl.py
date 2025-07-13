class CacheKey:
    ORDER_STATUS_KEY: str = "order:{}"
    TRACKING_USER_ID_KEY: str = "tracking_user:{}:order:{}"
    ADMINS_KEY: str = "system:admins"
    YUAN_RATE_KEY: str = "system:yuan_rate"
    CLOSEST_DATE_KEY: str = "system:date"
    match_for_key: str = ORDER_STATUS_KEY.format("*")
    match_tracking_key: str = TRACKING_USER_ID_KEY.format("*", "*")
    match_for_user_to_orders: str = "tracking_user:{}:order:*"
    match_for_order_to_users: str = "tracking_user:*order:{}"


class CacheTTL:
    hour: int = 3600
    day: int = 86400
    week: int = day * 7
    month: int = week * 4
    

class CacheErrors:
    uncorrect_value: str = "Некорректное значение"
    data_is_not_set: str = "В данный момент дата не установлена"
    data_is_empty: str = "Дата не может быть пустой"
    wrong_type: str = "Дата должна быть строкой"
    


