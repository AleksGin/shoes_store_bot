import logging
from shared.shared_pharses import CacheKey
from shared.shared_repos import CacheRepo


async def setup_admins(cache_repo: CacheRepo, settings) -> list[int]:
    admin_ids = []

    if settings.admin_bot_config.initial_ids:
        try:
            admin_ids = [
                int(x.strip())
                for x in settings.admin_bot_config.initial_ids.split(",")
                if x.strip()
            ]
        except ValueError:
            logging.error("Ошибка в парсинге admin IDs")

    if settings.admin_bot_config.super_admin_id:
        try:
            super_admin_id = int(settings.admin_bot_config.super_admin_id)
            if super_admin_id not in admin_ids:
                admin_ids.append(super_admin_id)
        except ValueError:
            logging.error("Ошибка в парсинге super admin ID")

    for admin_id in admin_ids:
        try:
            await cache_repo.add_admin_id(CacheKey.ADMINS_KEY, admin_id)
            logging.info(f"Admin ID {admin_id} added to cache")
        except Exception as e:
            logging.error(f"Failed to add admin {admin_id}: {e}")

    return admin_ids


async def setup_yuan_rate(cache_repo, settings) -> None:
    try:
        current_rate = await cache_repo.get_yuan_rate(CacheKey.YUAN_RATE_KEY)
        if current_rate == 0:
            rate_from_env = settings.yuan_rate_config.yuan_rate
            await cache_repo.set_yuan_rate(CacheKey.YUAN_RATE_KEY, rate_from_env)
            logging.info(f"Yuan rate {rate_from_env} set from env")
        else:
            logging.info(f"Yuan rate already exists: {current_rate}")
    except Exception as e:
        logging.error(f"Error setting yuan rate: {e}")


async def setup_closest_date(cache_repo, settings) -> None:
    try:
        current_date = await cache_repo.get_closest_date(CacheKey.CLOSEST_DATE_KEY)
        if not current_date:
            date_from_env = settings.closest_date_config.date
            await cache_repo.set_closest_date(CacheKey.CLOSEST_DATE_KEY, date_from_env)
            logging.info(f"Closest date {date_from_env} set from env")
        else:
            logging.info(f"Closest date already exists: {current_date}")
    except Exception as e:
        logging.error(f"Error setting closest date: {e}")


async def setup_all(cache_repo, settings) -> list[int]:
    admin_ids = await setup_admins(
        cache_repo,
        settings,
    )
    await setup_yuan_rate(
        cache_repo,
        settings,
    )
    await setup_closest_date(
        cache_repo,
        settings,
    )
    return admin_ids
