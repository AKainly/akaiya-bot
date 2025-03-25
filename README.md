# Akaiya Telegram Bot

akaiya – это Telegram-бот, который позволит вам получать уникальные аниме-изображения и GIF по запросу. Используйте команды `/start` и `/anime`, чтобы начать работу с ботом.

## Функционал

- **Приветствие пользователя:** Команда `/start` отправляет приветственное сообщение с информацией о возможностях бота.
- **Получение аниме-изображений:** Команда `/anime <tag>` возвращает изображение или GIF по заданному тегу.
- **Случайное изображение:** Используйте тег `random` для получения случайного изображения.

## Теги

Бот поддерживает следующие теги:

- **Изображения:** `waifu`, `neko`, `shinobu`
- **GIF:** `bully`, `cry`, `hug`, `lick`, `pat`, `nom`, `slap`, `dance`, `poke`, `cringe`, `bite`, `blush`, `smug`, `wink`, `highfive`
- **Случайное:** `random`

## Требования

- Python 3.7+
- [aiogram](https://docs.aiogram.dev/) (версия 3.x)
- [aiohttp](https://docs.aiohttp.org/en/stable/)
- Telegram Bot Token (полученный у [BotFather](https://core.telegram.org/bots#6-botfather))

## Установка

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/AKainly/akaiya-bot.git
   cd akaiya-bot
   ```

2. **Создайте виртуальное окружение (рекомендуется):**

   ```bash
   python -m venv .venv
   source venv/bin/activate  # Для Windows: .venv\Scripts\activate
   ```

3. **Установите зависимости:**

   ```bash
   pip install -r requirements.txt
   ```

   _Если файла `requirements.txt` нет, создайте его со следующим содержимым:_

   ```txt
   aiogram>=3.15.0
   aiohttp>=3.10.11
   ```

4. **Настройте переменные окружения или файл конфигурации:**

   `config.py` укажите в нем ваш Telegram Bot Token:

   ```python
   TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
   ```

## Запуск бота

Запустите бота командой:

```bash
python main.py
```

После запуска бот начнет получать обновления через long polling. Убедитесь, что одновременно запущена только одна копия бота, иначе вы можете столкнуться с ошибкой `TelegramConflictError`.

## Разработка

- Основной код находится в файле `main.py`.
- Для обработки команд используются декораторы aiogram.
- Для получения изображений используется API [waifu.pics](https://waifu.pics/) и [pic.re](https://pic.re/).

## Вклад

Если вы хотите внести изменения или улучшения, пожалуйста, создайте pull request. Любые замечания и предложения приветствуются!
