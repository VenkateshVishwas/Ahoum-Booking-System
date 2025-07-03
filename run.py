from app import create_app, db
from flask import Flask
import os

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Tables created!")

    
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

