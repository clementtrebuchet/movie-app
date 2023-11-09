# Movie-App

This application allows users to generate movie release charts, load data from a CSV file into a SQLite database, 
and export movie data from the database.


## Running the Flask Application
To run the Flask application, follow these steps:

Start the Flask development server:

```bash
python app.py
```

Open a web browser and navigate to http://localhost:8080 to access the application.

## Running Pytest
To run Pytest and execute the tests for the Flask application, follow these steps:

Ensure you have installed the project dependencies as mentioned in the setup section.

Make sure you are in the project directory.

Run the Pytest command:

```bash
pytest
```
Pytest will automatically discover the tests located in the project directory and its subdirectories and execute them.

# To create a SQLite database, you can follow these steps:

The SQLite database is automatically created by the application.

# CSV Data File

Place the `movies_metadata.csv` file in the root of the `movie-app` folder before starting the application or loading data. 

This CSV file is used to populate the SQLite database with movie data.
