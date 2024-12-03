## 📚 Homework Status Telegram Bot

Этот проект представляет собой **Telegram-бота**, который отслеживает статус домашних работ через API Яндекс.Практикума и отправляет уведомления в Telegram.

---

#### 📝 Описание

Бот проверяет статус домашних работ, используя API Яндекс.Практикума. При изменении статуса работы бот отправляет уведомления в указанный чат Telegram.
Добавлено логирование работы программы.

---

#### 🚀 Установка

#### Требования

- **Python** 3.7 или выше
- Установленные библиотеки:
  - `requests`
  - `python-dotenv`
  - `pyTelegramBotAPI`

1. Клонируйте репозиторий:
    ```sh
    git clone git@github.com:DmitriFaizullin/homework_bot.git
    cd homework_bot
    ```
2. Установите и активируйте виртуальное окружение:
    ```sh
    python3 -m venv venv
    ```
    для Linux/MacOS:
    ```
    source venv/bin/activate
    ```
    для Windows:
    ```
    source venv/Scripts/activate
    ```
3. Установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```

4. Создайте файл `.env` в корневом каталоге проекта и добавьте следующие строки:
    ```env
    PRACTICUM_TOKEN=your_practicum_token
    TELEGRAM_TOKEN=your_telegram_token
    TELEGRAM_CHAT_ID=your_telegram_chat_id
    ```
---
#### 💻 Использование
Запустите бота с помощью следующей команды:
```sh
python homework_bot.py
```

Бот начнет проверять статус домашних работ и отправлять уведомления в Telegram.

---
#### 👤 Авторы
Файзуллин Дмитрий Андреевич [Мой Telegram](https://t.me/DmitriFn)

---
Спасибо за внимание! Если у вас есть вопросы или предложения, не стесняйтесь обращаться.