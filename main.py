
import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

import Ya_found_2
import Ya_found

logging.basicConfig(level=logging.INFO)
import config

logging.basicConfig(level=logging.INFO)

API_TOKEN = config.token
bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):
    regexp = State()  # Will be represented in storage as 'Form:name'
    type_collum = State()  # Will be represented in storage as 'Form:gender'


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.regexp.set()

    await message.reply("Hi there! What's your regexp?")


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.regexp)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['regexp'] = message.text

    await Form.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("phone_number", "first_name", "full_name", "email")
    markup.add("other")

    await message.reply("What type?", reply_markup=markup)
    markup = types.ReplyKeyboardRemove()
    #message.reply("Wait a minute. Try find this")
    #await message.reply("What type?")


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.regexp)
async def process_age(message: types.Message, state: FSMContext):
    # Update state and data
    await Form.next()
    await state.update_data(age=int(message.text))

    # Configure ReplyKeyboardMarkup



@dp.message_handler(lambda message: message.text not in ["phone_number", "first_name" ,"full_name", "email", "other"], state=Form.type_collum)
async def process_gender_invalid(message: types.Message):
    """
    In this example gender has to be one of: Male, Female, Other.
    """
    return await message.reply("Bad Choose")


@dp.message_handler(state=Form.type_collum)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['type_collum'] = message.text

        # Remove keyboard

        await bot.send_message(
            message.chat.id,
            md.text(md.text('Waiting...'), sep='\n'))

        output = Ya_found.find_name(data['regexp'], data['type_collum'])
        # And send message
        for outputs in output:
            await bot.send_message(
                message.chat.id,
                md.text(md.text(outputs), sep='\n'))

    # Finish conversation
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)