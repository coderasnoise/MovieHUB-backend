from flask import Flask
from flask_migrate import Migrate
from flask_sslify import SSLify

from models import db
from routes import configure_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://batug:pass@35.226.213.195:3306/moviehub'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)
db.init_app(app)
sslify = SSLify(app)
app.config['SECRET_KEY'] = 'another_secret_key_here'


configure_routes(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)







