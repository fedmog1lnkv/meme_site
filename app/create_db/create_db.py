from app import connect_db, app

def create_db():
    db = connect_db()
    with app.open_resource('create_db/sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

# Раскоментировать строку ниже и выполнить скрипт
# create_db()