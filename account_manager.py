import asyncio

from telethon import TelegramClient

from SQL_support.sql_CRUD import sql_get_account, sql_add_account, sql_del_account, sql_change_proxy, \
    sql_get_acs_credentials, get_all_api_id

from assist_func import clear_csv

async def send_mes(client: TelegramClient) -> TelegramClient or None:
    async with client:
        me = await client.get_me ()
        if me.restricted:
            print(f'Skipping {me.first_name}')
            return None
        else:
            return client

async def auth_accounts(skip_account=False):
    get_clients = []
    for api_id in get_all_api_id():
        get_clients.append(await sql_get_acs_credentials(api_id))
    clients = [client for client in get_clients if client is not None]
    if skip_account is False:
        return clients
    else:
        fresh_clients = []
        for client in clients:
            new_cl = await send_mes(client)
            if new_cl is not None:
                fresh_clients.append(new_cl)
        return fresh_clients



async def auth_for_parsing():
    view_accounts()
    api_id = int(input('Enter the api id of the account from which u wanna parse members: '))
    client =  await sql_get_acs_credentials(api_id)
    if isinstance(client, TelegramClient):
        return client
    else:
        print('This account cant be used')
        return None
#
#eef4359a9b325ff1d1e5084df0e0f7537b6d736e2e636f6d&bot=@mtpro_xyz_bot#US


def add_account():
    add_another = 'y'
    while add_another == 'y':
        name = input('Enter account name: ')
        try:
            api_id = int(input('Enter api_id: '))
        except ValueError:
            print('api_id must be integer')
            api_id = int (input ('Enter api_id: '))
        api_hash = input('Enter api_hash: ')
        phone = input('Enter phone number with country code: ')
        proxy = input("Enter proxy for this account, press enter if u want to use this account without proxy.\n"
                      "Proxy format: proxy_type:addr:port:username:password or MTP:host_name:port:proxy_secret (for "
                      "MTProto Proxies), f.e. 'HTTP:22.92.130.159:8000:JKGGD3:R6KD4t' or "
                      "'MTP:mtproxy.network:8880:secret' (if the proxy has no secret enter 0 instead of secret): ")
        sql_add_account(name, api_id, api_hash, phone, proxy)
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
        ch_another = input ('Do u wanna change another account (y/n)? ').lower ()


async def test_auth():
    test_log = input('Do u wanna log in to all accounts or a specific one for testing (all/specific)? ').lower()
    if test_log == 'all':
        [await sql_get_acs_credentials(api_id) for api_id in get_all_api_id()]
    elif test_log == 'specific':
        api_id = int(input('Enter the api id of the account u wanna log in: '))
        await sql_get_acs_credentials(api_id)
    else:
        print('The command is not recognized')


async def main_menu():
    what_to_do = input('Menu:\n1.Add account\n2.View all accounts\n3.Change proxy'
                       '\n4.Test auth\n5.Delete account\n6.Delete duplicates from parsed users\n7.Quit \n - ')
    while what_to_do != '7':
        if what_to_do == '1':
            add_account()
        elif what_to_do == '2':
            view_accounts()
        elif what_to_do == '3':
            view_accounts()
            change_proxy()
        elif what_to_do == '4':
            await test_auth()
        elif what_to_do == '5':
            view_accounts()
            delete_account()
        elif what_to_do == '6':
            clear_csv()
            print('Duplicates deleted')
        what_to_do = input ('Menu:\n1. Add account\n2.View all accounts\n3.Change proxy'
                            '\n4.Test auth\n5.Delete account\n6.Delete duplicates from parsed users\n7.Quit \n - ')


if __name__ == '__main__':
    asyncio.run(main_menu())

