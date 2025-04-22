#!/bin/sh

# Файл, который сигнализирует о том, что init уже запускался
INIT_FLAG=/app/.init_done

# Запускаем Flask в фоне
flask run &
FLASK_PID=$!

# Ждём, пока Flask поднимется (например, проверим порт)
echo "Waiting for Flask to start..."
until nc -z localhost 5000; do
  sleep 1
done

# Если это первый запуск — инициализируем данные
if [ ! -f "$INIT_FLAG" ]; then
  echo "Running init_test_data.py..."
  python init_test_data.py && touch "$INIT_FLAG"
else
  echo "Init already done, skipping init_test_data.py"
fi

# Ждём завершения Flask
wait $FLASK_PID
