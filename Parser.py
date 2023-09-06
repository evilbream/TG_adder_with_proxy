import re
import typing
import csv
from telethon.tl.types import ChannelParticipantsRecent, ChannelParticipantsAdmins, ChannelParticipantCreator, \
    ChannelParticipantAdmin
from telethon import TelegramClient
import members_filter
import asyncio
from assist_func import get_from_csv


class Parser:
    def __init__(self, client):
        self.client = client

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


    async def test_parse(self, limit=None):
        group_id = await self.get_dialogs ()
        async with self.client:
            async for user in self.client.iter_participants(group_id, limit=limit):
                print(user.status)

    # remove bots + filter by name
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
                if (user.bot) or (isinstance(user.participant, ChannelParticipantCreator)) or (isinstance(user.participant, ChannelParticipantAdmin)) or (user_filter.exclude()): #исключить в имени или фамилии
                    continue
                users.append((user.id, user.first_name, user.username, user.access_hash))
        return users

    async def get_channels(self) -> int:
        async with self.client:
            dialogs = {}
            n = 1
            async for dialog in self.client.iter_dialogs ():
                if dialog.is_channel:
                    dialogs[n] = (dialog.name, dialog.id)
                    n += 1

        for k, v in dialogs.items ():
            print (k, v[0])
        dialog_num = input ('Choose group from which parsing will be done: ')
        while not dialog_num.isdigit ():
            dialog_num = input ('Choose group from which parsing will be done (digit): ')
        return int (dialogs[int (dialog_num)][1])

    # parse from chanel
    async def get_from_comments(self):
        chanel_id = await self.get_channels()
        async with self.client:
            # parse all chats where comments are opened
            rev = False  # reverse message iteration
            mes_count = input ('How many posts do you want to get a users from? If all - press enter: ')
            while not (mes_count.isdigit ()) or mes_count == '':
                mes_count = input ('How many posts do you want to get a users from (digit or enter):')
            if mes_count == '':
                mes_count = False
            else:
                mes_count = int (mes_count)
            reverse = input ('Do you want to parse from oldest mes to newest (y/n?): ').lower ()
            if reverse == 'y':
                rev = True
            entity = await self.client.get_entity (int (chanel_id))

            user_list = []
            i = 0
            async for mes in self.client.iter_messages (entity, limit=mes_count, reverse=rev):
                if (mes.replies is not None) and (mes.replies.comments):
                    try:
                        async for reply in self.client.iter_messages (entity, reply_to=mes.id):
                            user = await self.client.get_entity (reply.from_id)
                            if (user.bot) or (isinstance(user.participant, ChannelParticipantCreator)) or (isinstance(user.participant, ChannelParticipantAdmin)):
                                pass
                            else:
                                user_list.append ((user.id, user.first_name, user.username, user.access_hash))
                        i += 1
                        print (f'Users parsed from {i} post(s)')
                    except Exception as err:
                        pass
                else:
                    print ('This post doesnt have comments')
            return user_list

        # parse by specific date

    # filter by the time user was online
    # this filter would be working if user dont hide his online status.
    # Enter date after which u want to get user
    # completed filter
    # worked
    async def users_by_day_filter(self, limit=None):
        user_list = []
        group_id = await self.get_dialogs()
        date = input ('Enter the date no earlier than when the user should have been online. F.e: 2023:08:19: ')
        pattern = re.compile (r'\d\d\d\d:\d\d:\d\d')
        res = pattern.match (date)
        while res is None:
            print ('Unsupported date format try again')
            date = input ('Enter the date no earlier than when the user should have been online. F.e: 2023:08:19: ')

        date = [i.lstrip ('0') for i in date.split (':')]

        async with self.client:
            entity = await self.client.get_entity (int (group_id))
            async for user in self.client.iter_participants (entity, limit=limit):
                try:
                    if (user.status.was_online.year >= int (date[0])) and (
                            user.status.was_online.month >= int (date[1])) and (
                            user.status.was_online.day >= int (date[2])):
                        if (user.bot) or (isinstance(user.participant, ChannelParticipantCreator)) or (isinstance(user.participant, ChannelParticipantAdmin)):
                            pass
                        else:
                            user_list.append ((user.id, user.first_name, user.username, user.access_hash))
                except AttributeError:
                    pass
        return user_list


    async def users_by_time_filter(self, limit=None):
        user_list = []
        group_id = await self.get_dialogs()
        date = input ('Enter the date and time in 24 hours format no earlier than when the user should have been online. F.e: 2023:08:19:12:20 ')
        pattern = re.compile (r'\d\d\d\d:\d\d:\d\d:\d\d:\d\d')
        res = pattern.match (date)
        while res is None:
            print ('Unsupported date format try again')
            date = input ('Enter the date and time in 24 hours format no earlier than when the user should have been online. F.e: 2023:08:19:12:20 ')

        date = [i.lstrip ('0') for i in date.split (':')]


        async with self.client:
            entity = await self.client.get_entity (int (group_id))
            async for user in self.client.iter_participants (entity, limit=limit):
                try:
                    if (user.status.was_online.year >= int (date[0])) and (
                            user.status.was_online.month >= int (date[1])) and (
                            user.status.was_online.day >= int (date[2])) and (
                            user.status.was_online.hour >= int (date[3])) and (
                            user.status.was_online.minute >= int (date[4])):
                        if (user.bot) or (isinstance(user.participant, ChannelParticipantCreator)) or (isinstance(user.participant, ChannelParticipantAdmin)):
                            pass
                        else:
                            print(user.status)
                            user_list.append ((user.id, user.first_name, user.username, user.access_hash))
                except AttributeError:
                    pass
        return user_list

    # untested
    async def get_user_that_reacted_in_chat(self):
        group_id = await self.get_dialogs()
        rev = False  # reverse message iteration
        mes_count = input ('How many messages do you want to get a reaction from. If all - press enter: ')
        while not (mes_count.isdigit ()) or mes_count == '':
            mes_count = input ('How many messages do you want to get a reaction from (digit or enter):')
        if mes_count == '':
            mes_count = False
        else:
            mes_count = int (mes_count)
        reverse = input ('Do you want to parse from oldest mes to newest (y/n?): ').lower ()
        if reverse == 'y':
            rev = True
        reaction = input ('Select a reaction to get the users who reacted. F.e: 🔥 (if all - press enter): ')
        # client methods
        async with self.client:
            i = 0
            entity = await self.client.get_entity (int (group_id))
            async for user in self.client.iter_participants (entity):
                if str (i).endswith ('000'):
                    print (f'Pls wait skimmed over users ({i // 100} %)...')
                user = user.id
                i += 1
            user_dict = {}
            reacted_list = []
            async for mes in self.client.iter_messages (entity, limit=mes_count, reverse=rev):
                if (mes.reactions is not None) and (mes.reactions.recent_reactions):
                    if reaction == '':
                        reacted_list = await self.get_reacted_users (mes, user_dict)
                    else:
                        reacted_list = await self.get_reacted_users (mes, user_dict, reaction)
            if reacted_list:
                print ('Successfully parsed')
                return reacted_list
            else:
                print ('Sorry, but no one met given criteria')

    # for reaction processing with get_user_that_reacted_in_chat
    async def get_reacted_users(self, mes, user_dict, reaction=None):
        for i in mes.reactions.recent_reactions:
            try:
                if reaction is None:
                    user = await self.client.get_entity (i.peer_id.user_id)  # get user by id (entity)
                    if (user.bot) or (isinstance(user.participant, ChannelParticipantCreator)) or (isinstance(user.participant, ChannelParticipantAdmin)):
                        pass
                    else:
                        try:
                            user_dict[user.id] = (user.first_name, user.username, user.access_hash)
                        except KeyError:
                            pass
                else:
                    reaction_in_mes = i.reaction.emoticon  # get emotion in reply
                    if reaction_in_mes == reaction:
                        user = await self.client.get_entity (i.peer_id.user_id)  # get user by id (entity)
                        print (i)  # delete
                        if (user.bot) or (isinstance(user.participant, ChannelParticipantCreator)) or (isinstance(user.participant, ChannelParticipantAdmin)):
                            pass
                        else:
                            try:
                                user_dict[user.id] = (user.first_name, user.username, user.access_hash)
                            except KeyError:
                                pass
            except Exception as err:
                if str (err).startswith ('Could not find the input entity for PeerUser'):
                    print (str (err).split ('.')[0])
                else:
                    print (err)
                continue

        return ([(k, v[0], v[1], v[2]) for k, v in user_dict.items ()])




if __name__ == '__main__':
    pass
