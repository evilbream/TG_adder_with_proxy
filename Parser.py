import typing
import csv
from telethon.tl.types import ChannelParticipantsRecent, ChannelParticipantsAdmins
from telethon import TelegramClient
import members_filter
import asyncio
from assist_func import get_from_csv


class Parser:
    def __init__(self, client):
        self.client = client
        #NAME, API_ID, API_HASH = self.get_client () if no client
        #self.client = TelegramClient (NAME, API_ID, API_HASH)

    @staticmethod # unused method
    def get_client() -> typing.Tuple:
        client_dict = {}
        n_client = 1
        for cl in get_from_csv ('tg_accs.csv', 'accs'):
            client_dict[n_client] = cl
            n_client += 1
        for k, v in client_dict.items ():
            print (k, v[0])
        acc_num = input ('Choose account from which parsing will be done: ')
        while not acc_num.isdigit ():
            acc_num = input ('Choose account from which parsing will be done (digit): ')
        return client_dict[int (acc_num)][:3]

    async def get_dialogs(self) -> int:
        async with self.client:
            dialogs = {}
            n = 1
            async for dialog in self.client.iter_dialogs():
                if dialog.is_group:
                    dialogs[n] = (dialog.name, dialog.id)
                    n += 1
                else:
                    pass

        for k, v in dialogs.items ():
            print (k, v[0])
        dialog_num = input ('Choose group from which parsing will be done: ')
        while not dialog_num.isdigit ():
            dialog_num = input ('Choose group from which parsing will be done (digit): ')
        return int(dialogs[int (dialog_num)][1])

    async def parse_members(self, limit=None, status_filter=ChannelParticipantsRecent()) -> typing.List:
        try:
            group_id = await self.get_dialogs()
        except KeyError:
            print('Try again, this number wasnt in list')
            group_id = await self.get_dialogs ()

        users = []

        async with self.client:
            async for user in self.client.iter_participants(group_id, limit=limit, filter=status_filter):
                user_filter = members_filter.Member_filter (user)
                if user.bot or user_filter.exclude(): #исключить в имени или фамилии
                    continue
                users.append((user.id, user.first_name, user.username, user.access_hash))
        return users


if __name__ == '__main__':
    pass
