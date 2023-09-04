import asyncio
import random
import typing
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.tl.types import InputChannel, InputUser
from telethon import errors
from SQL_support.sql_CRUD import sql_change_something

from assist_func import get_from_csv


class Add_user:
    def __init__(self, client: TelegramClient):
        self.client = client

    async def join_group(self, group_link: str) -> bool:
        if group_link.startswith('https://t.me/'):
            self.group_link = group_link
        else:
            self.group_link = 'https://t.me/' + group_link
        async with self.client:
            try:
                group = await self.client.get_entity (self.group_link)
                await self.client (JoinChannelRequest (group))
                name = await self.client.get_entity('me')
                print(f'{name.first_name} successfully joined {self.group_link}')
                return True
            except Exception as err:
                if err is ValueError:
                    print("group with this username doesn't seem to exist")
                    return False
                else:
                    print(f'Something went wrong {err}')
                    return False

    async def meet_all_groups(self, show_dict=False) -> typing.Dict:
        chat_dict = {}
        num = 1
        async with self.client:
            async for dialog in self.client.iter_dialogs():
                df = dialog.id
                if show_dict:
                    if dialog.is_group:
                        chat_dict[num] = (dialog.id, dialog.name)
                        num += 1
            return chat_dict

    async def meet_users(self, group_id):
        user_list = []
        n = 1
        async with self.client:
            print(f'Skim over users, pls wait...')
            async for user in self.client.iter_participants(group_id):
                user_list.append((user.id, user.access_hash, user.first_name))
                n += 1
                if str(n).endswith('00'):
                    print(f'skimmed through {n} users')

    async def add_via_id(self, filename: str, group_link: str):
        async with self.client:
            me = await self.client.get_entity('me')
            group = await self.client.get_entity (group_link)
            chat = InputChannel (group.id, group.access_hash)
            for user_info in get_from_csv (filename, 'users'):
                users = await self.client.get_entity (int(user_info[0]))
                user = InputUser (user_id=users.id, access_hash=users.access_hash)
                try:
                    me = await self.client.get_entity ('me')
                    print (f'adding {user_info[1]} by {me.first_name}')
                    await self.client (InviteToChannelRequest (chat, [user]))
                    await asyncio.sleep (random.uniform (2, 7))
                except errors.PeerFloodError:
                    print('Flood error')
                    try:
                        sql_change_something(me.id, 'restriction', 'true')
                    except Exception as err:
                        print(f'Probable have some problem with database {err}')
                    break
                except errors.UserPrivacyRestrictedError:
                    print (f"can't add {user_info[1]} due to the user privacy setting")
                    continue
                except errors.UserNotMutualContactError:
                    print('User probably was in this group early, but leave it')
                    continue
                except errors.UserChannelsTooMuchError:
                    print(f'{user_info[1]} is already in too many channels/supergroups.')
                    continue
                except errors.UserKickedError:
                    print(f'{user_info[1]} was kicked from this supergroup/channel')
                except Exception as err:
                    print(err)
                    break

    async def add_via_username(self, filename: str, group_link: str):
        if group_link.startswith('https://t.me/'):
            self.group_link = group_link
        else:
            self.group_link = 'https://t.me/' + group_link
        async with self.client:
            me = await self.client.get_entity ('me')
            group = await self.client.get_entity (self.group_link)
            chat = InputChannel (group.id, group.access_hash)
            for user_info in get_from_csv (filename, 'users'):
                if user_info[2] != '':
                    user = await self.client.get_entity(user_info[2])
                else:
                    print(f"User with id {user_info[0]} doesn't have username")
                    continue
                user = InputUser (user_id=user.id, access_hash=user.access_hash)
                try:
                    await asyncio.sleep (random.uniform (2, 7))
                    me = await self.client.get_entity('me')
                    print (f'adding {user_info[2]} by {me.first_name}')
                    await self.client (InviteToChannelRequest (chat, [user]))
                except errors.PeerFloodError:
                    print (f'Flood error, try {me.username} this account later')
                    try:
                        sql_change_something (me.id, 'restriction', 'true')
                    except Exception as err:
                        print(f'Have some problem with database {err}')
                    break
                except errors.UserPrivacyRestrictedError:
                    print (f"Can't add {user_info[2]} due to users privacy setting")
                    continue
                except errors.UserNotMutualContactError:
                    print (f'{user_info[2]}  is not a mutual contact')
                    continue
                except errors.UserChannelsTooMuchError:
                    print(f'{user_info[1]} is already in too many channels/supergroups.')
                    continue
                except errors.UserKickedError:
                    print(f'{user_info[2]} was kicked from this supergroup/channel')
                except errors.UserBannedInChannelError:
                    print(f'{user_info[2]} was banned from sending messages in supergroups/channels')
                    try:
                        sql_change_something (me.id, 'restriction', 'true')
                    except Exception as err:
                        print (f'Have some problem with database {err}')
                    break
                except Exception as err:
                    print (err)
                    break


