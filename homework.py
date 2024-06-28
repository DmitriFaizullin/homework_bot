import os
import requests
from telebot import TeleBot, types
from dotenv import load_dotenv
import time
import exceptions as ex
import logging
# from logging.handlers import StreamHandler

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


def check_tokens():
    try:
        if not (PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID):
            raise ex.CheckTokensException
    except ex.CheckTokensException as error:
        logging.critical(error)
        # завершить работу


def send_message(bot, message):
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )
        logging.debug('Удачная отправка сообщения в Telegram')
    except Exception:
        raise ex.SendingMessageException


def get_api_answer(timestamp):
    api_answer = requests.get(ENDPOINT, headers=HEADERS, params={'from_date': timestamp})
    return api_answer.json()


def check_response(response):
    if 'homeworks' in response:
        if not response['homeworks']:
            raise ex.StatusNotChangedException
    if 'code' in response:
        if response['code'] == 'UnknownError':
            raise ex.FormDateException
        elif response['code'] == 'not_authenticated':
            raise ex.NotAuthenticatedException
        else:
            raise Exception


def parse_status(homework):
    if 'status' in homework:
        status = homework.get('status')
        if status in HOMEWORK_VERDICTS:
            verdict = HOMEWORK_VERDICTS.get(status)
            homework_name = homework.get('homework_name')
            return f'Изменился статус проверки работы "{homework_name}". {verdict}'
        raise Exception
    raise Exception


def main():
    """Основная логика работы бота."""

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='main.log',
        level=logging.DEBUG,
    )

    check_tokens()

    # Создаем объект класса бота
    bot = TeleBot(token=TELEGRAM_TOKEN)
    timestamp = 0
    # timestamp = int(time.time()) - RETRY_PERIOD

    ...

    while True:
        try:
            response = get_api_answer(timestamp)
            check_response(response)
            message = parse_status(response.get('homeworks')[0])
            send_message(bot, message)
            ...

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            ...
        ...


if __name__ == '__main__':
    main()
