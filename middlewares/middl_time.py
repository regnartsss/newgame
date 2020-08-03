from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from datetime import datetime


def time_start(mess=True):
    def decorator(time):
        setattr(time, 'time', mess)
        return time
    return decorator


class TimeTower(BaseMiddleware):
    """
    Simple middleware
    """
    def __init__(self, mess=False):
        self.mess = mess
        self.user_id = "message.from_user.id"
        super(TimeTower, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        mess = getattr(handler, 'time', self.mess)
        if mess is True:
            time = datetime.utcnow()
            utctime = time.strftime("%H:%M")
            if "14:00" <= utctime <= "14:20":
                await message.answer("Идёт бой, ожидайте")
                raise CancelHandler()
