from .models import Auto
if not path.exists('website/' + DB_NAME):
    db.create_all(app=app)
    print('Created database!')
    for i in Auto:
        print(i)
