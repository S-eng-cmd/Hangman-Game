# Простий додаток django

Додаток призначений для вивчення основ застосування django у web-розробці.

## Як встановити

* Створіть **порожню** папку на робочому столі, запустіть командний рядок і клонуйте репозиторій:

      git clone https://github.com/ap75/game.git .

* Створіть віртуальне оточення

      python -m venv .venv

* Активуйте віртуальне оточення

      .venv\Scripts\activate

* Встановіть необхідні бібліотеки

      pip install -r requirements.txt

* Застосуйте міграції

      python manage.py migrate

* Додайте суперкористувача, якщо хочете користуватися адмінкою

      python manage.py createsuperuser

* Запустіть додаток, [відкрийте його у браузері](http://127.0.0.1:8000/)

      python manage.py runserver
