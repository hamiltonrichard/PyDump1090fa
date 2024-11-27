# Developer's Notes

## __aircraft.json Breakdown__
The aircraft.json file can be broken down into the following details:

| Header    | Type    | Description                                         |
|-----------|---------|-----------------------------------------------------|
| hex       | String  | Unique aircraft identifier in hexadecimal format.   |
| flight    | String  | Flight identifier, typically a tail number or callsign. |
| alt_baro  | Integer | Barometric altitude in feet.                        |
| alt_geom  | Integer | Geometric altitude in feet.                         |
| gs        | Float   | Ground speed in knots.                              |
| track     | Float   | Track angle in degrees.                             |
| geom_rate | Integer | Rate of climb or descent in feet per minute.        |
| squawk    | String  | Transponder code assigned to the aircraft.          |
| emergency | String  | Emergency status of the aircraft.                   |
| category  | String  | Aircraft category indicating size and type.         |
| lat       | Float   | Latitude of the aircraft's position.                |
| lon       | Float   | Longitude of the aircraft's position.               |
| nic       | Integer | Navigation Integrity Category.                      |
| rc        | Integer | Radius of Containment in meters.                    |
| seen_pos  | Float   | Time in seconds since the last position update.     |
| version   | Integer | Version of the ADS-B system.                        |
| nic_baro  | Integer | Barometric Navigation Integrity Category.           |
| nac_p     | Integer | Navigation Accuracy Category for position.          |
| nac_v     | Integer | Navigation Accuracy Category for velocity.          |
| sil       | Integer | Surveillance Integrity Level.                       |
| sil_type  | String  | Type of Surveillance Integrity Level.               |
| gva       | Integer | Geometric Vertical Accuracy.                        |
| sda       | Integer | System Design Assurance level.                      |
| mlat      | Array   | Multilateration data (usually empty if not used).   |
| tisb      | Array   | Traffic Information Service Broadcast data.         |
| messages  | Integer | Total number of ADS-B messages received.            |
| seen      | Float   | Time in seconds since the last message was seen.    |
| rssi      | Float   | Received Signal Strength Indicator in dBm.          |
| last_seen | Float   | Calculated field: now - seen |
## __Data Absence__

Information in _aircraft.json_ dependant on what gets reported. This can include:

* Absence of the flight identifier (__flight__) - Callsigns are assigned by Air Traffic Controllers
* Absence of Multiateration data (__mlat__) - Reaons include the lack of mlat equpiment in the aircraft, equipment issues or environmental issues. 
* Absence of Traffic Information Service Broadcast date (__tisb__) - Same reasons for Multiateration information. 
* Configuration of PiAware. _See Multiateration Configuration_.

__Multiateration  Configuration__

MLAT configuration info from the [Piware Advanced Configuration Guide](https://www.flightaware.com/adsb/piaware/advanced_configuration):

| Config Name | Options | Default Value | Notes |
|-------------|---------|---------------|-------|
|allow-mlat|yes or no|yes| if _yes_, multilateration is enabled (also requires that receiver location is set on the FlightAware My ADS-B stats page)|
|mlat-results|yes or no	|yes| if _yes_, multilateration results are returned to PiAware from FlightAware|
|mlat-results-format|(see below)|(defaults below)|configures which ports/formats multilateration results are returned on|
|mlat-results-anon|yes or no|yes|if _yes_, mlat positions for blocked aircraft are returned with anonymized TIS-B addresses.
if no, mlat positions for blocked aircraft are not returned|



## Grouping Information

There are several combinations of data which could prove to be useful.  

## Positional information

| Header    | Type    | Description                                         |
|-----------|---------|-----------------------------------------------------|
| hex       | String  | Unique aircraft identifier in hexadecimal format.   |
| flight    | String  | Flight identifier, typically a tail number or callsign. |
| lat       | Float   | Latitude of the aircraft's position.                |
| lon       | Float   | Longitude of the aircraft's position.               |
| alt_baro  | Integer | Barometric altitude in feet.                        |
| alt_geom  | Integer | Geometric altitude in feet.                         |
| gs        | Float   | Ground speed in knots.                              |
| track     | Float   | Track angle in degrees.                             |
| geom_rate | Integer | Rate of climb or descent in feet per minute.        |
| gs        | Float   | Ground speed in knots.                              |
| track     | Float   | Track angle in degrees.                             |
| seen_pos  | Float   | Time in seconds since the last position update.     |



## Flight Status Information

| Header    | Type    | Description                                         |
|-----------|---------|-----------------------------------------------------|
| hex       | String  | Unique aircraft identifier in hexadecimal format.   |
| flight    | String  | Flight identifier, typically a tail number or callsign. |
| squawk    | String  | Transponder code assigned to the aircraft.          |
| emergency | String  | Emergency status of the aircraft.                   |
| category  | String  | Aircraft category indicating size and type.         |
| nic       | Integer | Navigation Integrity Category.                      |
| rc        | Integer | Radius of Containment in meters.                    |
| version   | Integer | Version of the ADS-B system.                        |
| nic_baro  | Integer | Barometric Navigation Integrity Category.           |
| nac_p     | Integer | Navigation Accuracy Category for position.          |
| nac_v     | Integer | Navigation Accuracy Category for velocity.          |
| sil       | Integer | Surveillance Integrity Level.                       |
| sil_type  | String  | Type of Surveillance Integrity Level.               |
| gva       | Integer | Geometric Vertical Accuracy.                        |
| sda       | Integer | System Design Assurance level.                      |


## Abbreaveated Flight status info

| Header    | Type    | Description                                         |
|-----------|---------|-----------------------------------------------------|
| hex       | String  | Unique aircraft identifier in hexadecimal format.   |
| flight    | String  | Flight identifier, typically a tail number or callsign. |
| lat       | Float   | Latitude of the aircraft's position.                |
| lon       | Float   | Longitude of the aircraft's position.               |

## Type Information

| Header    | Type    | Description                                         |
|-----------|---------|-----------------------------------------------------|
| hex       | String  | Unique aircraft identifier in hexadecimal format.   |
| category  | String  | Aircraft category indicating size and type.         |


## __Additional Canidates for Dataframes__

## Multilateration (MLAT) Details

* _Position Data_: Provides accurate position information of aircraft by triangulating signals from multiple ground-based stations.

* _Identification_: Can include aircraft identification if available.

* _Altitude_: Provides altitude information of the aircraft.

* _Velocity_: Offers speed and direction data.

## Traffic Information Service-Broadcast (TIS-B)

* _Position Data_: Provides accurate position information of aircraft, including those not equipped with ADS-B1.

* _Identification_: Includes identification data when available.

* _Altitude_: Provides altitude information.

* _Velocity_: Offers speed and direction data.

* Traffic Information: Enhances situational awareness by providing information about nearby traffic, including non-ADS-B equipped aircraft.

## __Data Considerations__

## Time Conversion
All time values are stored in epoch format. They will need to be converted.

__Time Conversion__

The following code can be used to convert time data in epoch format. 

```python
            # Add now to the aircraft data
            df['now'] = utc_datetime.strftime('%Y-%m-%d %H:%M:%S UTC')

            # Calculate the last time an aircraft was seen
            df['last_seen'] = df['seen'].apply(lambda x:utc_datetime - datetime.timedelta(seconds=x))
            df['last_seen'] = df['last_seen'].dt.strftime('%Y-%m-%d %H:%M:%S UTC')

            # Calculate distance in nautical miles
            df['distance'] = df.apply(lambda row: self.calculate_distance(row['lon'], row['lat']), axis=1)
```




## __Distance Information__

Using the coordinates of the aircraft and the piaware reciever, the following code is used to calculate the distance. Using the coordinates of the aircraft and the piaware reciever, the following cod could be modfied to calculate the distance. 

Latitude and Longitude for the reciever is in _recieverlocation.json_. Latitude and longitude can be access as follows:

Latitude and Longitude for the reciever is in _recieverlocation.json_. Latitude and longitude can be access as follows:


## Distance code


```python 

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
```
The source of the code came from [The Where-To Github Repository](https://github.com/CS3216-WhereTo/where-to/blob/master/back_end/WhereTo/routes/routing_helper.py)

 
## __Display Options__

Flight data could be displayed in sequence. THe following code explains how this could be possible:

```python
 def get_data():
    # Your data retrieval logic
    print("Getting data...")

def show_data1():
    # Your data display logic for show_data1
    print("Showing data 1...")

def show_data2():
    # Your data display logic for show_data2
    print("Showing data 2...")

def show_data3():
    # Your data display logic for show_data3
    print("Showing data 3...")

# List of show_data functions
show_functions = [show_data1, show_data2, show_data3]

# Loop to execute get_data() and cycle through show_data functions
for i in range(9):  # Adjust the range as needed
    get_data()
    show_function = show_functions[i % len(show_functions)]
    show_function()
```

## Database Sources

The FAA Registration Database can be [downloaded](https://www.faa.gov/licenses_certificates/aircraft_certification/aircraft_registry/releasable_aircraft_download) for different years. This may be helpful for providing additional details based on registration. 
