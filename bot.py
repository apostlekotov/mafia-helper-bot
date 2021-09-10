import os
import logging
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, ContentType, CallbackQuery

from data import msgs
from utils import (
  create_complete_kb,
  create_define_players_markup,
  create_table,
  get_initial_state,
  gen_role_list,
  suffle_roles
)

logging.basicConfig(level = logging.INFO)

# Config
load_dotenv()

TOKEN = os.getenv('TOKEN')

# Bot
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

global_state = {}

# Actions
@dp.message_handler(commands = ['start'])
async def start(msg: Message):
  await msg.answer(msgs['start'], reply_markup = create_table())

@dp.message_handler(lambda message: message.text == msgs['complete'])
async def distribute_roles(msg: Message):
  await msg.reply(suffle_roles(global_state[msg.chat.id]))
  await msg.answer(msgs['game_is_on'])

@dp.message_handler(content_types = ContentType.ANY)
async def default_reply(msg: Message):
  await msg.answer(msgs['default_reply'])


async def define_players(msg: Message, state):
  cid = msg.chat.id
  global_state[cid] = state

  await msg.answer(gen_role_list(), reply_markup = create_define_players_markup(global_state[cid]))
  await msg.answer(msgs['is_ready'], reply_markup = create_complete_kb())


# Handlers
@dp.callback_query_handler()
async def btn_handler(query: CallbackQuery):
  cid = query.message.chat.id

  if 'create_table' in query.data:
    await define_players(query.message, get_initial_state())
    await query.message.edit_reply_markup()  # clear btn
    await query.answer('Стол создан')

  elif 'increase' in query.data:
    if global_state[cid][query.data.split('-')[0]] > 9:
      await query.answer('Максимальное к-ство игроков этой роли - 10')
      return

    global_state[cid][query.data.split('-')[0]] += 1
    global_state[cid]['total_players'] += 1

    await query.message.edit_reply_markup(create_define_players_markup(global_state[cid]))
    await query.answer('')

  elif 'decrease' in query.data:
    if global_state[cid][query.data.split('-')[0]] == 2:
      await query.answer('Минимальное к-ство игроков этой роли - 2')
      return

    global_state[cid][query.data.split('-')[0]] -= 1
    global_state[cid]['total_players'] -= 1

    await query.message.edit_reply_markup(create_define_players_markup(global_state[cid]))
    await query.answer('')

  elif 'participate' in query.data:
    if global_state[cid][query.data.split('-')[0]] == 1:
      await query.answer('')
      return

    global_state[cid][query.data.split('-')[0]] = 1
    global_state[cid]['total_players'] += 1

    await query.message.edit_reply_markup(create_define_players_markup(global_state[cid]))
    await query.answer('')

  elif 'absent' in query.data:
    if global_state[cid][query.data.split('-')[0]] == 0:
      await query.answer('')
      return

    global_state[cid][query.data.split('-')[0]] = 0
    global_state[cid]['total_players'] -= 1

    await query.message.edit_reply_markup(create_define_players_markup(global_state[cid]))
    await query.answer('')

  elif 'empty' in query.data:
    await query.answer('')

  else:
    await bot.send_message(cid, msgs['error'])


if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)
