import json
import logging
import pandas as pd
import requests
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
            if not all(key in data for key in ('lat', 'lon', 'url')):
                raise ValueError("Missing configuration keys in receiverlocation.json")

            self.latitude = data['lat']
            self.longitude = data['lon']
            self.url = data['url']

            # Load aircraft defaults
            with open('/etc/py1090dumpfa/aircraftdefaults.json', 'r', encoding='utf-8') as f:
                self.aircraft_defaults = json.load(f)

            # Initialize aircraft data as a DataFrame
            self.aircraft_data = pd.DataFrame()

            # Fetch aircraft data upon initialization
            self.aircraft_data = self.get_aircraft_data()

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

            # Convert JSON to DataFrame
            df = pd.DataFrame(aircraft_data['aircraft'])

            # Replace NaN with "N/A"
            df = df.fillna("N/A")
            return df

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching aircraft data: {e}")
            return None

    def display_config(self):
        """Prints the configuration data."""
        print(f"Configuration data - Receiver URL: {self.url}, "
              f"Receiver Latitude: {self.latitude}, "
              f"Receiver Longitude: {self.longitude}")

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

    def get_aircraft_location_data(self):
        """Drop entries with no latitude and longitude data"""
        aircraft_data_df = self.get_aircraft_data()
        if aircraft_data_df is not None:
            aircraft_data_df = aircraft_data_df.dropna(subset=['lat', 'lon'])
        return aircraft_data_df

    def filter_aircraft_by_colX(self, column_name, columns=None):
        """Retrieves aircraft data filtered by a specific column and a list of values,
        optionally selecting specific columns."""
        aircraft_data_df = self.get_aircraft_data()
        if aircraft_data_df is not None:
            try:
                filtered_df = aircraft_data_df[aircraft_data_df[column_name]]
                filtered_df = filtered_df.dropna(subset=['lat', 'lon'])  # Drop rows with no location data

                # Check if the DataFrame is empty after filtering
                if filtered_df.empty:
                    logging.warning(f"No aircraft found with '{column_name}'.")
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
        
    def filter_aircraft_by_col(self, column_name, values, columns=None):
        """Retrieves aircraft data filtered by a specific column and a list of values,
        optionally selecting specific columns."""
        aircraft_data_df = self.get_aircraft_data()
        if aircraft_data_df is not None:
            try:
                filtered_df = aircraft_data_df[aircraft_data_df[column_name].isin(values)]
                filtered_df = filtered_df.dropna(subset=['lat', 'lon'])  # Drop rows with no location data

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
                filtered_df = filtered_df.dropna(subset=['lat', 'lon'])  # Drop rows with no location data

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
