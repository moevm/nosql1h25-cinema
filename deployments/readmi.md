

## Информация для запуска:
### ВСЕ КОМАНДЫ ИСПОЛЬЗУЮТСЯ ИЗ КОРНЕВОГО КАТАЛОГА ПРОЕКТА

1. Запустить базу данных через docker:
    
    ```docker-compose -f /deploymants/docker-compose.yml up -d```
   
    Для остановки БД и её УДАЛЕНИЯ ```docker-compose down -v```
2. Для запуска backend и теста работы с базой:

   2.1. Создать venv в каталоге backend:

      - ```python -m venv venv```
   

   2.2. Активировать окружение:

```.\venv\Scripts\activate```


   2.3. Обновить pip:

```python.exe -m pip install --upgrade pip```

   2.4. Установить зависимости:
      
```pip install -r requirements.txt```

Для запуска сервера 
```python main.py```

Для запуска тестов (при запущенном сервере)
```python init_test_data.py```