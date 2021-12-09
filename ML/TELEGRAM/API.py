from telethon import TelegramClient
#from telethon.errors.rpc_errors_401 import SessionPasswordNeededError

# (1) Use your own values here
api_id = '13920592'
api_hash = '8831ea25cb6fb04c05cdb69b20ff074f'

phone = '7499184374'
username = 'mohamadraffel'

# (2) Create the client and connect
client = TelegramClient(username, api_id, api_hash)
client.connect()

# Ensure you're authorized
if not client.is_user_authorized():
    client.send_code_request(phone)
    try:
        client.sign_in(phone, input('Enter the code: '))
    except SessionPasswordNeededError:
        client.sign_in(password=input('Password: '))

me = client.get_me()
print(me)
