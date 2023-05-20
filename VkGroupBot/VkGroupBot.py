import os
import vk_api
import requests
import random
import uuid
import time
import schedule
import datetime


class MyVkBot:
    def __init__(self, token):
        self.vk_session = vk_api.VkApi(token=token, api_version='5.131')
        self.vk = self.vk_session.get_api()
        self.http = requests.Session()
        # Сохраняем время последней отправки сообщения
        self.last_message_time = datetime.datetime.now() - datetime.timedelta(hours=6)

    def story(self, file, file_type, add_to_news=True, user_ids=None,
              reply_to_story=None, link_text=None, link_url=None,
              group_id='group_id'):

        if user_ids is None:
            user_ids = []

        if file_type == 'photo':
            method = self.vk.stories.getPhotoUploadServer

        values = {
            'add_to_news': int(add_to_news),
            'user_ids': ','.join(map(str, user_ids)),
            'reply_to_story': reply_to_story,
            'link_text': link_text,
            'link_url': link_url,
            'group_id': group_id
        }

        url = method(**values)['upload_url']

        with open(file, 'rb') as f:
                    response = self.http.post(url, files={'file': f})
                    print(response.text)
                    return response.json()

    def save_story(self, upload_result):
        self.vk.stories.save(upload_results=upload_result['response']['upload_result'])

    def post_and_delete_first_image(self, directory):
        # Получаем список файлов в каталоге
        files = os.listdir(directory)
        # Фильтруем список, чтобы оставить только файлы с расширением .png или .jpg
        images = [file for file in files if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg')]
        # Проверяем, есть ли изображения в каталоге
        if images:
            # Выбираем первое изображение
            image = images[0]
            # Формируем полный путь к изображению
            image_path = os.path.join(directory, image)
            # Загружаем историю с изображением
            upload_result = self.story(image_path, 'photo')
            # Опубликовываем историю
            self.save_story(upload_result)
            # Загружаем фотографию в альбом группы
            self.upload_photo_to_album(image_path, album_id, group_id)
            # Удаляем изображение
            os.remove(image_path)

    def upload_photo_to_album(self, filename, album_id, group_id):
        vk_session = vk_api.VkApi(token='user_token')
        vk = vk_session.get_api()

        # Получаем адрес сервера для загрузки фотографий
        upload_server = vk.photos.getUploadServer(album_id=album_id, group_id=group_id)
        upload_url = upload_server['upload_url']

        # Загружаем фотографию на сервер
        with open(filename, 'rb') as file:
            response = requests.post(upload_url, files={'file1': file}).json()

        # Сохраняем фотографию в альбоме
        photo = vk.photos.save(
            album_id=album_id,
            group_id=group_id,
            server=response['server'],
            photos_list=response['photos_list'],
            hash=response['hash']
        )[0]

        print(f"Фотография сохранена в альбоме с ID {photo['id']}")


    def save_image(self, image_data, directory):
        # Генерируем уникальное имя файла
        filename = f"{uuid.uuid4()}.png"
        # Формируем полный путь к файлу
        filepath = os.path.join(directory, filename)
        # Сохраняем данные изображения в файл
        with open(filepath, 'wb') as f:
            f.write(image_data)
            self.vk.messages.send(
                user_id=user_id,
                message='Изображения были успешно загружены!',
                random_id=random.randint(1, 2**31)
                )
        print('Photo saved on /Stories!')

    def check_images_count(self, directory, user_ids):
        # Получаем список файлов в каталоге
        files = os.listdir(directory)
        # Фильтруем список, чтобы оставить только файлы с расширением .png или .jpg
        images = [file for file in files if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg')]
        # Проверяем количество изображений в каталоге
        if len(images) < 2:
            # Получаем текущее время
            current_time = datetime.datetime.now()
            # Проверяем, прошло ли 4 часа с момента последней отправки сообщения
            if (current_time - self.last_message_time).total_seconds() >= 6 * 60 * 60:
                # Отправляем сообщение пользователю
                for user_id in user_ids:
                    try:
                        self.vk.messages.send(
                            user_id=user_id,
                            message='Количество изображений в архиве меньше 2',
                            random_id=random.randint(1, 2**31)
                        )
                        print(f'Message sended to admin {user_id}!')
                    except:
                        print(f'Message error send to {user_id}!')
                # Обновляем время последней отправки сообщения
                self.last_message_time = current_time
    
    def get_new_messages(self, user_id):
        # Получаем новые сообщения
        messages = self.vk.messages.getHistory(count=200, user_id=user_id)['items']
        # Фильтруем список, чтобы оставить только сообщения от указанного пользователя
        messages = [message for message in messages if message['from_id'] == user_id]
        return messages

    def download_photo(self, url):
        response = self.http.get(url)
        self.vk.messages.send(
            user_id=user_id,
            message='Сохраняю изображения...',
            random_id=random.randint(1, 2**31)
            )
        return response.content

user_ids = ['users_id for message']
album_id = 'album_id'
group_id = 'group_id'
last_message_id = 0
# Сохраняем время запуска бота
start_time = datetime.datetime.now()
my_bot = MyVkBot('Group_token')
#my_bot.post_and_delete_first_image(r'./Stories')
print("Bot started!")

def job():
    my_bot.post_and_delete_first_image(r'./Stories')

# Запланировать задание на каждый день в 00:00
schedule.every().day.at("00:00").do(job)

while True:
    # Получаем новые сообщения от пользователя
    for user_id in user_ids:
        messages = my_bot.get_new_messages(user_id)
        for message in messages:
            # Получаем время отправки сообщения
            message_time = datetime.datetime.fromtimestamp(message['date'])
            # Проверяем, было ли сообщение отправлено после запуска бота
            if message_time > start_time:
                # Проверяем, является ли сообщение новым
                if message['id'] > last_message_id:
                    # Обновляем идентификатор последнего обработанного сообщения
                    last_message_id = message['id']
                    if message['text'] == '/send photos':               
                        # Проверяем, есть ли вложения в сообщении
                        if 'attachments' in message:
                            for attachment in message['attachments']:
                                # Проверяем, является ли вложение фотографией
                                if attachment['type'] == 'photo':
                                    # Получаем URL-адрес фотографии
                                    photo_url = attachment['photo']['sizes'][-1]['url']
                                    # Загружаем данные фотографии
                                    photo_data = my_bot.download_photo(photo_url)
                                    # Сохраняем фотографию в каталоге
                                    my_bot.save_image(photo_data, r'./Stories')
    # Проверяем запланированные задания
    schedule.run_pending()
    # Проверяем количество фотографий в каталоге и отправляем сообщение пользователю, если их меньше 2
    my_bot.check_images_count(r'./Stories', user_ids)
    # Опрашиваем код каждую 1 секунду
    time.sleep(1)
