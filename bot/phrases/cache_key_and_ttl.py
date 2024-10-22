class CacheKey:
    USER_ID_KEY: str = "user_id_{}_order_id_{}_info:"


class CacheTTL:
    hour: int = 3600
    day: int = 86400
    week: int = day * 7
