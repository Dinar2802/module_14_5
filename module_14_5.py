from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import crud_functions
from crud_functions import *



api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
ikb = InlineKeyboardMarkup(resize_keyboard=True)
ikb2 = InlineKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать')
button3 = KeyboardButton(text='Купить')
button4 = KeyboardButton(text='Регистрация')
ibutton3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
ibutton4 = InlineKeyboardButton(text='Формула расчёта', callback_data='formulas')
ibutton5 = InlineKeyboardButton(text='Продукт 1', callback_data='product_buying')
ibutton6 = InlineKeyboardButton(text='Продукт 2', callback_data='product_buying')
ibutton7 = InlineKeyboardButton(text='Продукт 3', callback_data='product_buying')
ibutton8 = InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
kb.add(button1)
kb.add(button2)
kb.add(button3)
kb.add(button4)
ikb.add(ibutton3)
ikb.add(ibutton4)
ikb2.add(ibutton5)
ikb2.add(ibutton6)
ikb2.add(ibutton7)
ikb2.add(ibutton8)

get_all_products()
# add_user()
# is_included()


@dp.message_handler(text=['Информация'])
async def Start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью. Нажмите Рассчитать для подсчёта нормы калорий')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    await state.update_data(balance=1000)
    data = await state.get_data()
    crud_functions.add_user(data['username'], data['email'], data['age'])
    await message.answer("Регистрация прошла успешно.", reply_markup=kb)
    await state.finish()

@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=ikb)


@dp.callback_query_handler(text=['formulas'])
async def get_formulas(call):
    await call.message.answer('для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')


@dp.callback_query_handler(text=['calories'])
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    norma = int(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 161)
    await message.answer(f"Ваша норма в сутки {norma} ккал")
    await state.finish()


@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    for i in get_all_products():
        number = i[0]
        title = i[1]
        description = i[2]
        price = i[3]
        with open (f'{str(number) + ".jpeg"}', 'rb') as img:
            await message.answer_photo(img, caption=f'Название: {title} | Описание: {description} | Цена: {price}')
    await message.answer("Выберите продукт:", reply_markup=ikb2)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()



@dp.message_handler()
async def all_message(message):
    await message.answer('Выберите необходимый пунк меню', reply_markup=kb)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)