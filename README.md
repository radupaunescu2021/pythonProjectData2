To run the Flask application, follow these steps:

Set the Flask app environment variable:

export FLASK_APP=app.py

Start the Flask development server:

flask run

Open a web browser and navigate to http://localhost:5000 to access the application.

Running Pytest
To run Pytest and execute the tests for the Flask application, follow these steps:

Ensure you have installed the project dependencies as mentioned in the setup section.

Make sure you are in the project directory.

Run the Pytest command: pytest  will automatically discover the tests located in the project directory and its subdirectories and execute them.

Application Endpoints
This Flask application provides several HTTP endpoints that allow users to interact with the movie release data and perform various operations:

1. /load-data (HTTP GET)
Loads the movie data from a CSV file into the SQLite database. It expects the CSV file to be present in the root directory of the project.

Usage: Access this endpoint to populate the SQLite database before attempting to draw charts or export data. This endpoint needs to be called only once, unless the database needs to be refreshed with new data.
2. /draw-chart (HTTP GET)
Generates a bar chart of movies released per year. This endpoint reads the release year data from the SQLite database and creates a PNG image of the chart.

Usage: Access this endpoint after loading data to view a chart representing the distribution of movie releases over the years. The chart will be sent as a response in PNG format.
3. /export-data (HTTP GET)
Allows the user to download the movie release data in CSV format. It queries the SQLite database and provides the data as a downloadable file.

Usage: Access this endpoint to export the movie data from the SQLite database to a CSV file, which can be used for further analysis or record-keeping.
Note: Ensure that the database has been populated with data by using the /load-data endpoint before accessing /draw-chart and /export-data to avoid errors related to missing data.

For each of these endpoints, you would typically use an HTTP client to make the requests. This could be a web browser, command-line tool like curl, or any REST client application.

This section explains what each endpoint does and how to use them, making it easy for someone new to the project to understand the available functionality.