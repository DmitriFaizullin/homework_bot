class StatusNotChangedException(Exception):
    def __str__(self):
        return 'статус работы не изменился!'


class FormDateException(Exception):
    def __str__(self):
        return 'неправильный формат from_date!'


class NotAuthenticatedException(Exception):
    def __str__(self):
        return 'запрос с недействительным или некорректным токеном!'


class SendingMessageException(Exception):
    def __str__(self):
        return 'сбой при отправке сообщения в Telegram!'


class EndpointException(Exception):
    def __init__(self, error):
        super().__init__()
        self.error = error
    def __str__(self):
        return f'эндпоинт недоступен ({self.error})!'


class UnexpectedStatusException(Exception):
    def __init__(self, status):
        super().__init__()
        self.status = status
    def __str__(self):
        return f'неожиданный статус домажней работы ({self.status})!'


class NoKeyException(Exception):
    def __init__(self, key_name):
        super().__init__()
        self.key_name = key_name
    def __str__(self):
        return f'отсутствует ключ {self.key_name}!'
