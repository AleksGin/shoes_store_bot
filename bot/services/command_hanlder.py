import asyncio
import json
import logging
import os
import sys
from typing import Optional

import redis.asyncio as redis


class BotCommandHandler:
    def __init__(self, redis_client: redis.Redis) -> None:
        self.redis_client = redis_client
        self.pubsub = None
        self.listener_task: Optional[asyncio.Task] = None
        self._shutdown_event = asyncio.Event()

    async def start_listening(self) -> None:
        try:
            self.pubsub = self.redis_client.pubsub()
            await self.pubsub.subscribe("bot_commands")

            self.listener_task = asyncio.create_task(self._listen_for_commands())
            logging.info("Начато прослушивание команд через Redis pub/sub...")

        except Exception as e:
            logging.error(f"Ошибка при запуске прослушивания команд: {e}")

    async def _listen_for_commands(self):
        try:
            async for message in self.pubsub.listen():
                if message["type"] == "message":
                    try:
                        command_data = json.loads(message["data"])
                        await self._handle_command(command_data)
                    except json.JSONDecodeError:
                        logging.error("Ошибка декодирования команды")
                    except Exception as e:
                        logging.error(f"Ошибка обработки команды: {e}")

        except asyncio.CancelledError:
            logging.info("Прослушивание команд остановлено")
        except Exception as e:
            logging.error(f"Ошибка в цикле прослушивания: {e}")

    async def _handle_command(self, command_data: dict) -> None:
        command = command_data.get("command")
        admin_id = command_data.get("admin_id")

        logging.info(f"Получена команда: {command} от админа {admin_id}")

        if command == "restart":
            await self._handle_restart_command(admin_id)
        else:
            logging.warning(f"Неизвестная команда: {command}")

    async def _handle_restart_command(self, admin_id: int) -> None:
        try:
            logging.info(f"Обработка команды перезапуска от админа {admin_id}")

            await asyncio.sleep(1)
            
            await self.stop_listening()

            os._exit(0)

            self._shutdown_event.set()

            logging.info(
                "✅ Команда перезапуска инициирована - выполняется graceful shutdown"
            )

        except Exception:
            logging.error("Команда перезапуска инициирована - выполняется перезапуск")

    async def stop_listening(self):
        try:
            if self.listener_task and not self.listener_task.done():
                self.listener_task.cancel()
                try:
                    await self.listener_task
                except asyncio.CancelledError:
                    pass

            if self.pubsub:
                await self.pubsub.unsubscribe("bot_commands")
                await self.pubsub.close()

            logging.info("Прослушивание команд остановлено")

        except Exception as e:
            logging.error(f"Ошибка при остановке прослушивания: {e}")
