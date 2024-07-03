class FormDateException(Exception):
    """Неправильный формат from_date."""

    def __str__(self):
        """Описание ошибки."""
        return 'неправильный формат from_date!'


class NotAuthenticatedException(Exception):
    """Неверный токен."""

    def __str__(self):
        """Описание ошибки."""
        return 'запрос с недействительным или некорректным токеном!'


class SendingMessageException(Exception):
    """Сбой отправки сообщения в Telegram."""

    def __str__(self):
        """Описание ошибки."""
        return 'сбой при отправке сообщения в Telegram!'


class EndpointException(Exception):
    """Недоступен эндпоинт."""

    def __str__(self):
        """Описание ошибки."""
        return (f'Эндпоинт {self.args[0]} недоступен.')


class StatusCodeException(Exception):
    """Неверный сатус-код API сервера."""

    def __str__(self):
        """Описание ошибки."""
        return (f'Код ответа API: {self.args[0]}')
