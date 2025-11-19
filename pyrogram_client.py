# pyrogram_client.py - initializes a Pyrogram Client for additional features
from pyrogram import Client
from config import API_ID, API_HASH, TOKEN
# create a user client session file 'user_session'
user_client = Client('user_session', api_id=API_ID, api_hash=API_HASH)
# You may use user_client to perform actions that bot API cannot (if needed).
# Example usage in other modules:
# with user_client: user_client.send_message(chat_id, 'hello from user client')
