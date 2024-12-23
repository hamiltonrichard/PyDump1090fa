import datetime
import json
import logging
import pandas as pd
import requests
import math # import math module for trigonometric calculations
from fuzzywuzzy import fuzz

# Pandas configuration
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)

# Configure logging
logging.basicConfig(filename='py1090dumpfa.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Py1090Dumpfa:
    """Application to process aircraft data."""

    def __init__(self):
        """Initializes the PyDump1090fa object and fetches aircraft data."""
        try:
            with open('/etc/py1090dumpfa/receiverlocation.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Validate configuration data
            if not all(key in data for key in ('rec_lat', 'rec_lon', 'url')):
                raise ValueError("Missing configuration keys in receiverlocation.json")

            self.rec_lat = data['rec_lat']
            self.rec_lon = data['rec_lon']
            self.url = data['url']

            # Load aircraft defaults
            with open('/etc/py1090dumpfa/aircraftdefaults.json', 'r', encoding='utf-8') as f:
                self.aircraft_defaults = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as exc:
            logging.error(f"Initialization failed: {exc}")
            raise RuntimeError("Unable to create PyDump1090fa object.") from exc

    def get_aircraft_data(self):
        """Retrieves aircraft data, applies defaults, and returns a DataFrame."""
        try:
            response = requests.get(self.url, timeout=5)
            response.raise_for_status()
            aircraft_data = response.json()

            # Validate aircraft data structure
            if 'aircraft' not in aircraft_data:
                raise ValueError("Invalid aircraft data format: missing 'aircraft' key")

            # Extract 'now' and convert
            data_timestamp = aircraft_data['now']
            utc_datetime = datetime.datetime.fromtimestamp(data_timestamp)

            # Convert JSON to DataFrame
            df = pd.DataFrame(aircraft_data['aircraft'])

            # Drop aircraft without position data
            df.dropna(subset=['lat', 'lon']) # Drop rows with no location data

            # Add now to the aircraft data
            df['now'] = utc_datetime.strftime('%Y-%m-%d %H:%M:%S UTC')

            # Calculate the last time an aircraft was seen
            df['last_seen'] = df['seen'].apply(lambda x:utc_datetime - datetime.timedelta(seconds=x))
            df['last_seen'] = df['last_seen'].dt.strftime('%Y-%m-%d %H:%M:%S UTC')

            # Calculate distance in nautical miles
            df['distance'] = df.apply(lambda row: self.calculate_distance(row['lon'], row['lat']), axis=1)

            # Replace NaN with "N/A"
            df = df.fillna("N/A")

            return df

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching aircraft data: {e}")
            return None

    def calculate_distance(self, aircraft_lon, aircraft_lat):
        """
        Calculate the distance between the receiver and an aircraft in nautical miles.

        Args:
            aircraft_lon (float): Longitude of the aircraft.
            aircraft_lat (float): Latitude of the aircraft.

        Returns:
            float: Distance between the receiver and the aircraft in nautical miles.
        """
        return self.haversine(self.rec_lat, self.rec_lon, aircraft_lat, aircraft_lon)

    def haversine(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great-circle distance between two points on Earth using the Haversine formula.

        Args:
            lat1 (float): Latitude of the first point in degrees.
            lon1 (float): Longitude of the first point in degrees.
            lat2 (float): Latitude of the second point in degrees.
            lon2 (float): Longitude of the second point in degrees.

        Returns:
            float: Distance between the two points in nautical miles.
        """
        # Convert degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))

        # Radius of Earth in nautical miles
        r = 3440 

        return c * r

    def display_config(self):
        """Prints the configuration data."""
        print(f"Configuration data - Receiver URL: {self.url}, "
              f"Receiver Latitude: {self.rec_lat}, "
              f"Receiver Longitude: {self.rec_lon}")

    def export_data_to_csv(self, filename='aircraft_data.csv'):
        """Calls get_aircraft_data and saves the data to a CSV file."""
        try:
            df = self.get_aircraft_data()
            if df is not None:
                df.to_csv(filename, index=False)
                logging.info(f"Aircraft data saved to {filename}")
            else:
                logging.warning("Aircraft data is None. CSV file not saved.")
        except Exception as e:
            logging.error(f"Error saving aircraft data to CSV: {e}")

    def get_aircraft_data_by_cols(self, columns=None):
        """Retrieves aircraft data and, if specified, selects specific columns from the data. It also removes rows that don't have latitude and longitude information."""
        aircraft_data_df = self.get_aircraft_data()
        if aircraft_data_df is not None:
            if columns:
                aircraft_data_df = aircraft_data_df[columns]
            if aircraft_data_df.empty:
                raise ValueError("Error: No data found for specified columns")
            return aircraft_data_df
        else:
            return None

    def filter_aircraft_by_col(self, column_name, values, columns=None):
        """Retrieves aircraft data filtered by a specific column and a list of values,
        optionally selecting specific columns."""
        aircraft_data_df = self.get_aircraft_data()
        if aircraft_data_df is not None:
            try:
                filtered_df = aircraft_data_df[aircraft_data_df[column_name].isin(values)]
                filtered_df = filtered_df.dropna(subset=['lat', 'lon']) # Drop rows with no location data

                # Check if the DataFrame is empty after filtering
                if filtered_df.empty:
                    logging.warning(f"No aircraft found with '{column_name}' in {values}.")
                    return None
                else:
                    if columns:
                        filtered_df = filtered_df[columns]
                    return filtered_df
            except KeyError:
                logging.error(f"Error: Column '{column_name}' not found in aircraft data.")
                return None
        else:
            return None

    def fuzzy_filter_aircraft_by_col(self, column_name, value, columns=None, fuzzy_threshold=40):
        """Retrieves aircraft data filtered by a specific column and value,
        allowing approximate matches based on fuzzy string similarity,
        optionally selecting specific columns."""
        aircraft_data_df = self.get_aircraft_data()
        if aircraft_data_df is not None:
            try:
                # Apply fuzzy matching to the specified column
                aircraft_data_df['similarity'] = aircraft_data_df[column_name].apply(
                    lambda x: fuzz.ratio(str(x), str(value))
                )
                filtered_df = aircraft_data_df[aircraft_data_df['similarity'] >= fuzzy_threshold]
                # filtered_df = filtered_df.dropna(subset=['lat', 'lon']) # Drop rows with no location data

                # Check if the DataFrame is empty after filtering
                if filtered_df.empty:
                    logging.warning(f"No aircraft found with '{column_name}' similar to '{value}'.")
                    return None 
                else:
                    # Select specific columns if provided
                    if columns:
                        filtered_df = filtered_df[columns]
                    return filtered_df
            except KeyError:
                logging.error(f"Error: Column '{column_name}' not found in aircraft data.")
                return None
        else:
            return None
