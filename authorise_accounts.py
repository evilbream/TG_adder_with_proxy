import asyncio
import os

from assist_func import get_csv_len, convert_to_csv, get_txt_len, get_from_csv, divide_proxy
from auth import Authorisation


async def auth(): # default_authorisation nothing new
    if not (os.path.exists('tg_accs.csv')) or (get_csv_len('tg_accs.csv') + 1 < get_txt_len('tg_accs.txt')):
        convert_to_csv('tg_accs.txt', 'tg_accs.csv', 'accounts')
    if not os.path.exists ('proxy.csv') or (get_csv_len('proxy.csv') + 1 < get_txt_len('proxy.txt')):
        convert_to_csv('proxy.txt', 'proxy.csv', 'proxy')
    # authorise all accounts w or without proxy
    prox = input('Do you want to use a proxy? (y/n): ').lower()
    if prox == 'n':
        get_clients = [await (Authorisation(acc[0], acc[1], acc[2], acc[3]).starts()) for acc in get_from_csv('tg_accs.csv', 'accs')]
        clients = [client for client in get_clients if client is not None]
        return clients
    elif prox == 'y':
        # если в скл файле есть хотя бы 1 аккаунт спросить добавить прокси/аки или использовать ранее установленную уонфигурацию

        per_prox_ac = get_csv_len('tg_accs.csv')//get_csv_len('proxy.csv')
        print(f"I'll use {per_prox_ac} ac per one proxy")
        get_clients = [await (Authorisation(acc[0], acc[1], acc[2], acc[3], acc[4]).starts()) for acc in divide_proxy()]
        clients = [client for client in get_clients if client is not None]
        return clients
    else:
        print('u should have typed "y" or "n"')
        return