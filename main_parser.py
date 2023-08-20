import os

from Parser import Parser
import asyncio
from assist_func import add_to_existing_file, convert_to_csv
from account_manager import auth_for_parsing


def what_to_do():
    parser_menu = input ('Choose how to scrape users:\n1. Scrape users only with status Last seen Recently\n2. Parse without any filter'
                         '\n3. Scrape users from comments in the channel\n4. Scrape users, who were online later than '
                         'a certain date\n5. Scrape users, who reacted in the group (by specific emoji or with any '
                         'emoji)\n6. Scrape users, who were online later than a certain date n time\n7. Quit\n - ')
    while parser_menu not in '123456':
        parser_menu = input (
            'Choose how to scrape users:\n1. Scrape users only with status Last seen Recently\n2. Parse without any filter'
            '\n3. Scrape users from comments in the channel\n4. Scrape users, who were online later than '
            'a certain date\n5. Scrape users, who reacted in the group (by specific emoji or with any '
            'emoji)\n6. Scrape users, who were online later than a certain date n time\n7. Quit\n - ')
    return int(parser_menu)


async def extended_parser():
    client = await auth_for_parsing ()
    if client is None:
        return
    if not os.path.exists ('users.csv'):
        open ('users.csv', 'w')
    option = what_to_do()
    if option == 1:
        await parser(client)
    elif option == 2:
        await parser(client, without_filter=True)
    elif option == 3:
        # parse from channel worked
        users = await Parser(client).get_from_comments()
        if users:
            add_to_existing_file (users)
            print ('successfully parsed')
    elif option == 4:
        # parse by specific date
        limit = input ('How many users do u want to parse? Press enter if all (tg limit is 10000 from one group): ')
        if limit.isdigit ():
            limit = int (limit)
            users = await Parser (client).users_by_day_filter (limit=limit)
        else:
            users = await Parser (client).users_by_day_filter ()
        if users:
            add_to_existing_file (users)
            print ('successfully parsed')
    elif option == 5:
        # get users that reacted in chat
        users = await Parser(client).get_user_that_reacted_in_chat()
        if users:
            add_to_existing_file (users)
    elif option == 6:
        users = await Parser (client).users_by_time_filter ()
        if users:
            add_to_existing_file (users)
            print ('successfully parsed')
    elif option == 7:
        return


# fully functional old parser

async def parser(client, without_filter=None):
    limit = input('How many users do u want to parse? Press enter if all (tg limit is 10000 from one group): ')
    if limit.isdigit():
        limit = int(limit)
        if without_filter:
            users = await Parser (client).parse_members (limit=limit, status_filter=None)
        else:
            users = await Parser (client).parse_members (limit=limit)
    else:
        if without_filter:
            users = await Parser(client).parse_members(status_filter=None)
        else:
            users = await Parser(client).parse_members()

    add_to_existing_file(users)
    print('successfully parsed')


asyncio.run(extended_parser())
