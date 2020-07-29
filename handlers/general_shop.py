from loader import dp, storage
from aiogram import types
from aiogram.dispatcher import FSMContext
from work.Shop import Form, shop_rename_heroes_win, shop_rename_heroes, moving_heroes_win, keyboard_shop
from text.texting import button_shop, text_shop


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    if message.text == "11":
        await message.answer("Отмена")
        await state.finish()
    else:
        await shop_rename_heroes_win(message)


@dp.message_handler(state=Form.coordinates)
async def process_name(message: types.Message, state: FSMContext):
    if message.text == "11":
        await message.answer("Отмена")
        await state.finish()
    else:
        if await moving_heroes_win(message) is True:
            await state.finish()


@dp.message_handler(text=button_shop)   # Магазин
async def shop(message: types.Message):
    user_id = message.from_user.id
    await storage.set_data(chat=user_id, data={"message_id": message.message_id+1})
    await message.answer(text=text_shop, reply_markup=keyboard_shop())


@dp.callback_query_handler(lambda call: call.data.split("_")[0] == 'shop')
async def handler(call: types.CallbackQuery):
    await shop(call=call)


@dp.callback_query_handler(text="shop_rename")
async def handler(call: types.CallbackQuery):
    await call.message.edit_text(text=await shop_rename_heroes(call))


