from flask import Flask
from config import Config
from models import db
from routes import bp as ingredients_bp
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(ingredients_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(port=5001)