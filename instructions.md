# Инструкции по запуску и тестированию

## Запуск

Из корня проекта запустить следующие команды

```sh
docker compose build --no-cache
docker compose up
```

После чего приложение будет доступно на 5000 порту:
<http://localhost:5000>

## Тестирование

Для тестирования можно добавлять новые фильмы в бд или удалять существующие в админ панели в разделе **Каталог**.

### Как попасть в админ панель

Для перехода в админ панель нужно перейти по адресу:

<http://localhost:5000/admin>

и ввести логин и пароль (на данный момент при запуске приложения создается один администратор - логин: `admin123@mail.ru`, пароль: `123456`)

Нажмите *Войти*, после чего попадете на вкладку **Статистика**, сверху можно выбрать вкладку **Каталог**.
