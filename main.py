import sqlite3
from collections import Counter
import matplotlib
import pandas as pd
from matplotlib import pyplot as plt

matplotlib.use('Agg')

from flask import Flask, send_file, make_response


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
    # Count the number of movies released each year using a Counter collection
    # which will store each year as a key and the number of releases as its value
    year_count = Counter(release_years)

    # Extract the years from the counter which are the keys of the counter dictionary
    # These will serve as the x-axis labels for the bar chart
    years = list(year_count.keys())

    # Extract the counts from the counter which are the values of the counter dictionary
    # These will represent the height of the bars, i.e., the number of releases per year
    counts = list(year_count.values())

    # Generate the bar chart using matplotlib with years on the x-axis and counts on the y-axis
    plt.bar(years, counts)

    # Customize the chart by adding labels and a title
    plt.xlabel('Release Year')  # Label for the x-axis
    plt.ylabel('Number of Movies')  # Label for the y-axis
    plt.title('Movies Released Per Year')  # Chart title

    # Improve readability of the x-axis labels by rotating them 45 degrees
    plt.xticks(rotation=45)

    # Adjust the layout to ensure the chart is displayed nicely without any clipping
    plt.tight_layout()

    # Save the chart as a PNG image in the current directory
    plt.savefig('chart.png')

    # Close the matplotlib plot to free up memory resources
    plt.close()



@app.route('/draw-chart')
def graph_endpoint():
    # Check if the SQLite database has data before attempting to draw the chart.
    # The function database_has_data() should return a boolean indicating if data is present.
    if not database_has_data():
        # If there is no data, return a HTTP 400 response with an error message.
        return 'No data available in SQLite database.', 400

    # Establish a connection to the SQLite database that contains the movies data.
    conn = sqlite3.connect('movies.db')

    # Query the database to retrieve only the 'release_year' column from the 'movies' table
    # and read the result into a pandas DataFrame.
    df = pd.read_sql_query("SELECT release_year FROM movies", conn)

    # Call the function generate_movie_release_chart with the list of release years
    # to create and save the bar chart image.
    # The 'release_year' column is cast to integers to ensure proper handling by the chart function.
    generate_movie_release_chart(df['release_year'].astype(int).tolist())

    # After the chart has been generated, send it back as a file response with MIME type image/png.
    # The user will receive the chart as a downloadable or viewable PNG image.
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
    # Endpoint to export data from the SQLite database to a CSV file.

    # First, we check if there's data in the database to export.
    # The database_has_data() function should check for the existence of data and return True or False.
    if not database_has_data():
        # If the check returns False (no data), we send a 400 HTTP response with an error message.
        return 'No data available in SQLite database.', 400

    # If there is data, establish a connection to the SQLite database.
    conn = sqlite3.connect('movies.db')

    # Execute a SQL query to select the 'title' and 'release_year' of all movies in the database.
    # The result is read into a pandas DataFrame for easy manipulation and CSV conversion.
    df = pd.read_sql_query("SELECT title, release_year FROM movies", conn)

    # Convert the DataFrame to a CSV format. Index=False means we don't include the DataFrame index in the CSV.
    csv_data = df.to_csv(index=False)

    # Create an HTTP response object with the CSV data as the content.
    response = make_response(csv_data)

    # Set the content type of the response to 'text/csv' which is appropriate for CSV files.
    response.headers['Content-Type'] = 'text/csv'

    # Configure the Content-Disposition header so that the browser prompts the user to
    # download the file as 'movies.csv' instead of displaying it.
    response.headers['Content-Disposition'] = 'attachment; filename=movies.csv'

    # Send the response back to the client, triggering the download of the movies.csv file.
    return response