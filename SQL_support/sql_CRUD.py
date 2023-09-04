import sqlite3
from auth_helper import proxy_reformer
from auth import Authorisation


def sql_add_account(name, api_id, api_hash, phone, proxy, system: str, password: str ='', restriction='false'):
    conn = sqlite3.connect ('accounts.db')
    cur = conn.cursor ()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS tg_ac (Name TEXT, API_ID INTEGER PRIMARY KEY NOT NULL, API_HASH TEXT, 
        Phone TEXT, PROXY TEXT, System TEXT, Password TEXT, Restriction TEXT)''')
    cur.execute('''INSERT INTO tg_ac (Name, API_ID, API_HASH, Phone, PROXY, System, Password, Restriction)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (name, api_id, api_hash, phone, proxy, system, password, restriction))
    conn.commit ()
    conn.close ()


def sql_get_account(restricted_only: bool =False):
    conn = sqlite3.connect ('accounts.db')
    cur = conn.cursor ()
    cur.execute (
        '''CREATE TABLE IF NOT EXISTS tg_ac (Name TEXT, API_ID INTEGER PRIMARY KEY NOT NULL, API_HASH TEXT, 
        Phone TEXT, PROXY TEXT, System TEXT, Password TEXT, Restriction TEXT)''')
    if restricted_only:
        cur.execute ('''SELECT * from tg_ac WHERE Restriction == false''')
    else:
        cur.execute('''SELECT * from tg_ac''')
    res = cur.fetchall()
    num = 1
    print(f'NUM  Name    API_ID     API_HASH      Phone      PROXY      System      Password      Restriction')
    for row in res:
        print(f'{num} {row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} {row[6]} {row[7]}')
        num += 1
    conn.close()


def sql_del_account(api_id):
    conn = sqlite3.connect ('accounts.db')
    cur = conn.cursor ()
    cur.execute (
        '''CREATE TABLE IF NOT EXISTS tg_ac (Name TEXT, API_ID INTEGER PRIMARY KEY NOT NULL, API_HASH TEXT, 
        Phone TEXT, PROXY TEXT, System TEXT, Password TEXT)''')
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
        Phone TEXT, PROXY TEXT, System TEXT, Password TEXT, Restriction TEXT)''')
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


def sql_change_something(api_id, what_to_change, changed_cred): # функция для изменения пароля и рестрикта
    conn = sqlite3.connect ('accounts.db')
    cur = conn.cursor ()
    cur.execute (
        '''CREATE TABLE IF NOT EXISTS tg_ac (Name TEXT, API_ID INTEGER PRIMARY KEY NOT NULL, API_HASH TEXT, 
        Phone TEXT, PROXY TEXT, System TEXT, Password TEXT, Restriction TEXT)''')
    cur.execute ('''SELECT Name FROM tg_ac
        WHERE API_ID == ?''', (api_id,))
    res = cur.fetchone ()
    if res is not None:
        if what_to_change == 'restriction':
            cur.execute ('''UPDATE tg_ac
                            SET Restriction = ? 
                            WHERE API_ID == ?''', (changed_cred, api_id))
            print (f'Restriction for the account with the name {res[0]} was  changed')
            conn.commit ()
        elif what_to_change == 'password':
            cur.execute ('''UPDATE tg_ac
                            SET Password = ? 
                            WHERE API_ID == ?''', (changed_cred, api_id))
            print (f'Password for the account with the name {res[0]} was  changed')
            conn.commit ()
    else:
        print ('There is no account with such api id')
    conn.close ()


async def sql_get_acs_credentials(api_id):
    conn = sqlite3.connect ('accounts.db')
    cur = conn.cursor ()
    cur.execute (
        '''CREATE TABLE IF NOT EXISTS tg_ac (Name TEXT, API_ID INTEGER PRIMARY KEY NOT NULL, API_HASH TEXT, 
        Phone TEXT, PROXY TEXT, System TEXT, Password TEXT, Restriction TEXT)''')
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
                    return await Authorisation (res[0], res[1], res[2], res[3], mtproxy=proxy, password=res[6],
                                                device_model=res[5].split(':')[0], system_version=res[5].split(':')[1], app_version=res[5].split(':')[2]).starts ()
                else:
                    conn.close ()
                    return await Authorisation (res[0], res[1], res[2], res[3], new_mtproxy=proxy, password=res[6],
                                                device_model=res[5].split(':')[0], system_version=res[5].split(':')[1], app_version=res[5].split(':')[2]).starts ()
            else:
                proxy = proxy_reformer(res[4])
                conn.close ()
                return await Authorisation(res[0], res[1], res[2], res[3], proxy, password=res[6],
                                           device_model=res[5].split(':')[0], system_version=res[5].split(':')[1], app_version=res[5].split(':')[2]).starts()
        else:
            log_in = input(f'Unsupported proxy format or no proxy. Do u wanna log in to {res[0]} without proxy? (y/n) ').lower()
            if log_in == 'y':
                conn.close()
                return await Authorisation (res[0], res[1], res[2], res[3], password=res[6],
                                            device_model=res[5].split(':')[0], system_version=res[5].split(':')[1], app_version=res[5].split(':')[2]).starts()
            else:
                print('Ok')
                conn.close()
    else:
        print ('There is no account with such api id')
        conn.close ()
        return None


def sql_get_restriction(api_id):
    conn = sqlite3.connect ('accounts.db')
    cur = conn.cursor ()
    cur.execute (
        '''CREATE TABLE IF NOT EXISTS tg_ac (Name TEXT, API_ID INTEGER PRIMARY KEY NOT NULL, API_HASH TEXT, 
        Phone TEXT, PROXY TEXT, System TEXT, Password TEXT, Restriction TEXT)''')
    cur.execute ('''SELECT Restriction 
            FROM tg_ac
            WHERE API_ID == ?''', (api_id,))
    res = cur.fetchone ()
    conn.close()
    return res

def get_all_api_id(restricted_only: bool =False):
    conn = sqlite3.connect ('accounts.db')
    cur = conn.cursor ()
    cur.execute (
        '''CREATE TABLE IF NOT EXISTS tg_ac (Name TEXT, API_ID INTEGER PRIMARY KEY NOT NULL, API_HASH TEXT, 
        Phone TEXT, PROXY TEXT, System TEXT, Password TEXT, Restriction TEXT)''')
    if restricted_only:
        cur.execute('''SELECT API_ID FROM tg_ac WHERE Restriction == true''')
    else:
        cur.execute ('''SELECT API_ID FROM tg_ac''')
    res = cur.fetchall ()
    for i in res:
        yield i[0]
    conn.close()

def sql_del_table():
    conn = sqlite3.connect ('accounts.db')
    cur = conn.cursor ()
    cur.execute (
        '''Drop table tg_ac ''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    pass
