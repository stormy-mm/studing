Обеспечение работы нового сайта
===============================
## Необходимые пакеты:
* nginx
* Python 3.12.3
* virtualenv + pip
* Git

например, в Ubuntu:

    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-getv install nginx git python3.12 python3.12-venv

## Конфигурация виртуального узла Nginx

* см. gunicorn.template.service
* Заменить SITENAME на имя сайта

## Структура папок:
Если допустить, что есть учетная запись пользователя в /home/username

    /home/username
        /sites
            /SITENAME
                /database
                /source
                /static
                /virtualenv