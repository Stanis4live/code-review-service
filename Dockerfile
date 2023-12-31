# Используем официальный образ Python (основной образ) из Docker Hub
# использует базовые файлы и библиотеки из Debian 10
FROM python:3.10-slim-buster

# Устанавливаем рабочую директорию в контейнере. В ней будут находиться все файлы, которые будет необходимо выполнить
# при помощи образа.
WORKDIR /app

# Копируем файл зависимостей в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости. Команда, которая выполнится при первом запуске контейнера
RUN addgroup celerygroup && adduser --ingroup celerygroup celeryuser
RUN mkdir /var/log/mydjangoapp && chown -R celeryuser:celerygroup /var/log/mydjangoapp
RUN pip install --no-cache-dir psycopg2-binary
RUN pip install --no-cache-dir -r requirements.txt

# Копируем содержимое локальной директории в контейнер. Из корневой директории проекта в корневую директорию образа либо
# в директорию, которую я установил в WORKDIR
COPY . .

USER celeryuser

# Указываем порт, на котором будет работать приложение внутри образа
EXPOSE 8000

# Команда для запуска приложения. Выполняется каждый раз при запуске контейнера
# все слова команды пишутся отдельными строками через запятую в списке
CMD ["gunicorn", "code_review_service.wsgi:application", "--bind", "0.0.0.0:8000"]
