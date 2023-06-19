import requests
import json
import psycopg2
from psycopg2 import sql
from datetime import datetime

# Establish a connection to the PostgreSQL database
connection = psycopg2.connect(
    host="pgdb",  
    database="postgres",  
    user="admin",  
    password="admin"  
)
cursor = connection.cursor()  # Create a cursor object to interact with the database

# Loop through the years 2017 through to 2023
for year in range(2020, 2024):
    # Make a GET request to the Formula 1 live timing site for each year
    response = requests.get(f"https://livetiming.formula1.com/static/{year}/Index.json")
    
    # Parse the JSON response into a Python dictionary
    data = json.loads(response.content.decode('utf-8-sig'))

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

        cursor.execute("""
            SELECT circuit_id 
            FROM race_data.circuits 
            WHERE circuit_reference ILIKE %s 
            OR name ILIKE %s 
            OR location ILIKE %s
        """, (location, location, location))
        circuit_id = cursor.fetchone()

        try:
            # Insert the data into the 'events' table
            cursor.execute(
                """
                INSERT INTO race_data.events (season_id, race_round, circuit_id, official_name) 
                VALUES (%s, %s, %s, %s) 
                RETURNING event_id
                """,
                (season_id, race_round, circuit_id, official_name)
            )
        except psycopg2.Error as e:
            print("An error occurred while executing the INSERT statement:")
            print(e.pgerror)
            print(f"Query parameters were: season_id={season_id}, race_round={race_round}, circuit_id={circuit_id}, official_name={official_name}")


        #collect the event_id to update date when it's available
        event_id = cursor.fetchone()

        # Iterate over the session data for each meeting
        for session in meeting["Sessions"]:
            try:
                session_type = session["Type"]
            except KeyError:
                print("No Type found in session.")
                session_type = None  # or any default value

            try:
                session_start_date = datetime.fromisoformat(session["StartDate"]) if "StartDate" in session else None
            except Exception as e:  # To catch any error related to date formatting
                print(f"Error occurred while parsing StartDate: {e}")
                session_start_date = None

            try:
                session_end_date = datetime.fromisoformat(session["EndDate"]) if "EndDate" in session else None
            except Exception as e:  # To catch any error related to date formatting
                print(f"Error occurred while parsing EndDate: {e}")
                session_end_date = None
            
            try:
            # Assuming gmt_offset is a string in "HH:MM:SS" format.
                gmt_offset = datetime.strptime(session['gmt_offset'], "%H:%M:%S").time() if "gmt_offset" in session else None
            except Exception as e:  # To catch any error related to time formatting
                print(f"Error occurred while parsing gmt_offset: {e}")
                gmt_offset = None

            # Ensure that event_id is available, otherwise break the script
            if event_id is None:
                print("No event_id found, stopping script.")
                break  # or raise an exception to stop the script

            # Insert the session data into the 'sessions' table, ignoring any conflicts
            try:
                cursor.execute(
                    "INSERT INTO race_data.sessions (event_id, type, start_date, end_date, gmt_offset) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (session_id) DO NOTHING",
                    (event_id, session_type, session_start_date, session_end_date, gmt_offset)
                )
            except Exception as e:  # Catch any exceptions related to the execution of the SQL query
                print(f"An error occurred while inserting data into the sessions table: {e}")


    # Commit the transaction
    connection.commit()

# Close the cursor and the connection to the database
cursor.close()
connection.close()
