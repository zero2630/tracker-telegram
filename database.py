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

def check_user(username):
    query = "SELECT id FROM \"user\" WHERE telegram=%s;"
    cur.execute(query, (username,))
    a =  cur.fetchall()
    print(a)

def set_confirmed_tg(username, tg_chat_id):
    query = "UPDATE \"user\" SET tg_chat_id='%d', tg_confirmed='t' WHERE telegram=%s;"
    cur.execute(query, (tg_chat_id, username))
