# Используйте базовый образ
FROM python:3.11

# Установите/обновите зависимости, если необходимо
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# Установите рабочую директорию внутри контейнера
WORKDIR /app/

# Копируйте файлы и папки из хост-системы в контейнер
COPY . /app

# Определите переменные среды, если необходимо
ENV DJANGO_SETTINGS_MODULE=myproject.settings.production

# Определите порты, которые контейнер будет использовать
EXPOSE 8000

# Определите команду, которая будет выполняться при запуске контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
