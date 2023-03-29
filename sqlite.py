import sqlite3 as sq

conn = sq.connect('db/user.db', check_same_thread=False)
cursor = conn.cursor()

def db_table_val(user_id: int, username: str, passw: str, salt: str):
    cursor.execute('INSERT INTO test (user_id, username, passw, salt) VALUES (?, ?, ?, ?)', (user_id, username, passw, salt))
    conn.commit()
def db_table_main(user_id: int, username: str):
    cursor.execute('INSERT INTO test (user_id, username) VALUES (?, ?)', (user_id, username))
    conn.commit()
def db_table_ed(passw: str, user_id: int):
    sqlff = 'UPDATE test SET passw =? where user_id = ?'
    data = (passw, user_id)
    cursor.execute(sqlff, data)
    conn.commit()
def db_table_ed2(salt: str, user_id: int):
    sqlff = 'UPDATE test SET salt =? where user_id = ?'
    data = (salt, user_id)
    cursor.execute(sqlff, data)
    conn.commit()
def getName(conn, user_id: int):
    c = conn.cursor()
    c.execute("SELECT passw FROM test WHERE user_id = ?", (user_id, ))
    result = c.fetchone()
    if result:
        return result[0]
def getSalt(conn, user_id: int):
    c = conn.cursor()
    c.execute("SELECT salt FROM test WHERE user_id = ?", (user_id, ))
    result = c.fetchone()
    if result:
        return result[0]
def getTrue(user_id: int):
    check_id = user_id
    all_id = [x[0] for x in cursor.execute("SELECT user_id FROM test").fetchall()]
    if check_id in all_id:
        return True
    else:
        return False