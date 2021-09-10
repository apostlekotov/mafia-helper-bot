import random
from aiogram.types import (
  InlineKeyboardButton, 
  InlineKeyboardMarkup, 
  ReplyKeyboardMarkup, 
  KeyboardButton
)
from data import msgs, roles

def create_btn(text, data):
  return InlineKeyboardButton(text, callback_data = data)

def create_key(text):
  return KeyboardButton(text)

def create_table():
  return InlineKeyboardMarkup().add(create_btn(msgs['create_table'], 'create_table'))

def create_define_players_markup(state):
  markup = InlineKeyboardMarkup()

  for role in roles:
    if roles[role]['default_quantity'] > 1:
      markup.row(
        create_btn('➖', f'{role}-decrease'),
        create_btn(f'{roles[role]["emoji"]} {state[role]}', 'empty'),
        create_btn('➕', f'{role}-increase')
      )
    else:
      markup.row(
        create_btn('❌', f'{role}-absent'),
        create_btn(f'{roles[role]["emoji"]} {state[role]}', 'empty'),
        create_btn('✅', f'{role}-participate')
      )

  markup.row(create_btn(f'Игроков {state["total_players"]}', 'empty'))

  return markup


def create_complete_kb():
  return ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True).add(
    create_key(msgs['complete'])
  )


def gen_role_list():
  role_list = 'За этим столом вы можете увидеть таких персонажей: \n'

  for role in roles.values():
    role_list += f'{role["emoji"]} {role["label"]} \n'

  return role_list


def get_initial_state():
  initial_state = {
    'total_players': 0
  }

  for role in roles:
    initial_state[role] = roles[role]['default_quantity']
    initial_state['total_players'] += roles[role]['default_quantity']

  return initial_state


def suffle_roles(state):
  role_list = []
  suffled_roles = ''

  for role in roles:
    if state[role] > 0:
      for _ in range(state[role]):
        role_list.append(roles[role])

  random.shuffle(role_list)

  for i, role in enumerate(role_list):
    suffled_roles += f'Игрок №{i + 1}: {role["emoji"]} {role["label"]} \n'

  return suffled_roles
