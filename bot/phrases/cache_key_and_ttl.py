class CacheKey:
    USER_ID_KEY: str = "user:{}:order:{}"
    TRACKING_USER_ID_KEY: str = "tracking_user:{}:order:{}"
    match_for_key: str = USER_ID_KEY.format("*", "*")
    match_tracking_key: str = TRACKING_USER_ID_KEY.format("*", "*")


class CacheTTL:
    hour: int = 3600
    day: int = 86400
    week: int = day * 7
    


