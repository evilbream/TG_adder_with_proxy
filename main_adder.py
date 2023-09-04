import logging
import asyncio
import os
import typing

from telethon import events

from auth import Authorisation
from assist_func import get_csv_len, get_from_csv, divide_proxy, convert_to_csv, get_txt_len
# from authorise_accounts import auth  the old method no longer works
from account_manager import auth_accounts
from addingUsers import Add_user
from assist_func import split_ac
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


async def join_groups(clients: typing.List, group_link: str):
    join_group = [Add_user (cl).join_group (group_link) for cl in clients]
    res = await asyncio.gather (*join_group)
    while False in res:
        group_link = input ('Enter group link without @, like "group_link" or "https://t.me/group_link": ')
        join_group = [Add_user (cl).join_group (group_link) for cl in clients]
        res = await asyncio.gather (*join_group)
    return group_link


async def main_adder():
    # clients = await auth() - old method
    skip_account = input('Do u wannna automatically skip account if it have some restriction (may cause errors) (y/n)? ').lower()
    if skip_account == 'y':
        clients = await auth_accounts(skip_account=True)
    else:
        clients = await auth_accounts ()
    # join group to which to add users
    if clients:
        group_link = input('Enter group name to which to add users without @, like "group_link" or "https://t.me/group_link": ')
        await join_groups(clients, group_link)  # join group
    else:
        print("None of ur account's can be used")
        return

    # choose how to add users to group and add users to group
    client_num = len(clients)
    how_to_add, user_num = hows_to_add()
    # split csv
    try:
        split_ac(client_num, int(user_num))
    except TypeError:
        print('it seems there are not enough users in users.csv file. Try add more users in it or reduce the number '
              'of accounts or users via ac')
        return

    # adding to group
    add_user_objects = [Add_user(cl) for cl in clients]
    if how_to_add == 'id':
        how_to_act = get_by_id()
        if how_to_act == 'y':
            show_groups = [obj.meet_all_groups () for obj in add_user_objects[1:]]
            show_groups.append (add_user_objects[0].meet_all_groups (show_dict=True))
            res = await asyncio.gather (*show_groups)
            group_id = choose_dialog(res[-1])
            await asyncio.gather(*[cl.meet_users(group_id) for cl in add_user_objects])
            num = 0
            client_list = []
            for client in clients:
                client_list.append (Add_user (client).add_via_id(f'users{num}.csv', group_link))
                num += 1
            await asyncio.gather(*client_list, return_exceptions=True)

        else:
            group_lin = await join_groups(clients, how_to_act)  # join group from which users were parsed, link returned
            await asyncio.gather (*[cl.meet_users (group_lin) for cl in add_user_objects])
            num = 0
            client_list = []
            for client in clients:
                client_list.append (Add_user (client).add_via_id (f'users{num}.csv', group_link))
                num += 1
            await asyncio.gather (*client_list, return_exceptions=True)

    elif how_to_add == 'username':
        num = 0
        client_list = []
        for client in clients:
            client_list.append(Add_user(client).add_via_username(f'users{num}.csv', group_link))
            num += 1

        await asyncio.gather (*client_list, return_exceptions=True)


def choose_dialog(dialog_dict: typing.Dict) -> int:
    for k, v in dialog_dict.items ():
        print (k, v[1])
    ch_num = input('Choose num of the group from which users were parsed: ')
    while not ch_num.isdigit():
        ch_num = input ('Choose number of the group from which users were parsed (digit): ')
    return dialog_dict[int(ch_num)][0]


def get_by_id() -> str:
    is_joined = input("Are all the accounts from which the adding will take place joined the group from where "
                      "the users were parsed (y/n)?\n - ").lower()
    while not ((is_joined == 'y') or (is_joined == 'n')):
        is_joined = input ("Are all the accounts from which the adding will take place joined the group from where "
                           "the users were parsed (y/n)?\n - ").lower()

    if is_joined == 'n':
        group_link = input ('Enter group link from which users were parsed without @, like "group_link" or '
                            '"https://t.me/group_link": ')
        return group_link
    else:
        return is_joined


def hows_to_add():
    print ("WARNING: U can't add via ID user or interact with chat through id your current session hasn’t met yet."
           "That's why more errors may occur and additional actions would be required, when adding by id")
    how_to_add = input ("Do u want to add users via id or username (id/username)?\n - ")
    while not ((how_to_add == 'id') or (how_to_add == 'username')):
        how_to_add = input ("Do u want to add users via id or username? Type 'id' or 'username'\n - ")
    users_num = input("How many users do u want to add via one account? Recommended: 60 or less\n - ")
    while not users_num.isdigit():
        users_num = input ("How many users do u want to add via one account? Recommended: 60 or less. Pls type the digit\n - ")

    return how_to_add, users_num


def choose_proxy_type():
    print('Choose proxy type to use: ')
    proxy_type = input('1. mtproxy\n2. HTTP/HTTPS/SOCKS\n')
    while not ((proxy_type == '1') or (proxy_type == '2')):
        proxy_type = input ('1. mtproxy\n2. HTTP/HTTPS/SOCKS\n')
    return proxy_type

asyncio.run(main_adder())





