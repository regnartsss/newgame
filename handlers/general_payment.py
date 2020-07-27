from aiogram import types
from aiogram.types.message import ContentTypes
from loader import bot, dp
from keyboards.keyboard import keyboard_main_menu
# from work.Buy import succefull_tranzzo


@dp.shipping_query_handler(lambda query: True)
async def shipping(shipping_query: types.ShippingQuery):
    print("test1")
    await bot.answer_shipping_query(shipping_query.id, ok=True,
                                    # shipping_options=shipping_options,
                                    error_message='Попробуйте немного позднее')


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    print("test2")
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Aliens tried to steal your card's CVV,"
                                                      " but we successfully protected your credentials,"
                                                      " try to pay again in a few minutes, we need a small rest.")


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    await message.answer('Ура! Спасибо за оплату! Мы выполним ваш заказ на сумму `{} {}` как можно быстрее! '
                         'Оставайтесь на связи. '.format(message.successful_payment.total_amount / 100,
                                                         message.successful_payment.currency),
                         parse_mode='Markdown', reply_markup=keyboard_main_menu())
    # await succefull_tranzzo(message)
