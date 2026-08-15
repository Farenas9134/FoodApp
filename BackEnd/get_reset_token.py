import sys
from app.models import User
from app.extensions import db
from app import create_app

app = create_app()

email = sys.argv[1]

with app.app_context