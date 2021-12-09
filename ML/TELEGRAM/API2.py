from telethon.sync import TelegramClient


from telethon.sync import TelegramClient
api_id = 13920592
api_hash = '8831ea25cb6fb04c05cdb69b20ff074f'
phone = '+917499184374'
client = TelegramClient(phone, api_id, api_hash)


client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))


from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)