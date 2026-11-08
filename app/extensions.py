from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Created here without an app; the app factory attaches them with init_app().
db = SQLAlchemy()
migrate = Migrate()
