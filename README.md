# Flask Movie Data Application

This application is a Flask web service that provides endpoints for loading movie data into a database, generating charts, and exporting data.

## Getting Started

### Running the Flask Application

To get the Flask application up and running, follow these steps:

1. Set the Flask app environment variable:
   ```shell
   export FLASK_APP=main.py
    flask run

Open a web browser and navigate to http://localhost:5000 to access the application.

2. Running Tests with Pytest

To execute the tests for the Flask application using Pytest, follow these steps:

Ensure you have installed all the project dependencies as mentioned in the setup section.
Navigate to the project directory where test_app.py is located.
Execute the Pytest command to run the tests:

    ```shell
    pytest

3. Application Endpoints

The application provides the following endpoints:

GET /load-data

Loads movie data from a CSV file into the SQLite database.
Usage: Invoke this endpoint once to populate the database before using other endpoints.

GET /draw-chart

Generates a bar chart of movies released per year.
Usage: Access this endpoint after loading data to retrieve a PNG image of the movie release chart.


GET /export-data

Downloads movie release data in CSV format.
Usage: Use this endpoint to export the data for further analysis or record-keeping.
Note: Ensure that the /load-data endpoint has been used to populate the database before accessing the /draw-chart and /export-data endpoints.

For these endpoints, you can use an HTTP client like a web browser, curl, or any REST client software.
