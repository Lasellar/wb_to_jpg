import config
from pyrogram import Client, filters
from pyrogram.types import Message
import os
import datetime

from article_process import process

api_id = config.APP_API_ID
api_hash = config.APP_API_HASH
bot_token = config.bot_token

client_bot = Client(
    name='bot_andromeda', api_id=api_id, api_hash=api_hash, bot_token=bot_token
)


@client_bot.on_message(filters.command('start'))
async def start_command(client_object, message: Message):
    await client_bot.send_message(
        chat_id=message.from_user.id,
        text='здарова заебал, э, ты чо, гонишь? скинь артикул',
    )
    print(f'[{datetime.datetime.utcnow()}] {message.from_user.id} '
          f'{message.from_user.username} /start')


@client_bot.on_message()
async def article_processing(client_object, message: Message):
    try:
        print(f'[{datetime.datetime.utcnow()}] -------request: {message.text}---')
        archive_filename = process(message.text)
        print(f'archive {archive_filename}')
        await client_bot.send_document(
            chat_id=message.from_user.id,
            document=archive_filename
        )

        file_path = os.path.join('', f'{archive_filename}')
        os.remove(path=file_path)
        print(f'-------answered {message.from_user.id}---')
    except Exception as exception:
        print(exception)


print(datetime.datetime.utcnow(), client_bot.APP_VERSION)
client_bot.run()
