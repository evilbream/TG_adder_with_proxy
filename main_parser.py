import os

from Parser import Parser
import asyncio
from assist_func import add_to_existing_file, convert_to_csv


async def parser():
    if not os.path.exists('tg_accs.csv'):
        convert_to_csv('tg_accs.txt', 'tg_accs.csv', 'accounts')
    if not os.path.exists ('proxy.csv'):
        convert_to_csv('proxy.txt', 'proxy.csv', 'accounts')
    if not os.path.exists('users.csv'):
        open('users.csv', 'w')
    limit = input('How many users do u want to parse? Press enter if all (tg limit is 10000 from one group): ')
    if limit.isdigit():
        limit = int(limit)
        users = await Parser().parse_members (limit=limit)
    else:
        users = await Parser().parse_members()

    add_to_existing_file(users)
    print('successfully parsed')


asyncio.run(parser())