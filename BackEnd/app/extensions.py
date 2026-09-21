from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from sqlalchemy import MetaData, event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection

import sqlalchemy as sa


# Initialize SQLAlchemy instance (outside create_app for import access)

# Define explicit naming rules for SQL constraints (issues with sqlalchemy generating None constraints)
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
login_manager = LoginManager()

# Pthon's built-in SQLite driver ignores foreign key rules like "ON DELETE CASCADE"
# This listener ensures we enforce the rules (had issues with ingredientRecipes not being deleted)
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()