# Py1090Dumpfa

Py1090Dumpfa is a python class that can retrieve flight information originating from the aircraftdata.json file found in Flight Aware's Pi Aware software. Pi Aware utlizes Dump1090, so it may be compatible with [MalcomRobb's fork](https://github.com/MalcolmRobb/dump1090) of [Antirez's dump1090](https://github.com/antirez/dump1090) as well. At this time it has only been tested with Flight Aware's [Pi Aware](https://github.com/flightaware/piaware).

This document provides information about the member functions and their usage. See the [PyDump1090 Setup documentation](https://github.com/hamiltonrichard/PyDump1090fa/blob/main/Docs/PyDump1090faSetupInstructions.md) for using the library or running the sample application. For information concerning the header information see the [Developers Notes](https://github.com/hamiltonrichard/PyDump1090fa/blob/main/Docs/DeveloperNotes.md).


## Class Initalization

_Class definition_

The class reads the configuration data from the recieverlocation.json and aircraftdefaults.json files. 

```python
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
```



## Class Methods and Sample usage

The following documentation demonstrates the use of the class member functions.

### Initalizing a Class Object
Initializes the Py1090Dumpfa object and fetches aircraft data.

```python
# Create an instance of the class
flightdata = Py1090Dumpfa()
```

### display_config()
Prints the configuration data.

```python
# Display configuration data
flightdata.display_config()
```
Returns:
```
Configuration data - Receiver URL: http://localhost:8080/skyaware/data/aircraft.json, Receiver Latitude: 29.8944353, Receiver Longitude: -95.3414425
```
### get_aircraft_data()

Retrieves aircraft data, applies defaults, and returns a DataFrame.

```python
# Get aircraft data
aircraft_data = flightdata.get_aircraft_data()
if aircraft_data is not None:
    print(aircraft_data.head())  # Print the first few rows of the DataFrame
else:
    print("No aircraft data retrieved.")
 ```   

 Returns:
 ```
       hex squawk emergency version mlat tisb  messages  seen  rssi    flight alt_baro alt_geom  ...        lon  nic     rc seen_pos nic_baro nac_p nac_v  sil sil_type  gva  sda geom_rate
0  a28e5b   4076      none     0.0   []   []         5   0.3 -20.2       N/A      N/A      N/A  ...        N/A  N/A    N/A      N/A      N/A   N/A   N/A  N/A      N/A  N/A  N/A       N/A
1  a4cb46   4636      none     2.0   []   []       139   0.1 -13.8  N408KM      800.0    750.0  ... -95.668628  9.0   75.0      0.1      1.0  10.0   2.0  3.0  perhour  2.0  2.0       N/A
2  a163f2    N/A       N/A     N/A   []   []         5   0.3 -19.1       N/A  32050.0      N/A  ...        N/A  N/A    N/A      N/A      N/A   N/A   N/A  N/A      N/A  N/A  N/A       N/A
3  a0d6fb   4035       N/A     0.0   []   []        39  17.8 -15.7       N/A   3875.0   3975.0  ... -95.361974  8.0  186.0     20.0      1.0   8.0   2.0  2.0  unknown  N/A  N/A       N/A
4  abf008    N/A       N/A     2.0   []   []       100  11.8 -16.7  SWA256    10425.0  10875.0  ... -95.164921  8.0  186.0     40.8      1.0  10.0   2.0  3.0  perhour  2.0  2.0       N/A

[5 rows x 33 columns]
```


### export_data_to_csv()

Calls get_aircraft_data and saves the data to a CSV file.

```python
# Export aircraft data to a CSV file
flightdata.export_data_to_csv('aircraft_data.csv')
```

Returns:

A csv file containing data similar to this:

```
hex,flight,alt_baro,alt_geom,gs,track,baro_rate,squawk,emergency,category,lat,lon,nic,rc,seen_pos,version,nic_baro,nac_p,nac_v,sil,sil_type,gva,sda,mlat,tisb,messages,seen,rssi
aa9d69,AJI9972 ,34000.0,35625.0,386.5,252.2,-64.0,3126,none,A3,30.532333,-95.203265,9.0,75.0,0.1,2,1.0,10.0,2.0,3.0,perhour,2.0,3.0,[],[],292,0.1,-14.4
ad3e36,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,A3,N/A,N/A,N/A,N/A,N/A,0,N/A,N/A,N/A,N/A,unknown,N/A,N/A,[],[],75,217.7,-17.6
0d0f5f,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,A3,N/A,N/A,N/A,N/A,N/A,2,N/A,N/A,N/A,N/A,perhour,N/A,N/A,[],[],4437,84.9,-17.9
a45316,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,A3,N/A,N/A,N/A,N/A,N/A,2,N/A,N/A,N/A,N/A,perhour,N/A,N/A,[],[],2529,279.6,-18.3
```

### get_aircraft_data_by_cols()

Retrieves aircraft data and, if specified, selects specific columns from the data.

```python
# Get specific columns from aircraft data
selected_columns = ['hex', 'flight', 'lat', 'lon']
aircraft_data_cols = flightdata.get_aircraft_data_by_cols(columns=selected_columns)
if aircraft_data_cols is not None:
    print(aircraft_data_cols.head())  # Print the first few rows of the DataFrame
else:
    print("No data found for the specified columns.")
```
Returns:
```
      hex    flight        lat        lon
0  a8ec94       N/A        N/A        N/A
1  abdcdc  ASH6076    29.53775 -96.198983
2  a1cb05       N/A  29.409237 -95.139017
3  a0fbfa       N/A  29.975052 -95.386209
4  a5ff76  LXJ486    29.489182 -96.232734
```
### filter_aircraft_by_col()

Filters aircraft data by a specific column and a list of one or more values.

```Python
        flightdata=Py1090Dumpfa()
        
        category_data=flightdata.filter_aircraft_by_col('category',['A1','A2'],columns)

        if category_data is not None:
            print(category_data.head())
        else:
            print("No aircraft of specified categories found")
```

Returns:

```
       hex    flight category
5   a0f86d  N1615A         A1
6   ac1d7e  N88WP          A1
9   a0bea9       N/A       A1
10  a7d626       N/A       A2
13  a0fcb4       N/A       A1
```

Notes:
The example is better suited for fuzzy_filter_aircraft_by_col(). We're tyring to look for values that aren't a match. 



### fuzzy_filter_aircraft_by_col()

Filters aircraft data by a specific column and value, allowing approximate matches based on fuzzy string similarity. 

```python
# Fuzzy filter aircraft data by flight value
fuzzy_filtered_data = flightdata.fuzzy_filter_aircraft_by_col('flight', 'SWA', columns=['hex', 'flight', 'lat', 'lon'], fuzzy_threshold=40)
if fuzzy_filtered_data is not None:
    print(fuzzy_filtered_data.head())  # Print the first few rows of the fuzzy filtered DataFrame
else:
    print("No aircraft found for the specified fuzzy flight value.")
```
Returns
```
8   abd536  SWA2901   29.993793 -95.283984
10  ac2b61  SWA814    30.288574 -96.059337
20  ab5b8c  SWA559    29.660385 -95.851012
29  a2f77b  SWA873    31.073959 -95.063297
```

__NOTE:__ This function may not return the results you want exactly. You may need to adjust the fuzzy_threshold to tweak the results. The example used was to locate flights by airline based on the flight entroduction.
