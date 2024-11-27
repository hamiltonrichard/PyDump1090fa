"""Main application"""
import time
from py1090dumpfa_lib import Py1090Dumpfa
if __name__ == "__main__":
    try:
        # Create the flightdata object outside the loop
        flightdata = Py1090Dumpfa()
        flight_columns=['hex','flight','track','gs','alt_baro','lat','lon','now','seen','last_seen']
        flight_columns_emergency = ['hex','flight','track','gs','alt_baro','lat','lon', 'squawk','emergency']
        flight_distance=['hex','flight','distance'] 
        command_index = 0 # Initialize the command index

        while True:
            # Define the list of commands with titles and print statements
            commands = [
               ("Light Aircraft (A1)", lambda: print(flightdata.filter_aircraft_by_col('category', ['A1'],flight_distance))), 
               ("Small Aircraft (A2)", lambda: print(flightdata.filter_aircraft_by_col('category', ['A2'],flight_distance))), 
               ("Large Aircraft (A3)", lambda: print(flightdata.filter_aircraft_by_col('category', ['A3'],flight_distance))), 
               ("Large High Vortext Aircraft (A4)", lambda: print(flightdata.filter_aircraft_by_col('category', ['A4'],flight_distance))), 
               ("Heavy Aircraft (A5)", lambda: print(flightdata.filter_aircraft_by_col('category', ['A5'],flight_distance))), 
               ("High Performance Aircraft (A6)", lambda: print(flightdata.filter_aircraft_by_col('category', ['A6'],flight_distance))), 
               ("Rotor Aircraft (A7)", lambda: print(flightdata.filter_aircraft_by_col('category', ['A7'],flight_distance))), 
               ("Air France",lambda: print(flightdata.fuzzy_filter_aircraft_by_col('flight','AFR',flight_columns))), 
               ("Air Transport International", lambda: print(flightdata.fuzzy_filter_aircraft_by_col('flight','ATN',flight_columns))),
               ("Alaska Airlines",lambda: print(flightdata.fuzzy_filter_aircraft_by_col('flight','ASA',flight_columns))), 
               ("Commute Air",lambda: print(flightdata.fuzzy_filter_aircraft_by_col('flight','UCA',flight_columns))), 
               ("Delta Airlines",lambda: print(flightdata.fuzzy_filter_aircraft_by_col('flight','DAL',flight_columns))), 
               ("DHL",lambda: print(flightdata.fuzzy_filter_aircraft_by_col('flight','DHL',flight_columns))), 
               ("EVA Air",lambda: print(flightdata.fuzzy_filter_aircraft_by_col('flight','EVA',flight_columns))), 
               ("FedEx",lambda: print(flightdata.fuzzy_filter_aircraft_by_col('flight','FDX',flight_columns))), 
               ("Flex Jet",lambda: print(flightdata.fuzzy_filter_aircraft_by_col('flight','LXJ',flight_columns))), 
               ("Hera Flight",lambda: print(flightdata.fuzzy_filter_aircraft_by_col('flight','HER',flight_columns))), 
               ("Jet Blue",lambda: print(flightdata.fuzzy_filter_aircraft_by_col('flight','JBU',flight_columns))), 
               ("KLM",lambda: print(flightdata.fuzzy_filter_aircraft_by_col('flight','KLM',flight_columns))), 
               ("Mesa",lambda: print(flightdata.fuzzy_filter_aircraft_by_col('flight','ASH',flight_columns))), 
               ("Sky West",lambda: print(flightdata.fuzzy_filter_aircraft_by_col('flight','SKW',flight_columns))), 
               ("Southwest Airlines",lambda: print(flightdata.fuzzy_filter_aircraft_by_col('flight','SWA',flight_columns))), 
               ("Spirit",lambda: print(flightdata.fuzzy_filter_aircraft_by_col('flight','NKS',flight_columns))), 
               ("United Airlines",lambda: print(flightdata.fuzzy_filter_aircraft_by_col('flight','UAL',flight_columns))), 
               ("Volaris",lambda: print(flightdata.fuzzy_filter_aircraft_by_col('flight','VOI',flight_columns))) 
            ]

            print('\033c') 

            # Update the aircraft_data attribute within the loop
            flightdata.aircraft_data = flightdata.get_aircraft_data() 

            if not flightdata.aircraft_data.empty:
                # Clear the screen and print the title and command output
                print('\033c') 
                title, command = commands[command_index]
                print(f"=== {title} ===")
                command() 

                command_index = (command_index + 1) % len(commands) # Move to the next command
                time.sleep(5) 

    except RuntimeError as e:
        print(f"Error: {e}")
