
import telethon.sync ,TelegramClient
from telethon.tl.functions.messages import SendMessageRequest
import socks



api_id = 26160333
api_hash = '09db56dcd7af268e9199c43395637765'
phone = '+972546047056'
client=TelegramClient( phone, api_id, api_hash, proxy={
   'proxy_type': 'http'
     'url' = 'http://ip.smartproxy.com/json',
    'port': 7000,
    'username': 'hahr83'
    'password': 'xLGjXOu3n40yunbbf1' 
} )


client.start(phone_number)


message = 'Hello from Telegram client!'
client(SendMessageRequest('your_chat_id', message))

...