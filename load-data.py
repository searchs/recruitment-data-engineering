import requests  # For making HTTP requests
import json
import psycopg2  # For interacting with PostgreSQL database
from psycopg2 import sql  # For constructing SQL statements
from datetime import datetime  # For date and time functionality

# Make a GET request to the Formula 1 live timing site for the 2023 season data
response = requests.get("https://livetiming.formula1.com/static/2023/Index.json")

# Parse the JSON response into a Python dictionary
data = json.loads(response.content.decode('utf-8-sig'))

# Establish a connection to the PostgreSQL database
connection = psycopg2.connect(
    host="pgdb",  # Database server host
    database="postgres",  # Database name
    user="admin",  # Database user
    password="admin"  # User password
)
cursor = connection.cursor()  # Create a cursor object to interact with the database

# Extract the season data
season = data["Year"]

# Get the season_id from the season table using the year and championship short_name
cursor.execute(
    """
    SELECT season_id 
    FROM race_data.season 
    LEFT JOIN race_data.championship as c USING (championship_id)
    WHERE c.short_name = 'Formula 1' AND year = %s
    """, 
    (season,)
)
# Get season_id for the data
season_id_row = cursor.fetchone()
if season_id_row is None:
    print(f"No season_id found for year {season}")
else:
    season_id = season_id_row[0]


# Iterate over the meetings data
for meeting in data["Meetings"]:
    # Extract necessary data from each meeting
    country_name = meeting["Country"]["Name"]
    circuit_name = meeting["Circuit"]["ShortName"]
    race_name = meeting["Name"]
    location = meeting["Location"]
    official_name = meeting["OfficialName"]
    race_round = meeting["Number"]
    year = data["Year"]

    # Get the circuit_id from the circuits table using the location
    #cursor.execute("SELECT circuit_id FROM race_data.circuits WHERE location = %s", (location,))
    cursor.execute("""
        SELECT circuit_id 
        FROM race_data.circuits 
        WHERE circuit_reference ILIKE %s 
        OR name ILIKE %s 
        OR location ILIKE %s
    """, (location, location, location))
    circuit_id = cursor.fetchone()

    # Insert the data into the 'events' table
    cursor.execute(
        """
        INSERT INTO race_data.events (season_id, race_round, circuit_id, official_name) 
        VALUES (%s, %s, %s, %s) 
        RETURNING event_id
        """,
        (season_id, race_round, circuit_id, official_name)
    )

    #collect the event_id to update date when it's available
    event_id = cursor.fetchone()

    # Iterate over the session data for each meeting
    for session in meeting["Sessions"]:
        # Extract necessary data from each session
        session_id = session["Key"]
        session_type = session["Type"]
        session_start_date = datetime.fromisoformat(session["StartDate"])
        session_end_date = datetime.fromisoformat(session["EndDate"])

        # Insert the session data into the 'sessions' table, ignoring any conflicts
        cursor.execute(
            "INSERT INTO race_data.sessions (session_id, event_id, type, start_date, end_date) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (session_id) DO NOTHING",
            (session_id, event_id, session_type, session_start_date, session_end_date)
        )

# Commit the transaction
connection.commit()

# Close the cursor and the connection to the database
cursor.close()
connection.close()
