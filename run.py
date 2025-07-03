from app import create_app, db
from flask import Flask

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Tables created!")

    app.run(debug=True)
