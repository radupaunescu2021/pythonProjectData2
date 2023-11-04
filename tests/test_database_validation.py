import pandas as pd
import pytest
import sqlite3

from main import load_data_endpoint


@pytest.fixture
def sqlite_connection():
    #Load data into sql lite database movies.db
    load_data_endpoint()
    # Setup code: create a connection to the SQLite database
    connection = sqlite3.connect('movies.db')
    yield connection
    # Teardown code: close the connection after the test runs
    connection.close()


def test_record_count(sqlite_connection):
    # Load the dataset into a pandas DataFrame
    df_sqlite = pd.read_sql_query("SELECT * FROM movies", sqlite_connection)

    # Load original data
    df_original = pd.read_csv('movies_metadata.csv', usecols=['title', 'release_date'], low_memory=False)
    df_original['release_year'] = pd.to_datetime(df_original['release_date'], errors='coerce').dt.year
    df_original = df_original[['title', 'release_year']].dropna()

    # Check the number of records
    assert len(df_sqlite) == len(df_original), "Mismatch in the number of records"


def test_random_samples(sqlite_connection):
    # Load the dataset into a pandas DataFrame
    df_sqlite = pd.read_sql_query("SELECT * FROM movies", sqlite_connection)

    # Load original data
    df_original = pd.read_csv('movies_metadata.csv', usecols=['title', 'release_date'], low_memory=False)
    df_original['release_year'] = pd.to_datetime(df_original['release_date'], errors='coerce').dt.year
    df_original = df_original[['title', 'release_year']].dropna().reset_index(drop=True)

    # Reset index before sample to ensure alignment
    df_sqlite = df_sqlite.reset_index(drop=True)

    # Check random samples
    sample_sqlite = df_sqlite.sample(n=10, random_state=1).reset_index(drop=True)
    sample_original = df_original.sample(n=10, random_state=1).reset_index(drop=True)

    # Assert that the samples are equal without considering the index
    pd.testing.assert_frame_equal(sample_sqlite, sample_original)