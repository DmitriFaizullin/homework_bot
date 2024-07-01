class StatusNotChangedException(Exception):
    """Статус без изменений."""

    def __str__(self):
        """Описание ошибки."""
        return 'статус работы не изменился!'


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

    def __init__(self, error):
        """Инициализатор класса."""
        super().__init__()
        self.error = error

    def __str__(self):
        """Описание ошибки."""
        return f'эндпоинт недоступен ({self.error})!'


class UnexpectedStatusException(Exception):
    """Неожиданный статус домашней работы."""

    def __init__(self, status):
        """Инициализатор класса."""
        super().__init__()
        self.status = status

    def __str__(self):
        """Описание ошибки."""
        return f'неожиданный статус домажней работы ({self.status})!'


class NoKeyException(Exception):
    """Отсутсвует необходимый ключ в ответе сервера."""

    def __init__(self, key_name):
        """Инициализатор класса."""
        super().__init__()
        self.key_name = key_name

    def __str__(self):
        """Описание ошибки."""
        return f'отсутствует ключ {self.key_name}!'
