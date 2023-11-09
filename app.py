import csv
import io
import sqlite3
from collections import Counter

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, send_file, make_response

matplotlib.use("Agg")

app = Flask(__name__)


def generate_movie_release_chart(chart_path="chart.png"):
    # Connect to the SQLite database
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    # Query the database for all movies release dates
    cursor.execute("SELECT release_date FROM movies")
    release_dates = cursor.fetchall()

    # Close the SQLite connection
    conn.close()

    # Extract just the release years from the dates
    release_years = [
        int(date[0][:4])
        for date in release_dates
        if date[0] and len(date[0]) >= 4 and date[0][:4].isdigit()
    ]

    # Count the number of movies released each year
    year_counts = Counter(release_years)

    # Sort the years and counts so they are in order
    years, counts = zip(*sorted(year_counts.items()))

    # Prepare data for the bar chart
    fig, ax = plt.subplots()

    # Generate the bar chart
    ax.bar(years, counts)

    # Customize the chart
    ax.set_xlabel("Release Year")
    ax.set_ylabel("Number of Movies")
    ax.set_title("Movies Released per Year")

    # Set the x-axis to only include the range of years found in the dataset
    ax.set_xlim([min(years), max(years)])

    # Optionally, rotate x-axis labels if needed
    plt.xticks(rotation=45)

    # Use tight_layout to automatically adjust subplot params
    plt.tight_layout()

    # Save the chart to a file instead of showing it
    plt.savefig(chart_path)
    plt.close()


@app.route("/")
def index():
    return """
    <h1>Welcome to the Movie Release Chart App!</h1>
    <ul>
        <li><a href="/draw-chart">Draw Chart</a> - Generate and download a movie release chart.</li>
        <li><a href="/load-data">Load Data</a> - Load data into the SQLite database from the CSV file.</li>
        <li><a href="/export-data">Export Data</a> - Export movie data as a CSV file.</li>
    </ul>
    """


@app.route("/draw-chart")
def graph_endpoint():
    generate_movie_release_chart()

    # Return the generated chart as a file download
    return send_file("chart.png", mimetype="image/png")


@app.route("/load-data")
def load_data_endpoint():
    # Connect to the SQLite database
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    # Ensure that the table is created
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        release_date TEXT NOT NULL
    )
    """
    )

    # Clear existing data in the table
    cursor.execute("DELETE FROM movies")

    # Read the dataset into a pandas DataFrame
    df = pd.read_csv("movies_metadata.csv")

    # Preprocess the release_date column to ensure it contains valid dates
    # We'll assume a valid date is in the format YYYY-MM-DD and the year is after 1800
    valid_dates = df["release_date"].str.match(r"^\d{4}-\d{2}-\d{2}$") & (
            df["release_date"].str[:4] > "1800"
    )
    df = df[valid_dates]

    # Insert data into the movies table
    df[["title", "release_date"]].to_sql(
        "movies", conn, if_exists="replace", index=False
    )

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    return "Data loaded successfully into the database"


@app.route("/export-data")
def export_data():
    # Connect to the SQLite database
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    # Query the database for all movies
    cursor.execute("SELECT title, release_date FROM movies")
    movies = cursor.fetchall()

    # Set the response headers to indicate a CSV file download
    headers = {
        "Content-Type": "text/csv",
        "Content-Disposition": "attachment; filename=movies.csv",
    }

    # Create a temporary in-memory file to write the CSV data
    temp_file = io.StringIO()
    writer = csv.writer(temp_file)

    # Write the CSV header
    writer.writerow(["title", "release_year"])

    # Write each movie as a CSV row
    for movie in movies:
        writer.writerow(movie)

    # Move the file pointer to the beginning of the file
    temp_file.seek(0)

    # Create a Flask response with the CSV file
    response = make_response(temp_file.getvalue())
    response.headers = headers

    # Close the in-memory file
    temp_file.close()

    # Return the response
    return response


if __name__ == "__main__":
    app.run(debug=True, port=8080, host="localhost")
