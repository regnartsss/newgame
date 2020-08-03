from loader import storage, bot
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
import aiogram.utils.exceptions


class DeleteMess(BaseMiddleware):
    """
    Simple middleware
    """
    def __init__(self):
        self.user_id = "message.from_user.id"
        super(DeleteMess, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
        This handler is called when dispatcher receives a message

        :param message:
        """
        self.user_id = message.from_user.id
        message_id = 0
        try:
            message_id = (await storage.get_data(chat=self.user_id))['message_id']
        except KeyError:
            pass
        try:
            await bot.delete_message(chat_id=self.user_id, message_id=message_id)
        except UnboundLocalError:
            pass
        except aiogram.utils.exceptions.MessageToDeleteNotFound:
            pass
        except Exception as n:
            print(f"Ошибка удаления {n}")
