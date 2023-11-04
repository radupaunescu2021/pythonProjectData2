import sqlite3
from collections import Counter
from urllib import response

import matplotlib
import pandas as pd
from matplotlib import pyplot as plt

matplotlib.use('Agg')

from flask import Flask, send_file, make_response

import csv
import io

app = Flask(__name__)


def database_has_data():
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()

    # Check if the table exists and has data
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='movies'")
    table_exists = cur.fetchone()
    if table_exists:
        cur.execute("SELECT count(*) FROM movies")
        data_count = cur.fetchone()[0]
        conn.close()
        return data_count > 0
    conn.close()
    return False


def generate_movie_release_chart(release_years):
    # Count the number of movies released each year
    year_count = Counter(release_years)
    years = list(year_count.keys())
    counts = list(year_count.values())
    # Prepare data for the bar chart
    # Generate the bar chart
    plt.bar(years, counts)
    # Customize the chart
    plt.xlabel('Release Year')
    plt.ylabel('Number of Movies')
    plt.title('Movies Released Per Year')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('chart.png')
    plt.close()




@app.route('/draw-chart')
def graph_endpoint():
    if not database_has_data():
        return 'No data available in SQLite database.', 400

    conn = sqlite3.connect('movies.db')
    df = pd.read_sql_query("SELECT release_year FROM movies", conn)
    generate_movie_release_chart(df['release_year'].astype(int).tolist())
    return send_file('chart.png', mimetype='image/png')

@app.route('/load-data')
def load_data_endpoint():
    try:
        # Load the CSV data into a pandas DataFrame
        df = pd.read_csv('movies_metadata.csv',low_memory=False)

        # Convert the 'release_date' column to datetime, coerce errors to NaT (not a time), and extract the year
        df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year

        # Select only the 'title' and 'release_year' columns, and drop rows with NaN in these columns
        df = df[['title', 'release_year']].dropna()

        # Create a SQLite database called 'movies.db' (or connect to it if it already exists)
        with sqlite3.connect('movies.db') as conn:

            # Write the DataFrame to a SQL table named 'movies', replacing it if it already exists
            df.to_sql('movies', conn, if_exists='replace', index=False)

        # Close the connection to the database
        conn.close()

        # Return a success message if everything went fine
        return 'Data loaded into SQLite database successfully.'
    except Exception as e:
        # If any error occurs, return the error message
        return f'An error occurred: {e}'


@app.route('/export-data')
def export_data():
    if not database_has_data():
        return 'No data available in SQLite database.', 400

    conn = sqlite3.connect('movies.db')
    df = pd.read_sql_query("SELECT title, release_year FROM movies", conn)
    csv_data = df.to_csv(index=False)

    response = make_response(csv_data)
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=movies.csv'
    return response