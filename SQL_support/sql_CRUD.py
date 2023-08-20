import sqlite3
from auth_helper import proxy_reformer
from auth import Authorisation

def sql_add_account(name, api_id, api_hash, phone, proxy):
    conn = sqlite3.connect ('accounts.db')
    cur = conn.cursor ()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS tg_ac (Name TEXT, API_ID INTEGER PRIMARY KEY NOT NULL, API_HASH TEXT, 
        Phone TEXT, PROXY TEXT)''')
    cur.execute('''INSERT INTO tg_ac (Name, API_ID, API_HASH, Phone, PROXY)
                    VALUES (?, ?, ?, ?, ?)''', (name, api_id, api_hash, phone, proxy))
    conn.commit ()
    conn.close ()


def sql_get_account():
    conn = sqlite3.connect ('accounts.db')
    cur = conn.cursor ()
    cur.execute (
        '''CREATE TABLE IF NOT EXISTS tg_ac (Name TEXT, API_ID INTEGER PRIMARY KEY NOT NULL, API_HASH TEXT, 
        Phone TEXT, PROXY TEXT)''')
    cur.execute('''SELECT * from tg_ac''')
    res = cur.fetchall()
    num = 1
    print(f'NUM  Name    API_ID     API_HASH      Phone      PROXY')
    for row in res:
        print(f'{num} {row[0]} {row[1]} {row[2]} {row[3]} {row[4]}')
        num += 1
    conn.close()


def sql_del_account(api_id):
    conn = sqlite3.connect ('accounts.db')
    cur = conn.cursor ()
    cur.execute (
        '''CREATE TABLE IF NOT EXISTS tg_ac (Name TEXT, API_ID INTEGER PRIMARY KEY NOT NULL, API_HASH TEXT, 
        Phone TEXT, PROXY TEXT)''')
    cur.execute('''SELECT Name FROM tg_ac
    WHERE API_ID == ?''', (api_id, ))
    res = cur.fetchone()
    if res is not None:
        cur.execute ('''DELETE FROM tg_ac 
                    WHERE API_ID == ?''', (api_id,))
        print(f'Account with the name {res[0]} was successfully deleted')
        conn.commit()
    else:
        print('There is no account with such api id')
    conn.close()


def sql_change_proxy(api_id):
    conn = sqlite3.connect ('accounts.db')
    cur = conn.cursor ()
    cur.execute (
        '''CREATE TABLE IF NOT EXISTS tg_ac (Name TEXT, API_ID INTEGER PRIMARY KEY NOT NULL, API_HASH TEXT, 
        Phone TEXT, PROXY TEXT)''')
    cur.execute ('''SELECT Name FROM tg_ac
        WHERE API_ID == ?''', (api_id,))
    res = cur.fetchone ()
    if res is not None:
        proxy = input(f'Enter new proxy for the {res[0]}: ')
        cur.execute ('''UPDATE tg_ac
                        SET PROXY = ? 
                        WHERE API_ID == ?''', (proxy, api_id))
        print (f'Proxy for the account with the name {res[0]} was successfully changed')
        conn.commit ()
    else:
        print ('There is no account with such api id')
    conn.close ()


async def sql_get_acs_credentials(api_id):
    conn = sqlite3.connect ('accounts.db')
    cur = conn.cursor ()
    cur.execute (
        '''CREATE TABLE IF NOT EXISTS tg_ac (Name TEXT, API_ID INTEGER PRIMARY KEY NOT NULL, API_HASH TEXT, 
        Phone TEXT, PROXY TEXT)''')
    cur.execute ('''SELECT * 
        FROM tg_ac
        WHERE API_ID == ?''', (api_id,))
    res = cur.fetchone ()
    if res is not None:
        if ':' in res[4]:
            if res[4].startswith('MTP'):
                proxy = proxy_reformer (res[4])
                conn.close ()
                if len(proxy[2]) == 32:
                    return await Authorisation (res[0], res[1], res[2], res[3], mtproxy=proxy).starts ()
                else:
                    conn.close ()
                    return await Authorisation (res[0], res[1], res[2], res[3], new_mtproxy=proxy).starts ()
            else:
                proxy = proxy_reformer(res[4])
                conn.close ()
                conn.close ()
                return await Authorisation(res[0], res[1], res[2], res[3], proxy).starts()
        else:
            log_in = input(f'Unsupported proxy format or no proxy. Do u wanna log in to {res[0]} without proxy? (y/n) ').lower()
            if log_in == 'y':
                return await Authorisation (res[0], res[1], res[2], res[3]).starts()
            else:
                print('Ok')
                conn.close()
    else:
        print ('There is no account with such api id')
        conn.close ()
        return None



def get_all_api_id():
    conn = sqlite3.connect ('accounts.db')
    cur = conn.cursor ()
    cur.execute (
        '''CREATE TABLE IF NOT EXISTS tg_ac (Name TEXT, API_ID INTEGER PRIMARY KEY NOT NULL, API_HASH TEXT, 
        Phone TEXT, PROXY TEXT)''')
    cur.execute ('''SELECT API_ID FROM tg_ac''')
    res = cur.fetchall ()
    for i in res:
        yield i[0]
    conn.close()



if __name__ == '__main__':
    sql_get_acs_credentials(435353453)
