import json
import os
import random
import time
from dataclasses import dataclass
from SQL_support.sql_CRUD import sql_get_restriction, sql_add_account

# одинаковые апи ид добавлять 0 при добавлении или рандомный символ
@dataclass
class Add_by_session:
    js_dict: dict
    proxy: str = '' # no proxy by default

    def get_name(self):
        name = self.js_dict['session_file']
        return os.path.join ('sessions_dir', f'{name}.session')

    @staticmethod
    def test_if_in_database(phone):  # returned True if this account not in database
        res = sql_get_restriction (0, phone=phone)  # using restriction to test accounts in bd
        if res is None:
            return True
        return False

    def get_system(self):
        return f'{self.js_dict["device"]}:{self.js_dict["sdk"]}:{self.js_dict["app_version"]}'

    def start(self):
        new = self.test_if_in_database(self.js_dict['phone'])
        if new:
            name = self.get_name()
            system = self.get_system()
            print(name)
            app_id = str(random.randint(10000, 99999)) + '00000' + str(self.js_dict['app_id'])
            try:
                sql_add_account(name, api_id=int(app_id),
                                api_hash=self.js_dict['app_hash'], phone=self.js_dict['phone'],
                                proxy=self.proxy, password=self.js_dict['twoFA'], system=system)
                print(f'{self.js_dict["session_file"]} was successfully added to db')
            except Exception as err:
                print(f'Something went frong {err}')



def add_account_by_session():
    proxy_use = input('Do u want to use one proxy for all new accounts (y/n)?: ').lower()
    while proxy_use not in ['y', 'n']:
        proxy_use = input ('Do u want to use one proxy for all new accounts (y/n)?: ').lower ()
    if proxy_use == 'y':
        session_auth()
    else: # every time ask about proxy
        session_auth(one_proxy_for_all=False)


def get_credentials_from_json(js_filepath: str):
    with open (js_filepath , 'r') as f:
        lines = f.readlines ()
    js_session = json.loads (lines[0])
    return js_session


def get_session_list(): #returned path to js file
    session_list = {}
    for file in os.listdir ('sessions_dir'):
        if file.endswith ('.json'):
            try:
                session_list[os.path.join ('sessions_dir', file)] = 0
            except KeyError:
                pass
    for i in session_list.keys ():
        yield i


def session_auth(one_proxy_for_all=True):
    if one_proxy_for_all:
        proxy = input ("Enter proxy for this account, press enter if u want to use this account without proxy.\n"
                       "Proxy format: proxy_type:addr:port:username:password or MTP:host_name:port:proxy_secret (for "
                       "MTProto Proxies), f.e. 'HTTP:22.92.130.159:8000:JKGGD3:R6KD4t' or "
                       "'MTP:mtproxy.network:8880:secret' (if the proxy has no secret enter 0 instead of secret): ")
        for session in get_session_list(): # add account to db one by one
            js_dict = get_credentials_from_json(session) # returned js dictionary converted to py
            print(js_dict)
            Add_by_session(js_dict, proxy).start()
            continue
    else:
        for session in get_session_list(): # add account to db one by one
            js_dict = get_credentials_from_json(session) # returned js dictionary converted to py
            proxy = input ("Enter proxy for this account, press enter if u want to use this account without proxy.\n"
                           "Proxy format: proxy_type:addr:port:username:password or MTP:host_name:port:proxy_secret (for "
                           "MTProto Proxies), f.e. 'HTTP:22.92.130.159:8000:JKGGD3:R6KD4t' or "
                           "'MTP:mtproxy.network:8880:secret' (if the proxy has no secret enter 0 instead of secret): ")
            Add_by_session(js_dict, proxy).start()
            continue

