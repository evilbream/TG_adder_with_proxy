from telethon import TelegramClient, connection
import TelethonFakeTLS
# now with 2fa support
class Authorisation:
    def __init__(self, name, api_id, api_hash, phone, proxy=None, mtproxy=None, new_mtproxy=None,
                 password=None, device_model: str = None, system_version: str = None, app_version: str = None):
        self.password = password
        self.new_mtproxy = new_mtproxy
        self.proxy = proxy
        self.mtproxy = mtproxy
        self.phone = phone
        self.name = name
        self.api_hash = api_hash
        self.api_id = api_id
        if self.proxy is not None:
            self.client = TelegramClient(self.name, self.api_id, self.api_hash,  proxy=self.proxy, device_model=device_model, system_version=system_version, app_version=app_version)
        elif self.mtproxy is not None:
            self.client = TelegramClient(self.name, self.api_id, self.api_hash, connection=connection.ConnectionTcpMTProxyRandomizedIntermediate, proxy=mtproxy, device_model=device_model, system_version=system_version, app_version=app_version)
        elif self.new_mtproxy is not None:
            self.client = TelegramClient(self.name, self.api_id, self.api_hash, connection=TelethonFakeTLS.ConnectionTcpMTProxyFakeTLS, proxy=new_mtproxy, device_model=device_model, system_version=system_version, app_version=app_version)
        else:
            self.client = TelegramClient (self.name, self.api_id, self.api_hash, device_model=device_model, system_version=system_version, app_version=app_version)

    async def starts(self) -> TelegramClient or None:
        print(f'Starting log in to {self.name}')
        try:
            await self.client.start (self.phone, password=self.password)
            if self.proxy is not None:
                print(f'Successful log in from {self.name} per {self.proxy["addr"]} proxy')
            elif self.mtproxy is not None:
                print(f'Successful log in from {self.name} per {self.mtproxy[0]} proxy')
            else:
                print (f'Successful log in from {self.name} without proxy')
            return self.client
        except Exception as err:
            print(f'Something went wrong, failed to connect to {self.name} cuz {err}')
            return None


if __name__ == '__main__':
    pass

        








