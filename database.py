import psycopg2
from conf import DB_NAME, DB_USER, DB_PASS, DB_PORT, DB_HOST

params = {
    'dbname': DB_NAME,
    'user': DB_USER,
    'password': DB_PASS,
    'host': DB_HOST,
    'port': DB_PORT
}

conn = psycopg2.connect(**params)
conn.autocommit = True
cur = conn.cursor()

def get_tg_by_id(db_user_id):
    query = "SELECT tg_chat_id FROM \"user\" WHERE id=%s;"
    cur.execute(query, (db_user_id,))
    return cur.fetchall()

def check_user(username):
    query = "SELECT id FROM \"user\" WHERE telegram=%s;"
    cur.execute(query, (username,))
    return cur.fetchall()

def check_user_confirmed(db_user_id):
    query = "SELECT tg_confirmed FROM \"user\" WHERE id=%s;"
    cur.execute(query, (db_user_id,))
    a = cur.fetchall()[0][0]
    return a

def set_confirmed_tg(username, tg_chat_id):
    try:
        query = "UPDATE \"user\" SET tg_chat_id='%s', tg_confirmed='t' WHERE telegram=%s;"
        cur.execute(query, (tg_chat_id, username))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def check_deadlines(date):
    try:
        query = """SELECT u.tg_chat_id, t.name
FROM \"user\" as u
INNER JOIN task_assign as ta
    ON u.id = ta.user_id
INNER JOIN task as t
    ON t.id = ta.task_id
WHERE t.due_date = %s ;"""
        cur.execute(query, (date.strftime("%d.%m.%Y"),))
        return cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)