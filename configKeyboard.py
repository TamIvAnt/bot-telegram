import telebot
from telebot import types

keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('Привет', 'Регистрация', 'Начать игру', 'Пока')

keyboardStartGame = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardStartGame.row('Начать игру', 'Выход')

keyboardGame = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardGame.row('Атака', 'Оружие', 'Способности')
keyboardGame.row('Лавка', 'Баланс')
keyboardGame.row('Инвентарь', 'Выход')

keyboardInventory = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardInventory.row('Мои предметы', 'Мое оружие', 'Мои способности')

keyboardShop = types.InlineKeyboardMarkup()
#keyboardShop.row('Купить', 'Продать', 'Выход')

key_sell = types.InlineKeyboardButton(text = 'Продать', callback_data = 'sell')
key_buy = types.InlineKeyboardButton(text = 'Купить', callback_data = 'buy')
key_esc = types.InlineKeyboardButton(text = 'Выход', callback_data = 'esc')
keyboardShop.add(key_buy, key_sell, key_esc)

keyboardShopBuy = types.InlineKeyboardMarkup()
#keyboardShopBuy.row('Ржавый болт', 'Кость', 'Гнилое мясо')

buy_Item1 = types.InlineKeyboardButton(text = 'Ржавый болт', callback_data = 'rusty bolt')
buy_Item2 = types.InlineKeyboardButton(text = 'Кость', callback_data = 'bone')
buy_Item3 = types.InlineKeyboardButton(text = 'Гнилое мясо', callback_data = 'rotten meat')
keyboardShopBuy.add(buy_Item1, buy_Item2, buy_Item3)

keyboardAttack = types.InlineKeyboardMarkup()
key_gun = types.InlineKeyboardButton(text = 'Оружием', callback_data = 'gun')
key_skill = types.InlineKeyboardButton(text = 'Способностями', callback_data = 'skill')
keyboardAttack.add(key_gun, key_skill)

keyboardWeapon = types.InlineKeyboardMarkup()
keys_gun1 = types.InlineKeyboardButton(text = 'Старый пистолет', callback_data = 'pistol')
keys_gun2 = types.InlineKeyboardButton(text ='Лазер. винтовка', callback_data = 'rifle')
keys_gun3 = types.InlineKeyboardButton(text = 'Газовая ракета', callback_data = 'rocket')
keyboardWeapon.add(keys_gun1, keys_gun2, keys_gun3)

keyboardWeapon_Drop = types.InlineKeyboardMarkup()
keys_drop = types.InlineKeyboardButton(text='Выбросить', callback_data = 'drop')
keyboardWeapon.add(keys_drop)

keyboardEnemy = types.InlineKeyboardMarkup()
keys_enemy1 = types.InlineKeyboardButton(text = 'Скелет', callback_data = 'enemy_skeleton')
keys_enemy2 = types.InlineKeyboardButton(text = 'Мех. жук', callback_data = 'enemy_mechanical-beetle')
keys_enemy3 = types.InlineKeyboardButton(text = 'Бешенный пес', callback_data = 'enemy_mad-dog')
keyboardEnemy.add(keys_enemy1, keys_enemy2, keys_enemy3)

keyboardEnemy_Skills = types.InlineKeyboardMarkup()
keys_enemy1 = types.InlineKeyboardButton(text = 'Скелет', callback_data = 'skill_enemy_skeleton')
keys_enemy2 = types.InlineKeyboardButton(text = 'Мех. жук', callback_data = 'skill_enemy_mechanical-beetle')
keys_enemy3 = types.InlineKeyboardButton(text = 'Бешенный пес', callback_data = 'skill_enemy_mad-dog')
keyboardEnemy_Skills.add(keys_enemy1, keys_enemy2, keys_enemy3)

keyboardAnswer = types.InlineKeyboardMarkup()
key_yes = types.InlineKeyboardButton(text ='Да', callback_data='yes')
keyboardAnswer.add(key_yes)
key_no = types.InlineKeyboardButton(text ='Нет', callback_data='no')
keyboardAnswer.add(key_no)

keyboardSkill = types.InlineKeyboardMarkup()
key_fire = types.InlineKeyboardButton(text = 'Огненная струя', callback_data = 'fiery_stream')
key_water = types.InlineKeyboardButton(text = 'Водянной брызг', callback_data = 'water_spray')
key_clear = types.InlineKeyboardButton(text = 'Очистить', callback_data = 'clear')
keyboardSkill.add(key_fire, key_water, key_clear)

