import configValue
import configItems
import configKeyboard

import sqlite3

import telebot
import time
import random


bot = telebot.TeleBot('APIKey')

print('Запуск произведен!')
#----------------------------------------------------------------------------------


conn = sqlite3.connect('orders.db')
#print("Connection to SQLite DB successful")

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
   userid INT PRIMARY KEY,
   fname TEXT,
   lname TEXT,
   LvL INT
   );
""")
conn.commit()
conn.close()


inventory = sqlite3.connect('orders.db')
cursor = inventory.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS inventory(
   userid INT PRIMARY KEY,
   weapon TEXT,
   skill TEXT,
   user_money INT,
   item TEXT
   );
""")
inventory.commit()
inventory.close()


def reg_inventory_db(message):
    inventory = sqlite3.connect('orders.db')
    cursor = inventory.cursor()

    cursor.execute("""SELECT userid FROM inventory""")
    req = cursor.fetchone()
    res = 0

    if req == None:
        res = 0
    else:
        #res = int(''.join(map(str, req)))
        pass

    if res != message.from_user.id:
        cursor.execute(u"""INSERT INTO inventory(userid, weapon, skill, user_money, item) VALUES(?, ?, ?, ?, ?);""",
                    [message.from_user.id, None, None, None, None])

    else:
        print(1)

    inventory.commit()
    inventory.close()



def reg_db(message):
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()

    cur.execute("""SELECT userid FROM users""")
    req = cur.fetchone()
    if req == None:
        res = ''
    else:
        res = req[0]

    cur.execute("""SELECT fname FROM users""")
    fname = cur.fetchone()
    if fname == None:
        fname_req = ''
    else:
        fname_req = fname[0]

    cur.execute("""SELECT lname FROM users""")
    lname = cur.fetchone()
    if lname == None:
        lname_req = ''
    else:
        lname_req = lname[0]

    #print(res)
    #print(message.from_user.id)

    if res == message.from_user.id:
        bot.send_message(message.from_user.id, fname_req + ' ' + lname_req + ' ' + 'это Вы?',
                                            reply_markup = configKeyboard.keyboardAnswer)
    else:
        cur.execute(u"""INSERT INTO users(userid, fname, lname) VALUES(?, ?, ?);""",
                    [message.from_user.id, configValue.name, configValue.surname])

    conn.commit()
    conn.close()

    reg_inventory_db(message)

    bot.send_message(message.from_user.id, 'Зарегистрировал вас',
                            reply_markup=configKeyboard.keyboard)




def chek_db(message):
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()

    cur.execute("""SELECT userid FROM users WHERE userid = {}""".format(message.from_user.id))
    res = cur.fetchone()


    if res == None:
        bot.send_message(message.chat.id, 'Давай проведем регистрацию.')
        bot.send_message(message.chat.id, 'Твое имя?')
        bot.register_next_step_handler(message, get_name)
    else:
        configValue.STATUSAnswer = True
        bot.send_message(message.from_user.id, 'Вы зарегистрированны!',
                         reply_markup=configKeyboard.keyboardStartGame)


    conn.close()


def money_db(call):
    inventory = sqlite3.connect('orders.db')
    cursor = inventory.cursor()

    cursor.execute("""SELECT userid FROM inventory WHERE userid = {}""".format(call.message.chat.id))
    r = cursor.fetchone()

    if r == None:
        cursor.execute(u"""INSERT INTO inventory(userid) VALUES(?);""",
                                                [call.message.chat.id])
    else:
        pass

    cursor.execute("""SELECT user_money FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

    res = cursor.fetchone()

    if res == None:
        req = 0
        req = int(''.join(map(str, res)))
    else:
        req = int(''.join(map(str, res)))

    MONEY = req + configValue.user_money

    cursor.execute("""UPDATE inventory 
                    SET user_money = {}
                    WHERE userid = {}""".format(MONEY, call.message.chat.id))

    #cursor.execute("""SELECT * FROM inventory""")
    #req = cursor.fetchone()
    #print(req)

    cursor.execute("""SELECT user_money FROM inventory  WHERE userid = {}""".format(call.message.chat.id))
    res = cursor.fetchone()
    req = int(''.join(map(str, res)))

    bot.send_message(call.message.chat.id, 'Выпали монеты. Ваш баланс: ' + str(req),
                     reply_markup=configKeyboard.keyboardGame)

    inventory.commit()
    inventory.close()


def weapon_db(call, weapon=None):
    #print(weapon)

    inventory = sqlite3.connect('orders.db')
    cursor = inventory.cursor()

    #cursor.execute("""SELECT weapon FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

    #r = cursor.fetchone()
    #rs = ", ".join(r)
    #print(rs)

    cursor.execute("""UPDATE inventory 
                    SET weapon = ?
                    WHERE userid = ?""", (weapon, call.message.chat.id))


    inventory.commit()
    inventory.close()


def chek_weapon_db(call):
    inventory = sqlite3.connect('orders.db')
    cursor = inventory.cursor()

    cursor.execute("""SELECT weapon FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

    r = cursor.fetchone()
    rs = ", ".join(r)
    #print(rs)

    if len(rs) > 2:
        if call.data == "drop":
            bot.send_message(call.message.chat.id, 'Все оружие выброшенно ', reply_markup=configKeyboard.keyboardGame)
            weapon = ''

            cursor.execute("""UPDATE inventory 
                                SET weapon = ?
                                WHERE userid = ?""", (weapon, call.message.chat.id))


    elif len(rs) > 2:
        bot.send_message(call.message.chat.id, 'Место под оружие занято( ', reply_markup=configKeyboard.keyboardWeapon_Drop)

    inventory.commit()
    inventory.close()


def skill_db(call, skill):
    #print(skill)

    inventory = sqlite3.connect('orders.db')
    cursor = inventory.cursor()

    # cursor.execute("""SELECT weapon FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

    # r = cursor.fetchone()
    # rs = ", ".join(r)
    # print(rs)

    cursor.execute("""UPDATE inventory 
                        SET skill = ?
                        WHERE userid = ?""", (skill, call.message.chat.id))

    inventory.commit()
    inventory.close()


def sell_db(call, money):

    inventory = sqlite3.connect('orders.db')
    cursor = inventory.cursor()

    cursor.execute("""SELECT user_money FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

    r = cursor.fetchone()
    rs = r[0]

    if rs == None or rs == 0:
        rs = 0

    added = rs + money
    cursor.execute("""UPDATE inventory 
                         SET user_money = ?
                         WHERE userid = ?""", (added, call.message.chat.id))

    item = ''
    cursor.execute("""UPDATE inventory 
                         SET item = ?
                         WHERE userid = ?""", (item, call.message.chat.id))

    cursor.execute("""SELECT user_money FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

    r = cursor.fetchone()
    re = r[0]

    inventory.commit()
    inventory.close()

    bot.send_message(call.message.chat.id, 'Предметы проданны!', reply_markup=configKeyboard.keyboardGame)
    bot.send_message(call.message.chat.id, 'Ваш баланс: ' + str(re), reply_markup=configKeyboard.keyboardGame)


def attack_db(call):

    inventory = sqlite3.connect('orders.db')
    cursor = inventory.cursor()


    randoms = random.randint(1, 3)
    if randoms == 1:
        #configValue.item = configItems.item_1
        cursor.execute("""UPDATE inventory 
                            SET item = ?
                            WHERE userid = ?""", (configItems.item_1, call.message.chat.id))

    elif randoms == 2:
        #configValue.item = configItems.item_2
        cursor.execute("""UPDATE inventory 
                             SET item = ?
                             WHERE userid = ?""", (configItems.item_2, call.message.chat.id))

    elif randoms == 3:
        #configValue.item = configItems.item_3
        cursor.execute("""UPDATE inventory 
                            SET item = ?
                            WHERE userid = ?""", (configItems.item_3, call.message.chat.id))


    inventory.commit()
    inventory.close()

def check_atack_db(call):
    inventory = sqlite3.connect('orders.db')
    cursor = inventory.cursor()

    cursor.execute("""SELECT item FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

    r = cursor.fetchone()
    rs = r[0]

    inventory.close()

    bot.send_message(call.message.chat.id, 'Враг убит!) С него выпал предмет: ' + rs,
                     reply_markup=configKeyboard.keyboardGame)


def shop_buy(call):
    bot.send_message(call.message.chat.id, 'Вот, что есть у меня в лавке:  ',
                     reply_markup=configKeyboard.keyboardShopBuy)

def shop_sell(call):
    inventory = sqlite3.connect('orders.db')
    cursor = inventory.cursor()

    cursor.execute("""SELECT item FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

    r = cursor.fetchone()
    rs = r[0]
    #print(rs)

    inventory.close()

    if rs == configItems.item_1:
        sell_db(call, 15)

    elif rs == configItems.item_2:
        sell_db(call, 25)

    elif rs == configItems.item_3:
        sell_db(call, 45)

    else:
        bot.send_message(call.message.chat.id, 'Нечего продать!(', reply_markup=configKeyboard.keyboardGame)



def LvL_bd(call):
    inventory = sqlite3.connect('orders.db')
    cursor = inventory.cursor()

    cursor.execute("""SELECT LvL FROM users  WHERE userid = {}""".format(call.message.chat.id))
    cL = cursor.fetchone()
    C = cL[0]
    #print(C)


    if C == None:
        C = 0
        cursor.execute("""UPDATE users 
                                    SET LvL = ?
                                    WHERE userid = ?""", (C, call.message.chat.id))
        cursor.execute("""SELECT LvL FROM users  WHERE userid = {}""".format(call.message.chat.id))
        c = cursor.fetchone()
        Cs = c[0]

    else:
        pass

    cursor.execute("""SELECT EXP FROM users  WHERE userid = {}""".format(call.message.chat.id))
    cE = cursor.fetchone()
    CE = cE[0]
    #print(CE)

    if CE == None:
        CE = 0
        cursor.execute("""UPDATE users 
                                        SET EXP = ?
                                        WHERE userid = ?""", (CE, call.message.chat.id))
        cursor.execute("""SELECT LvL FROM users  WHERE userid = {}""".format(call.message.chat.id))
        c = cursor.fetchone()
        Cs = c[0]
        #print(Cs)

    else:
        pass

    inventory.commit()
    inventory.close()


def check_EXP_db(call):
    inventory = sqlite3.connect('orders.db')
    cursor = inventory.cursor()

    cursor.execute("""SELECT EXP FROM users  WHERE userid = {}""".format(call.message.chat.id))
    cE = cursor.fetchone()
    exp = cE[0]

    cursor.execute("""SELECT LvL FROM users  WHERE userid = {}""".format(call.message.chat.id))
    cL = cursor.fetchone()
    LVL = cL[0]

    if LVL == 3 and LVL != 4:
        if exp >= configValue.lvl_4:
            bot.send_message(call.message.chat.id, "Поздравляю с достижением 4-его уровня",
                             reply_markup=configKeyboard.keyboardGame)
            check_LvL(call, 4)

    elif LVL == 4:
        pass

    elif LVL == 2 and LVL != 3:
        if exp >= configValue.lvl_3:
            bot.send_message(call.message.chat.id, "Поздравляю с достижением 3-его уровня",
                             reply_markup=configKeyboard.keyboardGame)
            check_LvL(call, 3)

    elif LVL == 3:
        pass

    elif LVL == 1 and LVL != 2:
        if exp >= configValue.lvl_2:
            bot.send_message(call.message.chat.id, "Поздравляю с достижением 2-го уровня",
                             reply_markup=configKeyboard.keyboardGame)
            check_LvL(call, 2)

    elif LVL == 2:
        pass

    elif LVL == 0 and LVL != 1:
        if exp >= configValue.lvl_1:
            bot.send_message(call.message.chat.id, "Поздравляю с достижением 1-его уровня",
                            reply_markup=configKeyboard.keyboardGame)
            check_LvL(call, 1)

    elif LVL == 1:
        pass

    else:
        print('error')


    inventory.close()



def new_LvL_db(call, exp):
    #print(exp)

    inventory = sqlite3.connect('orders.db')
    cursor = inventory.cursor()

    cursor.execute("""SELECT EXP FROM users  WHERE userid = {}""".format(call.message.chat.id))
    cE = cursor.fetchone()
    E = cE[0]
    new_exp = 0

    if E != None:
        new_exp = E + exp
    else:
        check_EXP_db(call)

    cursor.execute("""UPDATE users 
                           SET EXP = ?
                           WHERE userid = ?""", (new_exp, call.message.chat.id))

    cursor.execute("""SELECT EXP FROM users  WHERE userid = {}""".format(call.message.chat.id))
    CE = cursor.fetchone()
    Ep = CE[0]
    print(Ep)


    inventory.commit()
    inventory.close()



def check_LvL(call, lvl):
    print(lvl)

    inventory = sqlite3.connect('orders.db')
    cursor = inventory.cursor()

    cL = lvl
    cursor.execute("""UPDATE users 
                               SET LvL = ?
                               WHERE userid = ?""", (cL, call.message.chat.id))
    cursor.execute("""SELECT LvL FROM users  WHERE userid = {}""".format(call.message.chat.id))
    c = cursor.fetchone()
    Cs = c[0]
    print(Cs)

    inventory.commit()
    inventory.close()




@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, это бета тест игрового бота от молодого программиста *TamIvAnt*.'
                                      ' Так как игра в стадии разработки могут быть баги, если нашли недоработку отправте на почту: tamivant0714@gmail.com'
                                      '. Приятной игры!', reply_markup = configKeyboard.keyboard)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?", reply_markup = configKeyboard.keyboard)
    elif message.text.lower() == "пока":
        bot.send_message(message.from_user.id, "Пока(((", reply_markup = configKeyboard.keyboard)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, 'Чем я могу тебе помочь?', reply_markup = configKeyboard.keyboard)
    elif message.text.lower() == "регистрация":
        reg_message(message)
    elif message.text.lower() == "начать игру":

        conn = sqlite3.connect('orders.db')
        cur = conn.cursor()

        cur.execute("""SELECT userid FROM users WHERE userid = {}""".format(message.from_user.id))
        res = cur.fetchone()
        #print(res)

        conn.close()

        if res == None:
            bot.send_message(message.from_user.id, 'Заригистрируйся!')
        else:
            bot.send_message(message.from_user.id, 'Начал!)', reply_markup=configKeyboard.keyboardGame)
            bot.register_next_step_handler(message, Game)

    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
#----------------------------------------------------------------------------------
def reg_message(message):
    if message.text == "регистрация" or "/reg":
        chek_db(message)
    else:
        bot.send_message(message.chat.id, 'Напиши "Pегистрация"')

def get_name(message):
    configValue.name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    configValue.surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет')
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    while configValue.age == 0:
        try:
             configValue.age = int(message.text)
        except Exception:
             bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')

        question = 'Тебе ' + str(configValue.age) + ' лет, тебя зовут ' + configValue.name + ' ' + configValue.surname + '?'
        bot.send_message(message.from_user.id, text = question, reply_markup = configKeyboard.keyboardAnswer)
        reg_db(message)


def Game(message):
    if message.text.lower() == "оружие":
        bot.send_message(message.from_user.id, text ='Какое?', reply_markup = configKeyboard.keyboardWeapon)
        configValue.STATUSWeapon = True
        bot.register_next_step_handler(message, Game)
    elif message.text.lower() == "атака":
        bot.send_message(message.from_user.id, text = 'Чем?)', reply_markup = configKeyboard.keyboardAttack)
        configValue.STATUSWeapon = False
        bot.register_next_step_handler(message, Game)
    elif message.text.lower() == "способности":
        bot.send_message(message.from_user.id, text = 'Вот все способности: ', reply_markup = configKeyboard.keyboardSkill)
        configValue.STATUSWeapon = False
        bot.register_next_step_handler(message, Game)
    elif message.text.lower() == "лавка":
        configValue.STATUSWeapon = False
        bot.send_message(message.from_user.id, 'Добро пожаловать в "Лавку на склоне"!!!', reply_markup=configKeyboard.keyboardShop)
        bot.register_next_step_handler(message, Game)
    elif message.text.lower() == "баланс":
        configValue.STATUSWeapon = False

        inventory = sqlite3.connect('orders.db')
        cursor = inventory.cursor()

        cursor.execute("""SELECT user_money FROM inventory WHERE userid = {}""".format(message.from_user.id))
        res = cursor.fetchone()
        req = res[0]
        if req == None or res == '':
            bot.send_message(message.from_user.id, 'Вы бедняк! ', reply_markup=configKeyboard.keyboardGame)
            bot.register_next_step_handler(message, Game)
        else:
            bot.send_message(message.from_user.id, 'Ваш баланс: ' + str(req), reply_markup=configKeyboard.keyboardGame)
            bot.register_next_step_handler(message, Game)

        inventory.close()

    elif message.text.lower() == "инвентарь":
        configValue.STATUSWeapon = False
        bot.send_message(message.from_user.id, 'Инвентарь открыт! ', reply_markup=configKeyboard.keyboardInventory)
        bot.register_next_step_handler(message, Game)
    elif message.text.lower() == "мои предметы":
        configValue.STATUSWeapon = False

        inventory = sqlite3.connect('orders.db')
        cursor = inventory.cursor()

        cursor.execute("""SELECT item FROM inventory  WHERE userid = {}""".format(message.from_user.id))

        r = cursor.fetchone()
        rs = r[0]
        #print(rs)

        inventory.close()
        if rs == None or rs == '':
            bot.send_message(message.from_user.id, text='Предметов нет!) ', reply_markup=configKeyboard.keyboardGame)
            bot.register_next_step_handler(message, Game)
        else:
            bot.send_message(message.from_user.id, text='Вот все предметы: ' + rs,
                             reply_markup=configKeyboard.keyboardGame)
            bot.register_next_step_handler(message, Game)


    elif message.text.lower() == "мое оружие":
        configValue.STATUSWeapon = False

        inventory = sqlite3.connect('orders.db')
        cursor = inventory.cursor()

        cursor.execute("""SELECT weapon FROM inventory  WHERE userid = {}""".format(message.from_user.id))

        rs = ''

        r = cursor.fetchone()
        if r == None:
            pass
        else:
            rs = r[0]
            #print(rs)

        if rs == None or rs == '':
            bot.send_message(message.from_user.id, text='Безоружен ',
                            reply_markup=configKeyboard.keyboardGame)
            bot.register_next_step_handler(message, Game)
        else:
            bot.send_message(message.from_user.id, text='Экированно: ' + rs,
                                reply_markup=configKeyboard.keyboardGame)
            bot.register_next_step_handler(message, Game)

        inventory.close()
    elif message.text.lower() == "мои способности":
        configValue.STATUSWeapon = False

        inventory = sqlite3.connect('orders.db')
        cursor = inventory.cursor()

        cursor.execute("""SELECT skill FROM inventory  WHERE userid = {}""".format(message.from_user.id))

        r = cursor.fetchone()
        rs = r[0]
        #print(rs)

        if rs == None or rs == '':
            bot.send_message(message.from_user.id, text='Нет активных способностей ',
                            reply_markup=configKeyboard.keyboardGame)
            bot.register_next_step_handler(message, Game)
        else:
            bot.send_message(message.from_user.id, text='Активированна: ' + rs,
                                reply_markup=configKeyboard.keyboardGame)
            bot.register_next_step_handler(message, Game)
    elif message.text.lower() == "выход":
        configValue.STATUSWeapon = False
        bot.send_message(message.from_user.id, 'Выход произведен', reply_markup = configKeyboard.keyboard)
    else:
        pass


#---------------------------------------------------------------------------------------
@bot.message_handler(commands=['randnumber'])
def respawn_enemy(call):
    #quant = call.message.text
    #print(quant)


    if call.data == 'enemy_skeleton':
        if configValue.enemy1_respawn < 10:
            bot.send_message(call.message.chat.id, '"Скелет" еще мертв')
        else:
            random_M = random.randint(1, 2)
            if random_M == 1:
                configValue.user_money += 10

                money_db(call)

            else:
                pass

            attack_db(call)
            check_atack_db(call)
            LvL_bd(call)
            new_LvL_db(call, configValue.Enemy1_exp)
            check_EXP_db(call)
            bot.send_message(call.message.chat.id, '"Скелет" возродится через 10 сек.')

            while configValue.enemy1_respawn > 0:
                configValue.enemy1_respawn -= 1
                time.sleep(1)
                #print(configValue.enemy1_respawn)
            bot.send_message(call.message.chat.id, '"Скелет" возродился!')
            configValue.enemy1_respawn = 10
            configValue.XP_enemy1 = 100
    elif call.data == "enemy_mechanical-beetle":
        if configValue.enemy2_respawn < 15:
            bot.send_message(call.message.chat.id, '"Мех. жук" еще мертв')
        else:
            random_M = random.randint(1, 2)
            if random_M == 1:
                configValue.user_money += 20

                money_db(call)

            else:
                pass

            attack_db(call)
            check_atack_db(call)
            LvL_bd(call)
            new_LvL_db(call, configValue.Enemy2_exp)
            check_EXP_db(call)

            bot.send_message(call.message.chat.id, '"Мех. жук" возродится через 15 сек.')

            while configValue.enemy2_respawn > 0:
                configValue.enemy2_respawn -= 1
                time.sleep(1)
                #print(configValue.enemy2_respawn)
            bot.send_message(call.message.chat.id, '"Мех. жук" возродился!')
            configValue.enemy2_respawn = 15
            configValue.XP_enemy2 = 125

    elif call.data == "enemy_mad-dog":
        if configValue.enemy3_respawn < 20:
            bot.send_message(call.message.chat.id, '"Бешенный пес" еще мертв')
        else:
            random_M = random.randint(1, 2)
            if random_M == 1:
                configValue.user_money += 50

                money_db(call)

            else:
                pass

            attack_db(call)
            check_atack_db(call)
            LvL_bd(call)
            new_LvL_db(call, configValue.Enemy3_exp)
            check_EXP_db(call)

            bot.send_message(call.message.chat.id, '"Бешенный пес" возродится через 15 сек.')

            while configValue.enemy3_respawn > 0:
                configValue.enemy3_respawn -= 1
                time.sleep(1)
                #print(configValue.enemy3_respawn)
            bot.send_message(call.message.chat.id, '"Бешенный пес" возродился!')
            configValue.enemy3_respawn = 20
            configValue.XP_enemy3 = 145

    elif call.data == 'skill_enemy_skeleton':
        if configValue.enemy1_respawn < 10:
            bot.send_message(call.message.chat.id, '"Скелет" еще мертв')
        else:
            random_M = random.randint(1, 2)
            if random_M == 1:
                configValue.user_money += 10

                money_db(call)

            else:
                pass

            attack_db(call)
            check_atack_db(call)
            LvL_bd(call)
            new_LvL_db(call, configValue.Enemy1_exp)
            check_EXP_db(call)

            bot.send_message(call.message.chat.id, '"Скелет" возродится через 10 сек.')

            while configValue.enemy1_respawn > 0:
                configValue.enemy1_respawn -= 1
                time.sleep(1)
                #print(configValue.enemy1_respawn)
            bot.send_message(call.message.chat.id, '"Скелет" возродился!')
            configValue.enemy1_respawn = 10
            configValue.XP_enemy1 = 100
    elif call.data == "skill_enemy_mechanical-beetle":
        if configValue.enemy2_respawn < 15:
            bot.send_message(call.message.chat.id, '"Мех. жук" еще мертв')
        else:
            random_M = random.randint(1, 2)
            if random_M == 1:
                configValue.user_money += 20

                money_db(call)

            else:
                pass

            attack_db(call)
            check_atack_db(call)
            LvL_bd(call)
            new_LvL_db(call, configValue.Enemy2_exp)
            check_EXP_db(call)

            bot.send_message(call.message.chat.id, '"Мех. жук" возродится через 15 сек.')

            while configValue.enemy2_respawn > 0:
                configValue.enemy2_respawn -= 1
                time.sleep(1)
                #print(configValue.enemy2_respawn)
            bot.send_message(call.message.chat.id, '"Мех. жук" возродился!')
            configValue.enemy2_respawn = 15
            configValue.XP_enemy2 = 125
    elif call.data == "skill_enemy_mad-dog":
        if configValue.enemy3_respawn < 20:
            bot.send_message(call.message.chat.id, '"Бешенный пес" еще мертв')
        else:
            random_M = random.randint(1, 2)
            if random_M == 1:
                configValue.user_money += 50

                money_db(call)
                
            else:
                pass

            attack_db(call)
            check_atack_db(call)
            LvL_bd(call)
            new_LvL_db(call, configValue.Enemy3_exp)
            check_EXP_db(call)

            bot.send_message(call.message.chat.id, '"Бешенный пес" возродится через 15 сек.')

            while configValue.enemy3_respawn > 0:
                configValue.enemy3_respawn -= 1
                time.sleep(1)
                #print(configValue.enemy3_respawn)
            bot.send_message(call.message.chat.id, '"Бешенный пес" возродился!')
            configValue.enemy3_respawn = 20
            configValue.XP_enemy3 = 145

#---------------------------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def response_processing(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Запомню : )')
        configValue.STATUSAnswer = True
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Еще раз! ', reply_markup = configKeyboard.keyboard)

    # Враги--------------------------------------------------------------------------------
    elif call.data == "gun":

        inventory = sqlite3.connect("orders.db")
        cursor = inventory.cursor()

        cursor.execute("""SELECT weapon FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

        rs = ''

        r = cursor.fetchone()
        if r == None:
            pass
        else:
            rs = r[0]
            print(rs)

        inventory.close()

        if rs != None or rs != '':
            bot.send_message(call.message.chat.id, 'Кого?', reply_markup = configKeyboard.keyboardEnemy)
        else:
            bot.send_message(call.message.chat.id, 'Возьми оружие!', reply_markup=configKeyboard.keyboardGame)
    elif call.data == "skill":

        inventory = sqlite3.connect("orders.db")
        cursor = inventory.cursor()

        cursor.execute("""SELECT skill FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

        rs = ''

        r = cursor.fetchone()
        if r == None:
            pass
        else:
            rs = r[0]
            print(rs)

        inventory.close()

        if rs != None or rs != '':
            bot.send_message(call.message.chat.id, 'Кого?', reply_markup=configKeyboard.keyboardEnemy_Skills)
        else:
            bot.send_message(call.message.chat.id, 'Нет активных способностей!', reply_markup=configKeyboard.keyboardGame)

    elif call.data == "skill_enemy_skeleton":

        inventory = sqlite3.connect("orders.db")
        cursor = inventory.cursor()

        cursor.execute("""SELECT skill FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

        rs = ''

        r = cursor.fetchone()
        if r == None:
            pass
        else:
            rs = r[0]
            print(rs)

        inventory.close()

        if configValue.XP_enemy1 > 0:
            if rs == 'огненная стрела':
                if configValue.XP_enemy1 < configValue.damage_fiery_stream:
                    configValue.XP_enemy1 = 0
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy1), reply_markup=configKeyboard.keyboardGame)
                else:
                    configValue.XP_enemy1 -= configValue.damage_fiery_stream
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy1), reply_markup = configKeyboard.keyboardGame)
            elif rs == 'водянной брызг':
                if configValue.XP_enemy1 < configValue.damage_water_spray:
                    configValue.XP_enemy1 = 0
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy1), reply_markup=configKeyboard.keyboardGame)
                else:
                    configValue.XP_enemy1 -= configValue.damage_water_spray
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy1), reply_markup=configKeyboard.keyboardGame)
        elif rs == "":
            bot.send_message(call.message.chat.id, 'Нет активных способностей!', reply_markup=configKeyboard.keyboardGame)
        else:
            attack_db(call)
            respawn_enemy(call)

    elif call.data == "skill_enemy_mechanical-beetle":


        inventory = sqlite3.connect("orders.db")
        cursor = inventory.cursor()

        cursor.execute("""SELECT skill FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

        r = cursor.fetchone()
        rs = r[0]
        print(rs)

        inventory.close()

        if configValue.XP_enemy2 == 0:
            randoms = random.randint(1, 3)
            if randoms == 1:
                configValue.item = configItems.item_1
            elif randoms == 2:
                configValue.item = configItems.item_2
            elif randoms == 3:
                configValue.item = configItems.item_3
            #bot.send_message(call.message.chat.id, 'Враг убит!) С него выпал предмет: ' + configValue.item,
                             #reply_markup=configKeyboard.keyboardGame)
            # bot.send_message(call.message.chat.id, 'С него выпал предмет: ' + configValue.item, reply_markup=configKeyboard.keyboardGame)
            respawn_enemy(call)


        elif configValue.XP_enemy2 > 0:
            if rs == "огненная струя":
                if configValue.XP_enemy2 < configValue.damage_fiery_stream:
                    configValue.XP_enemy2 = 0
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy2), reply_markup=configKeyboard.keyboardGame)
                else:
                    configValue.XP_enemy2 -= configValue.damage_fiery_stream
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy2), reply_markup = configKeyboard.keyboardGame)
            elif rs == "водянной брызг":
                if configValue.XP_enemy2 < configValue.damage_fiery_stream:
                    configValue.XP_enemy2 = 0
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy2), reply_markup=configKeyboard.keyboardGame)
                else:
                    configValue.XP_enemy2 -= configValue.damage_water_spray
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy2), reply_markup=configKeyboard.keyboardGame)
            else:
                bot.send_message(call.message.chat.id, 'Нет активных способностей!', reply_markup=configKeyboard.keyboardGame)


    elif call.data == "skill_enemy_mad-dog":


        inventory = sqlite3.connect("orders.db")
        cursor = inventory.cursor()

        cursor.execute("""SELECT skill FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

        r = cursor.fetchone()
        rs = r[0]
        print(rs)

        inventory.close()

        if configValue.XP_enemy3 > 0:
            if rs == "огненная струя":
                if configValue.XP_enemy3 < configValue.damage_fiery_stream:
                    configValue.XP_enemy3 = 0
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy3), reply_markup=configKeyboard.keyboardGame)
                else:
                    configValue.XP_enemy3 -= configValue.damage_fiery_stream
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy3), reply_markup = configKeyboard.keyboardGame)
            elif rs == "водянной брызг":
                if configValue.XP_enemy3 < configValue.damage_water_spray:
                    configValue.XP_enemy3 = 0
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy3), reply_markup=configKeyboard.keyboardGame)
                else:
                    configValue.XP_enemy3 -= configValue.damage_water_spray
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy3),
                                     reply_markup=configKeyboard.keyboardGame)
            else:
                bot.send_message(call.message.chat.id, 'Нет активных способностей!', reply_markup=configKeyboard.keyboardGame)
        else:
            randoms = random.randint(1, 3)
            if randoms == 1:
                configValue.item = configItems.item_1
            elif randoms == 2:
                configValue.item = configItems.item_2
            elif randoms == 3:
                configValue.item = configItems.item_3
            #bot.send_message(call.message.chat.id, 'Враг убит!) С него выпал предмет: ' + configValue.item,
                             #reply_markup=configKeyboard.keyboardGame)
            # bot.send_message(call.message.chat.id, 'С него выпал предмет: ' + configValue.item, reply_markup=configKeyboard.keyboardGame)
            respawn_enemy(call)

    elif call.data == "enemy_skeleton":


        inventory = sqlite3.connect("orders.db")
        cursor = inventory.cursor()

        cursor.execute("""SELECT weapon FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

        rs = ''

        r = cursor.fetchone()
        if r == None:
            pass
        else:
            rs = r[0]
            print(rs)

        inventory.close()

        if configValue.XP_enemy1 > 0:
            if rs == "пистолет":
                if configValue.XP_enemy1 < configValue.damage_pistol:
                    configValue.XP_enemy1 = 0
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy1),
                                     reply_markup=configKeyboard.keyboardGame)
                else:
                    configValue.XP_enemy1 -= configValue.damage_pistol
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy1), reply_markup = configKeyboard.keyboardGame)
            elif rs == "винтовка":
                if configValue.XP_enemy1 < configValue.damage_rifle:
                    configValue.XP_enemy1 = 0
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy1),
                                     reply_markup=configKeyboard.keyboardGame)
                else:
                    configValue.XP_enemy1 -= configValue.damage_rifle
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy1), reply_markup=configKeyboard.keyboardGame)
            elif rs == "газовая ракета":
                if configValue.XP_enemy1 < configValue.damage_rocket:
                    configValue.XP_enemy1 = 0
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy1),
                                     reply_markup=configKeyboard.keyboardGame)
                else:
                    configValue.XP_enemy1 -= configValue.damage_rocket
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy1), reply_markup=configKeyboard.keyboardGame)
        elif rs == "":
            bot.send_message(call.message.chat.id, 'Возьми Оружие', reply_markup=configKeyboard.keyboardGame)
        else:
            randoms = random.randint(1, 3)
            if randoms == 1:
                configValue.item = configItems.item_1
            elif randoms == 2:
                configValue.item = configItems.item_2
            elif randoms == 3:
                configValue.item = configItems.item_3
            #bot.send_message(call.message.chat.id, 'Враг убит!) С него выпал предмет: ' + configValue.item,
                             #reply_markup=configKeyboard.keyboardGame)
            # bot.send_message(call.message.chat.id, 'С него выпал предмет: ' + configValue.item, reply_markup=configKeyboard.keyboardGame)
            respawn_enemy(call)

    elif call.data == "enemy_mechanical-beetle":

        inventory = sqlite3.connect("orders.db")
        cursor = inventory.cursor()

        cursor.execute("""SELECT weapon FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

        rs = ''

        r = cursor.fetchone()
        if r == None:
            pass
        else:
            rs = r[0]
            print(rs)

        inventory.close()

        if configValue.XP_enemy2 == 0:
            randoms = random.randint(1, 3)
            if randoms == 1:
                configValue.item = configItems.item_1
            elif randoms == 2:
                configValue.item = configItems.item_2
            elif randoms == 3:
                configValue.item = configItems.item_3
            #bot.send_message(call.message.chat.id, 'Враг убит!) С него выпал предмет: ' + configValue.item,
                             #reply_markup=configKeyboard.keyboardGame)
            # bot.send_message(call.message.chat.id, 'С него выпал предмет: ' + configValue.item, reply_markup=configKeyboard.keyboardGame)
            respawn_enemy(call)

        elif configValue.XP_enemy2 > 0:
            if rs == "пистолет":
                if configValue.XP_enemy2 < configValue.damage_pistol:
                    configValue.XP_enemy2 = 0
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy2),
                                     reply_markup=configKeyboard.keyboardGame)
                else:
                    configValue.XP_enemy2 -= configValue.damage_pistol
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy2),
                                     reply_markup=configKeyboard.keyboardGame)
            elif rs == "винтовка":
                if configValue.XP_enemy2 < configValue.damage_rifle:
                    configValue.XP_enemy2 = 0
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy2),
                                     reply_markup=configKeyboard.keyboardGame)
                else:
                    configValue.XP_enemy2 -= configValue.damage_rifle
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy2),
                                     reply_markup=configKeyboard.keyboardGame)
            elif rs == "газовая ракета":
                if configValue.XP_enemy2 < configValue.damage_rocket:
                    configValue.XP_enemy2 = 0
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy2),
                                     reply_markup=configKeyboard.keyboardGame)
                else:
                    configValue.XP_enemy2 -= configValue.damage_rocket
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy2),
                                     reply_markup=configKeyboard.keyboardGame)
        else:
            bot.send_message(call.message.chat.id, 'Возьми Оружие', reply_markup=configKeyboard.keyboardGame)


    elif call.data == "enemy_mad-dog":

        inventory = sqlite3.connect("orders.db")
        cursor = inventory.cursor()

        cursor.execute("""SELECT weapon FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

        rs = ''

        r = cursor.fetchone()
        if r == None:
            pass
        else:
            rs = r[0]
            print(rs)

        inventory.close()

        if configValue.XP_enemy3 > 0:
            if rs == "пистолет":
                if configValue.XP_enemy3 < configValue.damage_pistol:
                    configValue.XP_enemy3 = 0
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy3),
                                     reply_markup=configKeyboard.keyboardGame)
                else:
                    configValue.XP_enemy3 -= configValue.damage_pistol
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy3),
                                     reply_markup=configKeyboard.keyboardGame)
            elif rs == "винтовка":
                if configValue.XP_enemy3 < configValue.damage_rifle:
                    configValue.XP_enemy3 = 0
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy3),
                                     reply_markup=configKeyboard.keyboardGame)
                else:
                    configValue.XP_enemy3 -= configValue.damage_rifle
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy3),
                                     reply_markup=configKeyboard.keyboardGame)
            elif rs == "газовая ракета":
                if configValue.XP_enemy3 < configValue.damage_rocket:
                    configValue.XP_enemy3 = 0
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy3),
                                     reply_markup=configKeyboard.keyboardGame)
                else:
                    configValue.XP_enemy3 -= configValue.damage_rocket
                    bot.send_message(call.message.chat.id, 'Ударил! ', reply_markup=configKeyboard.keyboardGame)
                    bot.send_message(call.message.chat.id, 'Жизний осталось = ' + str(configValue.XP_enemy3),
                                     reply_markup=configKeyboard.keyboardGame)
            elif rs == "":
                bot.send_message(call.message.chat.id, 'Возьми Оружие', reply_markup=configKeyboard.keyboardGame)
        else:
            randoms = random.randint(1, 3)
            if randoms == 1:
                configValue.item = configItems.item_1
            elif randoms == 2:
                configValue.item = configItems.item_2
            elif randoms == 3:
                configValue.item = configItems.item_3
            #bot.send_message(call.message.chat.id, 'Враг убит!) С него выпал предмет: ' + configValue.item,
                             #reply_markup=configKeyboard.keyboardGame)
            # bot.send_message(call.message.chat.id, 'С него выпал предмет: ' + configValue.item, reply_markup=configKeyboard.keyboardGame)
            respawn_enemy(call)

    #Способности----------------------------------------------------------------------------
    elif call.data == "fiery_stream":

        inventory = sqlite3.connect('orders.db')
        cursor = inventory.cursor()

        cursor.execute("""SELECT skill FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

        rs = ''

        r = cursor.fetchone()
        if r == None:
            pass
        else:
            rs = r[0]
            print(rs)

        inventory.close()

        if rs == None or rs == '':
            bot.send_message(call.message.chat.id, 'Способность активированна', reply_markup=configKeyboard.keyboardGame)
            skill = 'огненная струя'
            skill_db(call, skill)

        else:
            bot.send_message(call.message.chat.id, 'Слот занят!')

    elif call.data == "water_spray":

        inventory = sqlite3.connect('orders.db')
        cursor = inventory.cursor()

        cursor.execute("""SELECT skill FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

        rs = ''

        r = cursor.fetchone()
        if r == None:
            pass
        else:
            rs = r[0]
            print(rs)

        inventory.close()

        if rs == None or rs == '':
            bot.send_message(call.message.chat.id, 'Способность активированна', reply_markup=configKeyboard.keyboardGame)
            skill = 'водянной брызг'
            skill_db(call, skill)
        else:
            bot.send_message(call.message.chat.id, 'Слот занят!')

    elif call.data == "clear":

        inventory = sqlite3.connect('orders.db')
        cursor = inventory.cursor()

        skill = ''

        cursor.execute("""UPDATE inventory 
                            SET skill = ?
                            WHERE userid = ?""", (skill, call.message.chat.id))

        inventory.commit()
        inventory.close()

        bot.send_message(call.message.chat.id, 'Способности очищенный', reply_markup=configKeyboard.keyboardGame)

    #Пушки--------------------------------------------------------------------------------
    elif configValue.STATUSWeapon:

        inventory = sqlite3.connect('orders.db')
        cursor = inventory.cursor()

        cursor.execute("""SELECT weapon FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

        rs = ''

        r = cursor.fetchone()
        if r == None:
            pass
        else:
            rs = r[0]
            print(rs)

        if rs == None or rs == '':

            if call.data == "pistol":
                bot.send_message(call.message.chat.id, 'Взял пистолет ', reply_markup=configKeyboard.keyboardGame)
                weapon = 'пистолет'
                weapon_db(call, weapon)

            elif call.data == "rifle":
                bot.send_message(call.message.chat.id, 'Взял винтовку ', reply_markup=configKeyboard.keyboardGame)
                weapon = 'винтовка'
                weapon_db(call, weapon)

            elif call.data == "rocket":
                bot.send_message(call.message.chat.id, 'Взял газовую ракету ',
                                    reply_markup=configKeyboard.keyboardGame)
                weapon = 'газовая ракета'
                weapon_db(call, weapon)

        elif len(rs) > 2:

            if call.data == "drop":
                bot.send_message(call.message.chat.id, 'Все оружие выброшенно ',
                                 reply_markup=configKeyboard.keyboardGame)
                weapon = ''

                cursor.execute("""UPDATE inventory 
                                    SET weapon = ?
                                    WHERE userid = ?""", (weapon, call.message.chat.id))

            elif len(rs) > 2:

                bot.send_message(call.message.chat.id, 'Место под оружие занято( ',
                                 reply_markup=configKeyboard.keyboardWeapon_Drop)

        inventory.commit()
        inventory.close()


    elif call.data == 'buy':
        shop_buy(call)

    elif call.data == 'rusty bolt':

        inventory = sqlite3.connect('orders.db')
        cursor = inventory.cursor()

        cursor.execute("""SELECT user_money FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

        rs = ''

        r = cursor.fetchone()
        if r == None:
            pass
        else:
            rs = r[0]
            print(rs)
        inventory.close()

        if rs >= configValue.price_item1:
            away = rs - configValue.price_item1

            inventory = sqlite3.connect('orders.db')
            cursor = inventory.cursor()

            cursor.execute("""UPDATE inventory 
                                SET user_money = ?
                                WHERE userid = ?""", (away, call.message.chat.id))

            cursor.execute("""UPDATE inventory 
                                SET item = ?
                                WHERE userid = ?""", (configItems.item_1, call.message.chat.id))

            inventory.commit()
            inventory.close()

            bot.send_message(call.message.chat.id, 'Держи он почти новый) ',
                             reply_markup=configKeyboard.keyboardShop)

        else:
            bot.send_message(call.message.chat.id, 'А монеты?! ',
                             reply_markup=configKeyboard.keyboardShop)

    elif call.data == 'bone':

        inventory = sqlite3.connect('orders.db')
        cursor = inventory.cursor()

        cursor.execute("""SELECT user_money FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

        rs = ''

        r = cursor.fetchone()
        if r == None:
            pass
        else:
            rs = r[0]
            print(rs)

        inventory.close()

        if rs >= configValue.price_item2:
            away = rs - configValue.price_item2

            inventory = sqlite3.connect('orders.db')
            cursor = inventory.cursor()

            cursor.execute("""UPDATE inventory 
                                 SET user_money = ?
                                 WHERE userid = ?""", (away, call.message.chat.id))

            cursor.execute("""UPDATE inventory 
                                 SET item = ?
                                 WHERE userid = ?""", (configItems.item_2, call.message.chat.id))

            inventory.commit()
            inventory.close()

            bot.send_message(call.message.chat.id, 'Держи самая свежая! ',
                             reply_markup=configKeyboard.keyboardShop)
            configValue.item = configItems.item_1
        else:
            bot.send_message(call.message.chat.id, 'А монеты?! ',
                             reply_markup=configKeyboard.keyboardShop)

    elif call.data == 'rotten meat':

        inventory = sqlite3.connect('orders.db')
        cursor = inventory.cursor()

        cursor.execute("""SELECT user_money FROM inventory  WHERE userid = {}""".format(call.message.chat.id))

        rs = ''

        r = cursor.fetchone()
        if r == None:
            pass
        else:
            rs = r[0]
            print(rs)

        inventory.close()

        if rs>= configValue.price_item3:
            away = rs - configValue.price_item3

            inventory = sqlite3.connect('orders.db')
            cursor = inventory.cursor()

            cursor.execute("""UPDATE inventory 
                                SET user_money = ?
                                WHERE userid = ?""", (away, call.message.chat.id))

            cursor.execute("""UPDATE inventory 
                                SET item = ?
                                WHERE userid = ?""", (configItems.item_3, call.message.chat.id))

            inventory.commit()
            inventory.close()

            bot.send_message(call.message.chat.id, 'Держи еще мокрое) ',
                             reply_markup=configKeyboard.keyboardShop)
            configValue.item = configItems.item_1
        else:
            bot.send_message(call.message.chat.id, 'А монеты?! ',
                             reply_markup=configKeyboard.keyboardShop)


    elif call.data == 'sell':
        shop_sell(call)

    elif call.data == 'esc':
        bot.send_message(call.message.chat.id, 'Прощай!!!', reply_markup=configKeyboard.keyboardGame)

    else:
        pass
#---------------------------------------------------------------------------------------

bot.polling(none_stop=True, interval=0)
