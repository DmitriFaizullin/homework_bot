class StatusNotChangedException(Exception):
    def __str__(self):
        return 'Статус работы не изменился!'


class FormDateException(Exception):
    def __str__(self):
        return 'Неправильный формат from_date!'


class NotAuthenticatedException(Exception):
    def __str__(self):
        return 'Запрос с недействительным или некорректным токеном!'


class SendingMessageException(Exception):
    def __str__(self):
        return 'Сбой при отправке сообщения в Telegram!'


class CheckTokensException(Exception):
    def __str__(self):
        return (
            'В глобальном окружении отсутствует переменная '
            '(PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)!'
        )
