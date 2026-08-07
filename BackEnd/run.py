from app import create_app
from flask_login import LoginManager

login_manager = LoginManager()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)