# YooKassa Payment History Downloader

## Описание

Проект предназначен для загрузки истории транзакций из сервиса [ЮKassa](https://yookassa.ru/) за указанный период времени. Приложение позволяет пользователю выбрать даты начала и окончания периода и сохраняет историю успешных платежей в CSV-файл для дальнейшего анализа или учета.

## Функциональность

- Ввод дат начала и окончания периода для получения истории транзакций.
- Автоматическая загрузка данных по всем указанным аккаунтам ЮKassa.
- Сохранение истории транзакций в CSV-формате.
- Графический пользовательский интерфейс для удобства использования.

## Установка и запуск

Чтобы запустить проект, необходимо установить Python и необходимые библиотеки. Следуйте инструкциям ниже для настройки проекта:

1. Клонируйте репозиторий на ваш локальный компьютер:


git clone https://github.com/OrdinSI/YooKassa-Payment-History-Downloader.git

2. Перейдите в каталог проекта:


cd YooKassa-Payment-History-Downloader

3. Установите виртуальное окружение и активируйте его:

Для Windows:


python -m venv venv
venv\Scripts\activate

Для macOS и Linux:


python3 -m venv venv
source venv/bin/activate

4. Установите необходимые зависимости:


pip install -r requirements.txt

5. Запустите приложение:


python main.py

## Компиляция в исполняемый файл

Для компиляции приложения в единый исполняемый файл для Windows, используйте следующую команду:


pyinstaller --onefile --windowed main.py

После компиляции, исполняемый файл `.exe` будет находиться в каталоге `dist`.


## Лицензия

[MIT](LICENSE)