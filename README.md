# Running the Flask Application
To run the Flask application, follow these steps:

Set the Flask app environment variable:

`export FLASK_APP=app.py`

Start the Flask development server:

`flask run`

Open a web browser and navigate to http://localhost:5000 to access the application.

# Running Pytest
To run Pytest and execute the tests for the Flask application, follow these steps:

Ensure you have installed the project dependencies as mentioned in the setup section.

Make sure you are in the project directory.

Run the Pytest command:
`pytest`
Pytest will automatically discover the tests located in the project directory and its subdirectories and execute them.

# To create a SQLite database, you can follow these steps:

Open a terminal window. You can find the Terminal application in the Utilities folder within the Applications folder.
Navigate to the directory where you want to create the SQLite database file. For example, if you want to create the database 
file in your home directory, use the following command:

`cd ~`

Launch the SQLite shell by running the following command:

`sqlite3 database.db`

Replace database.db with the name you want to give to your SQLite database file. This command will create a new SQLite database file with the specified name in the current directory.

Once you run the command, you will enter the SQLite shell prompt, indicated by 
`sqlite>`. 
