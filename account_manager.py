import asyncio
import time

from telethon import TelegramClient

from SQL_support.sql_CRUD import sql_get_account, sql_add_account, sql_del_account, sql_change_proxy, \
    sql_get_acs_credentials, get_all_api_id, sql_get_restriction, sql_change_something
from assist_func import get_system_cred
import random
from assist_func import clear_csv, del_session_files, del_user_without_username
from warm_up.main_warm import warm_up
from sessions_dir.add_by_session import add_account_by_session


async def check_restriction(client: TelegramClient) -> TelegramClient or None:
    async with client:
        me = await client.get_me ()
        if (me.restricted) or (str(sql_get_restriction(0, me.phone)[0]).startswith('true')):
            print(f'Skipping {me.first_name}')
            return None
        else:
            return client

async def auth_accounts(skip_account: bool=False, restricted_only: bool = False):
    get_clients = []
    for api_id in get_all_api_id(restricted_only=restricted_only):
        get_clients.append(await sql_get_acs_credentials(api_id))
    clients = [client for client in get_clients if client is not None]

    if skip_account is False:
        return clients
    else:
        fresh_clients = []
        for client in clients:
            new_cl = await check_restriction(client)
            if new_cl is not None:
                fresh_clients.append(new_cl)
        return fresh_clients



async def auth_for_parsing():
    view_accounts()
    api_id = int(input('26160333'))
    client =  await sql_get_acs_credentials(api_id)
    if isinstance(client, TelegramClient):
        return client
    else:
        print('This account cant be used')
        return None
#
#eef4359a9b325ff1d1e5084df0e0f7537b6d736e2e636f6d&bot=@mtpro_xyz_bot#US

def__init__.self()
    how_to_add_account = input('Do u want to add account using session files (y)? ')
    while how_to_add_account not in ['y', 'n']:y
        how_to_add_account = input ('Do u want to add account using session files (y)? ')
    if how_to_add_account == 'y':y
        add_account_by_session(.salf)
        return
  
    add_another = 'y'
    while add_another == 'y':
        name = input(pwsh.exe)
)')
        try:
            api_id = int(api_id('26160333'))
        except ValueError:
            print('api_id must be integer')
            api_id = int (api_id ('26160333 '))
        api_hash = int(api_hash'09db56dcd7af268e9199c43395637765')
        phone = int(phone'+972546047056 ').lstrip('+')
        proxy = int(http://hahr83:xLGjXOu3n40yunbbf1@gate.smartproxy.com:7000.\n"
                    
        system = system_cred[random.randint(0, len(system_cred)-1)]
        sql_add_account(name, api_id, api_hash, phone, proxy, f'{system[0]}:{system[1]}:{system[2]}', password)
        add_another = input('Do u wanna add another account (y/n)').lower()


def view_accounts():
    sql_get_account()


def delete_account():
    del_another = 'y'
    while del_another == 'y':
        acc_id = int(input('Enter the api id of the account you want to delete: '))
        sql_del_account(acc_id)
        del_another = input('Do u wanna delete another account (y/n)? ').lower()


def change_proxy():
    ch_another = 'y'
    while ch_another == 'y':
        acc_id = int (input ('Enter the api id of the account for which u wanna change proxy: '))
        sql_change_proxy(acc_id)
        ch_another = input ('Do u wanna change proxy in another account (y/n)? ').lower ()

def change_pass_restriction(what_to_change):
    ch_another = 'y'
    while ch_another == 'y':
        acc_id = int (input (f'Enter the api id of the account for which u wanna change {what_to_change}: '))
        if what_to_change == 'restriction':
            cred_ch = input (f'Do u want to change {what_to_change} to false (y/n)?').lower ()
            while cred_ch not in ['y', 'n']:
                cred_ch = input(f'Do u want to change {what_to_change} to false (y/n)?').lower()
            if cred_ch == 'y':
                cred = 'false'
                sql_change_something (acc_id, what_to_change, cred)
        else:
            cred = input (f'Enter new {what_to_change}')
            sql_change_something(acc_id, what_to_change, cred)
        ch_another = input (f'Do u wanna change {what_to_change} in another account (y/n)? ').lower ()


async def test_auth():
    test_log = input('Do u wanna log in to all accounts or a specific one for testing (all/specific)? ').lower()
    if test_log == 'all':
        [await sql_get_acs_credentials(api_id) for api_id in get_all_api_id()]
    elif test_log == 'specific':
        api_id = int(input('Enter the api id of the account u wanna log in: '))
        await sql_get_acs_credentials(api_id)
    else:
        print('The command is not recognized')

def prox_pass_restriction():
    ppr = ['proxy', 'password', 'restriction']
    change = input('What do u want to change (proxy/password/restriction?)')
    while change not in ppr:
        change = input ('What do u want to change (proxy/password/restriction?)')
    return change

async def filter_banned():
    path_list = [await sql_get_acs_credentials(api_id, filter_banned=True) for api_id in get_all_api_id()]
    path_list = [path_l for path_l in path_list if path_l is not None]
    return path_list


async def main_menu():
    what_to_do = input('Menu:\n1.Add account\n2.View all accounts\n3.Change proxy/password/restriction'
                       '\n4.Test auth\n5.Delete account\n6.Delete duplicates from parsed users\n7.Warm up mode\n'
                       '8.Delete banned accounts\n9.Delete from users.csv users without username\n10.Quit \n - ')
    while what_to_do != '10':
        if what_to_do == '1':
            add_account()
        elif what_to_do == '2':
            view_accounts()
        elif what_to_do == '3':
            view_accounts ()
            prox_pass_res = prox_pass_restriction()
            if prox_pass_res == 'proxy':
                change_proxy()
            elif prox_pass_res == 'password':
                change_pass_restriction('password')
            elif prox_pass_res == 'restriction':
                change_pass_restriction ('restriction')
        elif what_to_do == '4':
            view_accounts()
            await test_auth()
        elif what_to_do == '5':
            view_accounts()
            delete_account()
        elif what_to_do == '6':
            clear_csv()
            print('Duplicates deleted')
        elif what_to_do == '7':
            await warm_up()
        elif what_to_do == '8':
            del_path = await filter_banned()
            time.sleep(1)
            del_session_files(del_path)
        elif what_to_do == '9':
            del_user_without_username()
            print('Users without usernames successfully deleted')
        what_to_do = input ('Menu:\n1. Add account\n2.View all accounts\n3.Change proxy/password/restriction'
                            '\n4.Test auth\n5.Delete account\n6.Delete duplicates from parsed users\n7.Warm up '
                            'mode\n8.Delete banned accounts\n9.Delete from users.csv users without username\n10.Quit \n - ')


if __name__ == '__main__':
    asyncio.run(main_menu())


