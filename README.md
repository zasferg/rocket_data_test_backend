Данное приложение было разработано в рамках тестового задания.
Для запуска вам понадобится docker.
Запуск приложения:
  1. перейдите в папку проектом.
  2. создайте файл .env  и скопируте все данные из .env-sample
  3. откройте терминал выполните команду docker compose up --build.
Проект запустится самостоятельно.
Для генерации данных в бд войидите в контейнер web , перейдите в папку src/test_app и запустите файл populate_db.py.
Для создания суперпользователя так же войдите в контейнер web , перейдите в папку src/test_app введите команду
python manage.py createsuperuser и следуйте дальнейшим указаниям.
