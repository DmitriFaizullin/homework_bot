import os
import requests
from telebot import TeleBot
from dotenv import load_dotenv
import time
import exceptions as ex
import logging
import sys

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
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


def check_tokens():
    """Docstring."""
    if not (PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID):
        logging.critical(
            'В глобальном окружении отсутствует переменная '
            'PRACTICUM_TOKEN, TELEGRAM_TOKEN или TELEGRAM_CHAT_ID!'
        )
        sys.exit()


def send_message(bot, message):
    """Отправка сообщения в Telegram."""
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )
        logging.debug('Удачная отправка сообщения в Telegram')
    except Exception:
        raise ex.SendingMessageException


def get_api_answer(timestamp):
    """Docstring."""
    try:
        api_answer = requests.get(ENDPOINT, headers=HEADERS, params={'from_date': timestamp})
        if api_answer.status_code != 200:
            raise Exception(f'status code ответа {api_answer.status_code}')
        return api_answer.json()
    except Exception as error:
        raise ex.EndpointException(error)


def check_response(response):
    """Docstring."""
    if not isinstance(response, dict):
        raise TypeError('формат ответа сервера должен быть классa dict')
    if 'homeworks' in response:
        if not isinstance(response['homeworks'], list):
            raise TypeError('класс homeworks должен быть list')
        if not response['homeworks']:
            raise ex.StatusNotChangedException
    elif 'code' in response:
        if response['code'] == 'UnknownError':
            raise ex.FormDateException
        elif response['code'] == 'not_authenticated':
            raise ex.NotAuthenticatedException
    else:
        raise ex.NoKeyException('homeworks или code')


def parse_status(homework):
    """Docstring."""
    if 'status' in homework:
        status = homework.get('status')
        if status in HOMEWORK_VERDICTS:
            verdict = HOMEWORK_VERDICTS.get(status)
            if 'homework_name' not in homework:
                raise ex.NoKeyException('homework_name')
            homework_name = homework.get('homework_name')
            return f'Изменился статус проверки работы "{homework_name}". {verdict}'
        raise ex.UnexpectedStatusException(status)
    raise ex.NoKeyException('status')


def main():
    """Основная логика работы бота."""
    check_tokens()

    # Создаем объект класса бота
    bot = TeleBot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time()) - RETRY_PERIOD
    previous_message = ''

    while True:
        try:
            response = get_api_answer(timestamp)
            check_response(response)
            message = parse_status(response.get('homeworks')[0])
            send_message(bot, message)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            if type(error) is ex.StatusNotChangedException:
                logging.debug(message)
            else:
                if type(error) is not ex.SendingMessageException:
                    if previous_message != message:
                        send_message(bot, message)
                        previous_message = message
                logging.error(message)

        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
