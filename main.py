import os
import requests
import shutil
import random
import telegram
from dotenv import load_dotenv


def get_comic(random_number_comic):
    comic_url = f'https://xkcd.com/{random_number_comic}/info.0.json'
    response = requests.get(comic_url)
    response.raise_for_status()
    comic = response.json()
    comic_url = comic['img']
    comic_comment = comic['alt']
    return comic_url, comic_comment


def save_comic(comic_url, folder_name, random_number_comic):
    response = requests.get(comic_url)
    response.raise_for_status()
    with open(os.path.join(folder_name, f'comic_{random_number_comic}.png'), 'wb') as file:
        file.write(response.content)


def publish_comic(bot, chat_id, folder_name, comic_comment, random_number_comic):
    with open(os.path.join(folder_name, f'comic_{random_number_comic}.png'), 'rb') as document:
        bot.send_document(chat_id=chat_id, document=document, caption=comic_comment)


def main():
    load_dotenv()
    folder_name = 'images'
    max_comic_number = 2700
    random_number_comic = random.randint(1, max_comic_number)
    chat_id = os.environ['TG_CHAT_ID']
    bot = telegram.Bot(token=os.environ['TG_TOKEN'])

    try:
        os.makedirs(folder_name, exist_ok=True)
        comic_url, comic_comment = get_comic(random_number_comic)
        save_comic(comic_url, folder_name, random_number_comic)
        publish_comic(bot, chat_id, folder_name, comic_comment, random_number_comic)
    finally:
        shutil.rmtree(folder_name)


if __name__ == '__main__':
    main()
