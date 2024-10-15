class CacheKey:
    USER_ID_KEY: str = "info for {} id"


class CacheTTL:
    hour: int = 3600
    day: int = 86400
    week: int = day * 7

