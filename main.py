from telethon import TelegramClient, events, sync
from telethon.tl.types import InputMessagesFilterPhotos
from pathlib import Path
import re
import os
#import logging
#uncomment line below if you need proxy
#import socks

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
API_ID = your_api_id
API_HASH = "your_api_hash"

# Put the chat from which you want to retrieve the multimedia files
CHAT_ALIAS = "Regrambot"

BASE_DIR = Path(__file__).resolve().parent
MEDIA_FOLDER = "media"
MEDIA_DIR = os.path.join(BASE_DIR, MEDIA_FOLDER)

# logging.basicConfig(level=logging.DEBUG)

client = TelegramClient("give_a_session_name",
                        API_ID, API_HASH,
                        # You may want to use proxy to connect to Telegram
                        # proxy=(socks.SOCKS5, 'PROXYHOST',
                        # PORT, 'PROXYUSERNAME', 'PROXYPASSWORD')
                        )
client.start()


p1 = re.compile(r".+\.com/(.+)\?igshid=.+")
p2 = re.compile(r".+\@(.+) \n")

line_break = "\n"
if os.path.exists(MEDIA_DIR):
    answer = input("\n> Media folder has been found. Do you want to delete\
                   it with all its content? [y/(n)]: ").lower()
    while answer not in ("yes", "y", "no", "n", ""):
        answer = input('> You must answer "yes" (y) or "no" (n): ').lower()

    if answer in ("yes", "y"):
        os.system("rm -rf %s" % MEDIA_DIR)
        line_break = ""
        print("\nDeleting media folder")

        os.mkdir(MEDIA_DIR)
        print(f"{line_break}Media folder created\n")
else:
    os.mkdir(MEDIA_DIR)
    print(f"{line_break}Media folder created\n")

messages = client.get_messages(CHAT_ALIAS, None)

for message in messages:
    message_dict = message.to_dict()
    has_photo = message_dict["media"]

    try:
        if has_photo is not None:
            user = re.search("Username: (.*)\n", message.message).group(1)
            # id = message.media.photo.id
            # date = message.media.photo.date.strftime("%Y-%m-%d_%H.%M.%S")
            # filename = f"{user}_{id}_{date}"

            print(f"Downloading media from user [ {user} ]")

            if not os.path.exists(os.path.join(MEDIA_DIR, user)):
                os.mkdir(os.path.join(MEDIA_DIR, user))
            os.chdir(os.path.join(MEDIA_DIR, user))
        else:
            match = p1.search(message_dict["message"])

            if match is None:
                match = p2.search(message_dict["message"])

        message.download_media()

    except AttributeError:
        continue

print("\nAll files has been succesfully downloaded!")
