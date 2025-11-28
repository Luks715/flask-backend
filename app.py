from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# registrar os eventos
import socket_events

# registrar blueprints
from routes.auth_routes import auth
from routes.user_routes import users
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(users, url_prefix="/users")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
