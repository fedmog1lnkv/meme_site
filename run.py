import os

print("Установка библиотек")
os.system('pip install -r requirements.txt')

if os.path.exists('app/database.db') == False:
    print("Создание БД")
    os.system('python app/create_db/create_db.py')

print("запуск приложения")
os.system('python main.py')