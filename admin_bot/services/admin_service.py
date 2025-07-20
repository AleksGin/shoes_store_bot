import asyncio
from datetime import (
    date,
    datetime,
)
from pathlib import Path
from typing import List, Tuple

from admin_images import AdminBotImgs
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
)
from fsm import AdminManagementStates
from keyboards.inline import (
    admin_command_keyboard,
    admin_managemenet_menu,
)
from keyboards.reply import to_admin_menu_keyboard
from phrases import (
    AdminManagementMenu,
    AdminMenu,
    DefaultPhrases,
)

from services.message_service import MessageService
from shared.shared_pharses import CacheKey
from shared.shared_repos import CacheRepo


class AdminPanelService:
    def __init__(
        self,
        message_service: MessageService,
        cache_repo: CacheRepo,
    ) -> None:
        self._message_service = message_service
        self._cache = cache_repo

    async def welcome_text(self, message: Message) -> None:
        try:
            await self._message_service.send_message_with_image(
                mesage_text=AdminMenu.admin_menu,
                chat_id=message.chat.id,
                path=Path(AdminBotImgs.welcome_img),
                keyboard=admin_command_keyboard(),
            )
        except Exception:
            await self._message_service.send_simple_message(
                message_text=DefaultPhrases.something_went_wrong,
                chat_id=message.chat.id,
            )

    async def yuan_input_process(
        self,
        message: Message,
        state: FSMContext,
    ) -> None:
        try:
            if not message.text:
                await self._message_service.send_simple_message(
                    chat_id=message.chat.id,
                    message_text=DefaultPhrases.empty_message_error,
                )
                return

            new_rate = float(message.text.replace(",", "."))

            success = await self._cache.set_yuan_rate(
                CacheKey.YUAN_RATE_KEY,
                new_rate,
            )

            if success:
                await self._message_service.send_simple_message(
                    chat_id=message.chat.id,
                    message_text=DefaultPhrases.success_change_rate,
                )

                await asyncio.sleep(0.5)
            else:
                await self._message_service.send_simple_message(
                    message_text=DefaultPhrases.save_into_cache_error,
                    chat_id=message.chat.id,
                )

            await self._cache.add_admin_log(
                action=DefaultPhrases.action_name_rate,
                admin_id=message.from_user.id,  # type: ignore
                new_value=str(new_rate),
            )

            await state.clear()

        except ValueError:
            await self._message_service.send_simple_message(
                message_text=DefaultPhrases.value_error,
                chat_id=message.chat.id,
            )
        except Exception:
            await self._message_service.send_simple_message(
                chat_id=message.chat.id,
                message_text=DefaultPhrases.something_went_wrong,
            )
            await state.clear()

    async def change_date_action(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        try:
            await callback.message.edit_caption(  # type: ignore
                caption=AdminMenu.change_closest_date,
            )

            date_from_cache = await self._cache.get_closest_date(
                CacheKey.CLOSEST_DATE_KEY
            )

            await self._message_service.send_simple_message(
                chat_id=callback.from_user.id,
                message_text=DefaultPhrases.current_date_in_cache.format(
                    date_from_cache
                ),
                keyboard=to_admin_menu_keyboard(),
            )

            await state.set_state(AdminManagementStates.waiting_for_date_input)
        except Exception:
            await self._message_service.send_simple_message(
                message_text=DefaultPhrases.something_went_wrong,
                chat_id=callback.from_user.id,
            )
            await asyncio.sleep(0.5)
            await self.to_admin_menu(callback=callback)

    async def change_date_process(
        self,
        message: Message,
        state: FSMContext,
    ) -> None:
        try:
            if not message.text:
                await self._message_service.send_simple_message(
                    chat_id=message.chat.id,
                    message_text=DefaultPhrases.empty_message_error,
                )
                return

            new_date = message.text.strip()

            is_valid, error_message = self._validate_date_format(new_date)

            if not is_valid:
                await self._message_service.send_simple_message(
                    message_text=error_message,
                    chat_id=message.chat.id,
                )
                return
            success = await self._cache.set_closest_day(
                CacheKey.CLOSEST_DATE_KEY,
                new_date,
            )

            if success:
                await self._message_service.send_simple_message(
                    message_text=DefaultPhrases.success_change_date,
                    chat_id=message.chat.id,
                )
                await asyncio.sleep(0.5)
                await self.to_admin_menu(message=message)

                await self._cache.add_admin_log(
                    action=DefaultPhrases.action_name_date,
                    admin_id=message.from_user.id,  # type: ignore
                    new_value=new_date,
                )
            else:
                await self._message_service.send_simple_message(
                    message_text=DefaultPhrases.save_into_cache_date_error,
                    chat_id=message.chat.id,
                )

            await state.clear()

        except Exception:
            await self._message_service.send_simple_message(
                chat_id=message.chat.id,
                message_text=DefaultPhrases.something_went_wrong,
            )
            await state.clear()

    async def change_rate_action(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        await callback.message.edit_caption(  # type: ignore
            caption=AdminMenu.change_rate,
        )

        rate_from_cache = await self._cache.get_yuan_rate(CacheKey.YUAN_RATE_KEY)

        await self._message_service.send_simple_message(
            chat_id=callback.from_user.id,
            message_text=DefaultPhrases.current_rate_in_cache.format(rate_from_cache),
            keyboard=to_admin_menu_keyboard(),
        )

        await state.set_state(AdminManagementStates.waiting_for_rate_input)

    async def to_admin_menu(
        self,
        callback: CallbackQuery | None = None,
        message: Message | None = None,
    ) -> None:
        try:
            if callback:
                await callback.message.edit_caption(  # type: ignore
                    caption=AdminMenu.admin_menu,
                    reply_markup=admin_command_keyboard(),
                )
            else:
                await self._message_service.remove_keyboard(message.chat.id)  # type: ignore
                await self._message_service.send_message_with_image(
                    mesage_text=AdminMenu.admin_menu,
                    chat_id=message.chat.id,  # type: ignore
                    path=Path(AdminBotImgs.welcome_img),
                    keyboard=admin_command_keyboard(),
                )

        except Exception:
            chat_id = callback.from_user.id if callback else message.chat.id  # type: ignore
            await self._message_service.send_simple_message(
                message_text=AdminMenu.admin_menu,
                chat_id=chat_id,
                keyboard=admin_command_keyboard(),
            )

    async def open_admin_control(
        self,
        callback: CallbackQuery,
    ) -> None:
        try:
            await callback.message.edit_caption(  # type: ignore
                caption=AdminMenu.control_admins,
                reply_markup=admin_managemenet_menu(),
            )

        except Exception:
            await self._message_service.send_simple_message(
                message_text=AdminMenu.control_admins,
                chat_id=callback.from_user.id,
                keyboard=admin_managemenet_menu(),
            )

    async def get_admin_logs(self, callback: CallbackQuery):
        try:
            await callback.message.edit_caption(caption=AdminMenu.statistics)  # type: ignore

            logs = await self._cache.get_admin_logs(limit=5)

            if not logs:
                await self._message_service.send_simple_message(
                    message_text=DefaultPhrases.no_logs_notification,
                    chat_id=callback.from_user.id,
                )
                return

            formatted_logs = []
            for log_entry in logs:
                formatted_log = self._format_log_entry(log_entry)
                formatted_logs.append(formatted_log)

            stats_message = "📊 <b>Последние действия:</b>\n\n" + "\n\n".join(
                formatted_logs
            )

            await self._message_service.send_simple_message(
                message_text=stats_message,
                chat_id=callback.from_user.id,
                keyboard=to_admin_menu_keyboard(),
            )

        except Exception:
            await self._message_service.send_simple_message(
                message_text=DefaultPhrases.something_went_wrong,
                chat_id=callback.from_user.id,
            )

    async def restart_cros_bot_action(self, callback: CallbackQuery):
        try:
            await self._cache.add_admin_log(
                action=DefaultPhrases.action_name_restart_bot,
                admin_id=callback.from_user.id,
            )
            await callback.message.answer(text="🔄Отпрваляю команду на перезапуск...\n⏳ Ожидайте")  # type: ignore

            command_data = {
                "command": "restart",
                "admin_id": callback.from_user.id,
                "timestamp": datetime.now().isoformat(),
            }

            success = await self._cache.send_bot_command(command_data=command_data)

            result_message = self._status_formatter(success)

            await callback.message.edit_text(text=result_message)  # type: ignore

        except Exception as e:
            print(f"❌ Error restarting main bot: {e}")
            await self._message_service.send_simple_message(
                message_text=DefaultPhrases.restart_bot_admin_error,
                chat_id=callback.from_user.id,
            )

    async def add_admin_action(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        try:
            await callback.message.edit_caption(caption=AdminManagementMenu.add_admin)  # type: ignore

            await self._message_service.send_simple_message(
                chat_id=callback.from_user.id,
                message_text=DefaultPhrases.ask_for_input_admin_id,
                keyboard=to_admin_menu_keyboard(),
            )

            await state.set_state(AdminManagementStates.waiting_for_add_admin_id)
        except Exception:
            await self._message_service.send_simple_message(
                message_text=DefaultPhrases.something_went_wrong,
                chat_id=callback.from_user.id,
            )
            await self.to_admin_menu(callback=callback)

    async def add_admin_process(
        self,
        message: Message,
        state: FSMContext,
    ) -> None:
        try:
            if not message.text:
                await self._message_service.send_simple_message(
                    chat_id=message.chat.id,
                    message_text=DefaultPhrases.empty_message_error,
                )
                return

            admin_id = int(message.text)

            success = await self._cache.add_admin_id(
                key=CacheKey.ADMINS_KEY, user_id=admin_id
            )

            if success:
                await self._message_service.send_simple_message(
                    message_text=DefaultPhrases.success_add_admin.format(admin_id),
                    chat_id=message.chat.id,
                )
                await asyncio.sleep(0.5)
                await self.to_admin_menu(message=message)

                await self._cache.add_admin_log(
                    action=DefaultPhrases.action_name_add_admin,
                    admin_id=message.from_user.id,  # type: ignore
                    new_value=str(admin_id),
                )
            else:
                await self._message_service.send_simple_message(
                    message_text=DefaultPhrases.save_into_cache_admin_error,
                    chat_id=message.chat.id,
                )

            await state.clear()
        except ValueError:
            await self._message_service.send_simple_message(
                message_text=DefaultPhrases.admin_value_error,
                chat_id=message.chat.id,
            )

        except Exception:
            await self._message_service.send_simple_message(
                chat_id=message.chat.id,
                message_text=DefaultPhrases.something_went_wrong,
            )
            await state.clear()

    async def delete_admin_action(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        try:
            await callback.message.edit_caption(  # type: ignore
                caption=AdminManagementMenu.delete_admin,
            )

            await self._message_service.send_simple_message(
                chat_id=callback.from_user.id,
                message_text=DefaultPhrases.ask_for_input_admin_id,
                keyboard=to_admin_menu_keyboard(),
            )

            await state.set_state(AdminManagementStates.waiting_for_remove_admin_id)
        except Exception:
            await self._message_service.send_simple_message(
                message_text=DefaultPhrases.something_went_wrong,
                chat_id=callback.from_user.id,
            )
            await self.to_admin_menu(callback=callback)

    async def delete_admin_process(
        self,
        message: Message,
        state: FSMContext,
    ) -> None:
        try:
            if not message.text:
                await self._message_service.send_simple_message(
                    chat_id=message.chat.id,
                    message_text=DefaultPhrases.empty_message_error,
                )
                return

            admin_id = int(message.text)

            success = await self._cache.remove_admin_id(
                key=CacheKey.ADMINS_KEY,
                user_id=admin_id,
            )

            if success:
                await self._message_service.send_simple_message(
                    message_text=DefaultPhrases.success_remove_admin.format(admin_id),
                    chat_id=message.chat.id,
                )
                await asyncio.sleep(0.5)
                await self.to_admin_menu(message=message)

                await self._cache.add_admin_log(
                    action=DefaultPhrases.action_name_delete_admin,
                    admin_id=message.from_user.id,  # type: ignore
                    new_value=str(admin_id),
                )
            else:
                await self._message_service.send_simple_message(
                    message_text=DefaultPhrases.delete_from_cache_admin_error,
                    chat_id=message.chat.id,
                )

            await state.clear()
        except ValueError:
            await self._message_service.send_simple_message(
                message_text=DefaultPhrases.admin_value_error,
                chat_id=message.chat.id,
            )

        except Exception:
            await self._message_service.send_simple_message(
                chat_id=message.chat.id,
                message_text=DefaultPhrases.something_went_wrong,
            )
            await state.clear()

    async def get_admin_ids(self, callback: CallbackQuery) -> None:
        try:
            admin_ids = await self._cache.get_admin_ids(CacheKey.ADMINS_KEY)

            if not admin_ids:
                await self._message_service.send_simple_message(
                    chat_id=callback.from_user.id,
                    message_text=DefaultPhrases.no_admin_notification,
                )
            else:
                formatted_message = self._format_admin_ids(admin_ids=admin_ids)

            await callback.message.edit_caption(  # type: ignore
                caption=formatted_message,
                reply_markup=admin_managemenet_menu(show_list_button=False),
            )
        except Exception:
            await self._message_service.send_simple_message(
                chat_id=callback.from_user.id,
                message_text=DefaultPhrases.something_went_wrong,
            )
            await self.to_admin_menu(callback=callback)

    def _format_admin_ids(self, admin_ids: List[int]) -> str:
        numbered_list = "\n".join(
            f"{i}. ID: {admin_id}" for i, admin_id in enumerate(admin_ids, 1)
        )

        formatted_message = DefaultPhrases.admin_ids.format(
            len(admin_ids), numbered_list
        )

        return formatted_message

    def _format_log_entry(self, log_entry: dict) -> str:
        action = log_entry.get("action", "")
        timestamp = log_entry.get("timestamp", "")
        old_value = log_entry.get("old_value")
        new_value = log_entry.get("new_value")

        action_emojis = {
            "rate_change": "💹",
            "date_change": "📅",
            "bot_restart": "🔄",
            "admin_add": "👤➕",
            "admin_remove": "👤➖",
        }

        emoji = action_emojis.get(action, "⚙️")

        if action == "rate_change":
            if old_value and new_value:
                return (
                    f"{emoji} Курс изменен с {old_value}₽ на {new_value}₽ ({timestamp})"
                )
            elif new_value:
                return f"{emoji} Курс установлен на {new_value}₽ ({timestamp})"

        elif action == "date_change":
            if old_value and new_value:
                return (
                    f"{emoji} Дата изменена с {old_value} на {new_value} ({timestamp})"
                )
            elif new_value:
                return f"{emoji} Дата установлена на {new_value} ({timestamp})"

        elif action == "bot_restart":
            return f"{emoji} Перезапуск бота ({timestamp})"

        return f"{emoji} {action} ({timestamp})"

    def _status_formatter(self, send_status: bool) -> str:
        if send_status:
            result_message = (
                "✅ <b>Команда на перезапуск отправлена</b>\n\n"
                "📤 Основной бот получит команду\n"
                "⏳ Ожидайте выполнения (5-10 секунд)"
            )
        else:
            result_message = "⚠️ <b>При отправке команды что-то пошла не так...</b>"

        return result_message

    def _validate_date_format(self, date_str: str) -> Tuple[bool, str]:
        try:
            input_date = datetime.strptime(date_str, "%d.%m.%Y").date()
            current_date = date.today()

            if input_date < current_date:
                return False, DefaultPhrases.past_date_error.format(
                    date_str, current_date.strftime("%d.%m.%Y")
                )

            days_diff = (input_date - current_date).days

            if days_diff > 365:
                return False, DefaultPhrases.date_is_too_long.format(date_str)

            return True, ""

        except ValueError:
            return False, DefaultPhrases.date_value_error
