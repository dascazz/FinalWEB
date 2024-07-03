from flask import Flask
from flask_cors import CORS
from models import mysql
from routes.user_routes import bp as user_bp
from routes.reservation_routes import bp as reservation_bp
from routes.review_routes import bp as review_bp

app = Flask(__name__)
CORS(app)
app.config.from_object('config.Config')
mysql.init_app(app)

# Register Blueprints
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(reservation_bp, url_prefix='/reservation')
app.register_blueprint(review_bp, url_prefix='/review')



if __name__ == '__main__':
    app.run(debug=True)
