### Food App WIP

Save, Read, and Commit to creating all your favorite recipes from popular influencers on Instagram, Tiktok, and more!

### Setup:

Ensure the latest version of Python, Node.js, and npm are installed

Run pip install -r requirements.txt from the root directory to get all required packages

### Updating the database:

Update the models in models.py, run the following commands if you modify any attributes of an existing schema or create a new schema.

flask db migrate -m "comments"

flask --app run.py db upgrade

### Run Flask Backend:

Navigate into the BackEnd folder and then run:

python run.py

All routes are found in BackEnd\app\routes

### Run React:

Navigate from the root to FrontEnd and then Food-Project (FoodApp\FrontEnd\Food-Project)

npm run dev

In order to send requests from the frontend to the backend, both commands must be run in separate terminals.

### Testing

Navigate to BackEnd folder and then run the following command to run every test file:

python -m pytest 

If you want to mess around with bash scripting, open a bash terminal and navigate to BackEnd\testing\tests.sh and run:

bash tests.sh

Information about creating bash tests is found in tests.sh

---