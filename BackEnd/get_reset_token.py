## The sole purpose of this file is to test both the forgot-password and reset-password routes in one workflow ##
## The token is generated after the forgot-password route runs which is then taken as a parameter by the reset-password route ##
## Token is printed onto terminal so bash can read it and test the reset-password route ##

from app.models import User
from app.extensions import db
from run import app
from sqlalchemy import select

email = "bash-test2@gmail.com"

with app.app_context():
    stmt = select(User).filter_by(email=email)
    user = db.session.scalars(stmt).first()

    if user:
        print(user.reset_token)