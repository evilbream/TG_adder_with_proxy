import os

from Parser import Parser
import asyncio
from assist_func import add_to_existing_file, convert_to_csv
from account_manager import auth_for_parsing

async def parser():
    client = await auth_for_parsing()
    if client is None:
        return
    if not os.path.exists('users.csv'):
        open('users.csv', 'w')
    limit = input('How many users do u want to parse? Press enter if all (tg limit is 10000 from one group): ')
    if limit.isdigit():
        limit = int(limit)
        users = await Parser(client).parse_members (limit=limit)
    else:
        users = await Parser(client).parse_members()

    add_to_existing_file(users)
    print('successfully parsed')


asyncio.run(parser())
