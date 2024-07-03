import logging
import os
import sys
import time
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from telebot import TeleBot, apihelper

import exceptions as ex


load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(
    logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
)
logger.addHandler(handler)


def check_tokens():
    """Проверка наличия токенов в окружении."""
    tokens = {
        'PRACTICUM_TOKEN': PRACTICUM_TOKEN,
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
        'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID,
    }
    missing_tokens = [name for name, value in tokens.items() if not value]
    for token in missing_tokens:
        logging.critical(
            f'В глобальном окружении отсутствует переменная {token}')
    return missing_tokens


def send_message(bot, message):
    """Отправка сообщения в Telegram."""
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )
    except (apihelper.ApiException, requests.RequestException):
        raise ex.SendingMessageException
    logging.debug('Удачная отправка сообщения в Telegram')


def get_api_answer(timestamp):
    """Сделать запрос к api сайта."""
    request_params = {
        'url': ENDPOINT,
        'headers': HEADERS,
        'params': {'from_date': timestamp}
    }
    try:
        api_answer = requests.get(**request_params)
        if api_answer.status_code != HTTPStatus.OK:
            raise ex.StatusCodeException(api_answer.status_code)
    except requests.RequestException:
        raise ex.EndpointException(request_params["url"])
    return api_answer.json()


def check_response(response):
    """Проверить ответ сервера."""
    if not isinstance(response, dict):
        raise TypeError(f'класс ответа сервера {type(response)} вместо dict')
    if 'homeworks' in response:
        if not isinstance(response['homeworks'], list):
            raise TypeError(
                f'класс homeworks {type(response["homeworks"])} вместо list')
        if not response['homeworks']:
            logging.debug('Cтатус работы не изменился!')
            return False
    elif 'code' in response:
        if response['code'] == 'UnknownError':
            raise ex.FormDateException
        if response['code'] == 'not_authenticated':
            raise ex.NotAuthenticatedException
    else:
        raise KeyError('homeworks или code')
    return True


def parse_status(homework):
    """Возвращает статус домашней работы."""
    if 'status' not in homework:
        raise KeyError('status')
    status = homework['status']
    if status not in HOMEWORK_VERDICTS:
        raise KeyError(f'отсутствует ключ {status}')
    if 'homework_name' not in homework:
        raise KeyError('отсутствует ключ homework_name')
    return (
        f'Изменился статус проверки работы '
        f'"{homework["homework_name"]}". {HOMEWORK_VERDICTS[status]}'
    )


def main():
    """Основная логика работы бота."""
    if check_tokens():
        sys.exit()

    bot = TeleBot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time()) - RETRY_PERIOD
    previous_message = ''

    while True:
        try:
            response = get_api_answer(timestamp)
            if check_response(response):
                message = parse_status(response.get('homeworks')[0])
                send_message(bot, message)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
            if isinstance(error, ex.SendingMessageException):
                break
            if previous_message != message:
                send_message(bot, message)
                previous_message = message

        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
