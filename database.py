import logging
# logging.basicConfig(level=logging.INFO)  # Отключить после дебага

import mysql.connector
from mysql.connector import Error
import env.config

from datetime import datetime, date
from dateutil.relativedelta import relativedelta





def mydbConnection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=env.config.db_host,
            user=env.config.db_name,
            passwd=env.config.db_pass,
            database=env.config.db_name
        )
    except Error as e:
        logging.error(f"The error '{e}' occurred")

    return connection




def add_new_user(user_id, user_name):
    connection = mydbConnection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * from users WHERE user_id='{user_id}'")
    if cursor.fetchall():  # checking if something found with this username
        logging.info('User_id:' + str(user_id) + ' already exists. His user_name is:' + user_name)
    else:
        sql = "INSERT INTO users (user_id, user_name, subscribe_until, count_request) VALUES (%s, %s, %s, %s)"
        val = (user_id, user_name, datetime.now().date(), 0)
        cursor.execute(sql, val)
        connection.commit()
        logging.info('New user has been registred, iser_id:' + str(user_id) + ' User_name:' + user_name)


def check_user_status(user_id, user_name=''):
    connection = mydbConnection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT user_id, status from users WHERE user_id='{user_id}'")
    myresult = cursor.fetchall()
    return myresult[0][1]


# myresult1 = check_user_status(243697626, 'Василий')
# print(myresult1)

def new_free_day(user_id, connection):
    cursor = connection.cursor()
    sql = f"""UPDATE users 
            SET subscribe_until='{datetime.now().date()}',
                count_request=1             
            WHERE user_id='{user_id}'"""
    try:
        cursor.execute(sql)
        connection.commit()
    except:
        logging.error('DB append failed!')
        connection.rollback()

def new_try_counter(user_id, connection):
    cursor = connection.cursor()
    sql = f"""UPDATE users 
            SET count_request = count_request + 1             
            WHERE user_id='{user_id}'"""
    try:
        cursor.execute(sql)
        connection.commit()
    except:
        logging.error('DB append failed!')
        connection.rollback()

def change_user_status_to_free(user_id, connection):
    cursor = connection.cursor()
    sql = f"""UPDATE users 
            SET status = 'free', 
            count_request = 1,
            subscribe_until='{datetime.now().date()}'        
            WHERE user_id='{user_id}'"""
    try:
        cursor.execute(sql)
        connection.commit()
    except:
        logging.error('DB append failed! change_user_status_to_free ')
        connection.rollback()

def can_user_make_openAI_request(user_id):
    connection = mydbConnection()
    cursor = connection.cursor()
    sql = f"SELECT user_id, status, subscribe_until, count_request, thread_id from users WHERE user_id='{user_id}'"
    cursor.execute(sql)
    myresult = cursor.fetchall()[0]
    status = myresult[1]
    subscribe_until = myresult[2]
    count_request = myresult[3]
    thread_id = myresult[4]

    if status=='admin':
        return True
    elif status=='paid':
        if subscribe_until >= datetime.now().date(): # Если подписка не закончилась
            logging.info("User_id:" + str(user_id) + " payed trying")
            return True, thread_id
        else:                                        # Подписка закончилась, но еще можно бесплатно
            logging.info("User_id:" + str(user_id) + " trying, but subscribe finishing. Free try #1")
            change_user_status_to_free(user_id, connection)
            return True, thread_id
    elif status=='free':
        if subscribe_until < datetime.now().date():  # Если сегодня не было попыток, снова бесплатные запросы
            new_free_day(user_id, connection)
            logging.info("User_id:" + str(user_id) + " obnulil his free days, Free try#1")
            return True, thread_id
        else:                                        # Попытки сегодня были уже. Сча будем считать их
            if count_request < env.config.count_request_maximum_free: # Бесплатных попыток хватает,
                new_try_counter(user_id, connection)
                logging.info("User_id:" + str(user_id) + ". Free try#" + str(count_request+1))
                return True, thread_id
            else:                                     # Бесплатные попытки закончились
                logging.info("User_id:" + str(user_id) + " free try finished")
                return False


    # print(myresult)

# print(can_user_make_openAI_request(123))


def make_one_month_subscribe(user_id):
    connection = mydbConnection()
    cursor = connection.cursor()

    one_month_later = datetime.now() + relativedelta(months=+1)
    str_one_month_later = one_month_later.strftime("%Y-%m-%d")

    sql = f"UPDATE users SET status = 'paid', subscribe_until='{str_one_month_later}' WHERE user_id='{user_id}'"

    try:
        cursor.execute(sql)
        logging.info("One month subscribe, user_id:" + str(user_id))
        connection.commit()
    except:
        logging.error('DB append failed! make_one_month_subscribe')
        connection.rollback()

# make_one_month_subscribe(123)

def add_thread_id_to_user(user_id, thread_id):
    connection = mydbConnection()
    cursor = connection.cursor()

    sql = f"UPDATE users SET thread_id='{thread_id}' WHERE user_id='{user_id}'"

    try:
        cursor.execute(sql)
        logging.info("make thread for user_id:" + str(user_id))
        connection.commit()
    except:
        logging.error('DB append failed! add_thread_id_to_user \n' + sql)
        connection.rollback()
