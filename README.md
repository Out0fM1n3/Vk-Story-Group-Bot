# VK-Story-Group-Bot
## Описание на русском

Этот проект представляет собой бота для социальной сети VK, который может публиковать истории и фотографии в группе VK.

## Установка

Для использования этого бота необходимо установить следующие зависимости:

```
pip install vk_api
pip install requests
pip install schedule
```

## Использование

Чтобы использовать этого бота, необходимо создать экземпляр класса `MyVkBot`, передав токен группы в качестве аргумента:

```python
my_bot = MyVkBot('Group_token')
```

Затем можно использовать различные методы класса `MyVkBot` для публикации историй и фотографий в группе VK. Например, чтобы опубликовать историю с изображением, можно использовать метод `story`:

```python
upload_result = my_bot.story(image_path, 'photo')
my_bot.save_story(upload_result)
```

Вот информация об аргументах некоторых методов класса `MyVkBot`:

- Метод `post_and_delete_first_image` принимает один аргумент `directory`, который указывает каталог, из которого нужно выбрать первое изображение для публикации.

- Метод `save_image` принимает два аргумента: `image_data` и `directory`. Аргумент `image_data` содержит данные изображения, которые нужно сохранить в файле. Аргумент `directory` указывает каталог, в котором нужно сохранить файл с изображением.

- Метод `check_images_count` принимает два аргумента: `directory` и `user_ids`. Аргумент `directory` указывает каталог, в котором нужно проверить количество изображений. Аргумент `user_ids` содержит список идентификаторов пользователей, которым нужно отправить сообщение, если количество изображений в каталоге меньше 2.

- Метод `get_new_messages` принимает один аргумент `user_id`, который указывает идентификатор пользователя, от которого нужно получить новые сообщения.

- Метод `download_photo` принимает один аргумент `url`, который указывает URL-адрес фотографии, которую нужно загрузить.



# VK-Story-Group-Bot
## Description in English

This project is a VK bot that can post stories and photos to a VK group.

## Installation

To use this bot, you need to install the following dependencies:

```
pip install vk_api
pip install requests
pip install schedule
```

## Usage

To use this bot, you need to create an instance of the `MyVkBot` class, passing the group token as an argument:

```python
my_bot = MyVkBot('Group_token')
```

Then you can use various methods of the `MyVkBot` class to post stories and photos to a VK group. For example, to post a story with an image, you can use the `story` method:

```python
upload_result = my_bot.story(image_path, 'photo')
my_bot.save_story(upload_result)
```

Here is information about the arguments of some methods of the `MyVkBot` class:

- The `post_and_delete_first_image` method takes one argument `directory`, which specifies the directory from which to select the first image for publication.

- The `save_image` method takes two arguments: `image_data` and `directory`. The `image_data` argument contains the image data that needs to be saved to a file. The `directory` argument specifies the directory in which to save the file with the image.

- The `check_images_count` method takes two arguments: `directory` and `user_ids`. The `directory` argument specifies the directory in which to check the number of images. The `user_ids` argument contains a list of user IDs to send a message to if the number of images in the directory is less than 2.

- The `get_new_messages` method takes one argument `user_id`, which specifies the user ID from whom to receive new messages.

- The `download_photo` method takes one argument `url`, which specifies the URL of the photo to download.
