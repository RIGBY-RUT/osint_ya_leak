import json
import logging
import time
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.dispatcher import filters
import re
from datetime import datetime

#import Ya_found_2
#import Ya_found
import Ya_DB_finder
import BD_emulator

logging.basicConfig(level=logging.INFO)
import config

logging.basicConfig(level=logging.INFO)
test=0
PHONE_REGEXP = '^([+]?[0-9\s-\(\)]{3,25})*$'
pattern_email = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"


API_TOKEN = config.token
bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


list_db = ["first_name", "full_name", "email","phone_number", "address_city", "address_street", "address_house", "address_entrance", "address_floor", "address_office", "address_comment"]
str_db  = "first_name", "full_name", "email","phone_number", "address_city", "address_street", "address_house", "address_entrance", "address_floor", "address_office", "address_comment"





# States
class Form(StatesGroup):
    regexp = State()  # Will be represented in storage as 'Form:name'
    type_collum = State()  # Will be represented in storage as 'Form:gender'




#Обработка ошибки флуда
# @dp.errors_handler(exception=exceptions.RetryAfter)
# async def exception_handler(update: types.Update, exception: exceptions.RetryAfter):
    # await state.finish()
    
    # return True
    




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
    nums=0
    while nums < len(list_db):
    
        try:
           markup.add(list_db[nums], list_db[nums+1],list_db[nums+2])
        except:
            markup.add(list_db[nums], list_db[nums+1])
         
        nums+=3
    markup.add("other")

    await message.reply("What type?", reply_markup=markup)
    markup = types.ReplyKeyboardRemove()
    #await message.reply("", reply_markup=markup)
    #message.reply("Wait a minute. Try find this")
    #await message.reply("What type?")


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.regexp)
async def process_age(message: types.Message, state: FSMContext):
    # Update state and data
    await Form.next()
    await state.update_data(age=int(message.text))

    # Configure ReplyKeyboardMarkup



@dp.message_handler(lambda message: message.text not in list_db, state=Form.type_collum)
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
        await message.reply('Waiting...', reply_markup=types.ReplyKeyboardRemove())
        #await bot.send_message(
            #message.chat.id,
            #md.text(md.text('Waiting...'), sep='\n'))
        #markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        #markup = types.ReplyKeyboardRemove()
        #output = Ya_found.find_name(data['regexp'], data['type_collum'])
        if test == 0:
            output = json.loads(Ya_DB_finder.finding(data['regexp'], data['type_collum']))
        else:
            output = json.loads(BD_emulator.finding(data['regexp'], data['type_collum']))
        # And send message
        if len(output) != 0:
            pause = 1
            if len(output) > 60:
                pause = 5
                output = output[:60]
                md.text(md.text('This is a part of outpu (ferst 40 items)'), sep='\n')
            for person in output:
                #print('='*20)
                #print(person)
                iformation = ""
                for key, values in person.items():
                    if key != '_id':
                        iformation = str(iformation + '*' + str(key)  + '*' +  ': ' + '`' +str(values) + '`' + '\n')
                        #iformation = ( iformation,
                        #    hcode(str(key)), '--',
                        #    code(str(values)))
            
                await bot.send_message(
                    message.chat.id,
                    (iformation), parse_mode = 'Markdown')
                try:
                    await bot.send_location(
                    message.chat.id,
                    person['location_latitude'], person['location_longitude'])
                except:
                    await bot.send_message(
                    message.chat.id,
                    md.text(md.text('No location data'), sep='\n'))
                time.sleep(pause)
                
        else:
            await bot.send_message(
                    message.chat.id,
                    md.text(md.text("Nothing"), sep='\n'))


    # Finish conversation
    await state.finish()




@dp.message_handler(lambda message: message.text not in list_db)
async def check_phone(message: types.Message):
    input_text = message.text
    output = 0
    if input_text[1:].isdigit():
        input_text = (re.sub("[^0-9]", "", message.text))
        if input_text[0] == '8':
            input_text = '7'+ input_text[1:]
        await message.reply('Waiting... Try find this number', reply_markup=types.ReplyKeyboardRemove())
        output = json.loads(Ya_DB_finder.finding_phone(input_text))

    elif re.match(pattern_email, input_text) is not None:
        await message.reply('Waiting... Try find this email', reply_markup=types.ReplyKeyboardRemove())
        output = json.loads(Ya_DB_finder.finding(input_text, 'email'))
               
    else:
        await message.reply('Waiting... Try find this name', reply_markup=types.ReplyKeyboardRemove())
        output = json.loads(Ya_DB_finder.finding(input_text, 'full_name'))
    if len(output) != 0:
        for person in output:
            iformation = ""
        if len(output) != 0:
            for person in output:
                print('='*20)
                print(person)
                iformation = ""
                for key, values in person.items():
                    if key != '_id':
                        iformation = str(iformation + '*' + str(key)  + '*' +  ': ' + '`' +str(values) + '`' + '\n')
                        #iformation = ( iformation,
                        #    hcode(str(key)), '--',
                        #    code(str(values)))
            
                await bot.send_message(
                    message.chat.id,
                    (iformation), parse_mode = 'Markdown')
                try:
                    await bot.send_location(
                    message.chat.id,
                    person['location_latitude'], person['location_longitude'])
                except:
                    await bot.send_message(
                    message.chat.id,
                    md.text(md.text('No location data'), sep='\n'))
                time.sleep(1)
                
    else:
        await bot.send_message(
                message.chat.id,
                md.text(md.text("Nothing"), sep='\n'))


    # Finish conversation
#    await state.finish()








if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)