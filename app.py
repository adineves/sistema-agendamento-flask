from flask import Flask
from app.routes import main
from app.models import db

print("INICIO DO APP")  # <-- DEBUG

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(main)

if __name__ == "__main__":
    print("ENTROU NO MAIN")  # <-- DEBUG

    with app.app_context():
        db.create_all()

    print("ANTES DO RUN")  # <-- DEBUG
    app.run(debug=True)
