import asyncio
from SQL_support.sql_CRUD import get_all_api_id, sql_get_acs_credentials
from warm_up.asist_warm import WARM_UP


async def auth_accounts(restricted_only: bool = False):
    get_clients = []
    for api_id in get_all_api_id(restricted_only=restricted_only):
        get_clients.append(await sql_get_acs_credentials(api_id))
    clients = [client for client in get_clients if client is not None]

    return clients


def get_time_channels():
    times = input('Enter the time in minutes for which you want to run the warm-up mode: ')
    while not times.isdigit():
        times = input ('Enter the time in minutes for which you want to run the warm-up mode: ')
    forwarding_chanel = input('Enter link to the chat from which forwarding will take place: ')
    fake_chanel = input('Enter link to the chat in which accounts will communicate among themself: ')
    use_restricted = input('Do u want to use only restricted accounts (y/n)? ').lower()
    while use_restricted not in ['y', 'n']:
        use_restricted = input ('Do u want to use only restricted accounts (y/n)? ').lower ()
    if use_restricted == 'y':
        use_restricted = True
    else:
        use_restricted = False
    private = input('Do you want the accounts to communicate among themselves in private chats (y/n)? ').lower()
    while private not in ['y', 'n']:
        private = input ('Do you want the accounts to communicate among themselves in private chats (y/n)? ').lower ()
    if private == 'y':
        private= True
    else:
        private = False
    return int(times) * 60, forwarding_chanel, fake_chanel, use_restricted, private


async def get_username(client):
    async with client:
        me = await client.get_me()
        return me.username


async def warm_up():
    times, forwarding_chanel, fake_chanel, use_restricted, private = get_time_channels()
    private = True
    if private:
        clients = await auth_accounts (restricted_only=use_restricted)
        # start warm up after obtaining clients
        user_list = await asyncio.gather(*[get_username(cl) for cl in clients])
        user_list = [ i for i in user_list]
        if len(user_list) < 1:
            print('For private chatting among accounts add more then one account')
            return
        await asyncio.gather(*[WARM_UP(cl, forwarding_chanel, fake_chanel, user_list).start(times) for cl in clients], return_exceptions=True)

    else:
        clients = await auth_accounts(restricted_only=use_restricted)
        await asyncio.gather (
            *[WARM_UP (cl, forwarding_chanel, fake_chanel, []).start (times) for cl in clients],
            return_exceptions=True)
