# PyDump1090fa Setup Instructions

This document will describe the setup process to use the library and run the sample application. This has not been tested running on a Raspberry Pi. Development is done on a seperate system running OpenSUSE Linux.  Installation Steps are as follows:

* Clone the PyDump1090fa repository
* Create your Python Virtual Environment
* Install the required Python Modules
* Copy the _receiverdefaults.json_ file to /etc/pydump1090fa.
* Copy the _aircraftdefaults.json_ file to /etc/pydump1090fa.


## Clone the PyDump1090 Repository

Clone the PyDump1090fa resitory. 

```bash
git clone [pydump1090_repo_name]
```
__Optional:__

Copy the repository files to a different location.  

## Setting up your Python Virtual Environment (Linux)


_**Create The Environment**_ 

From your PyDump1090fa working directory execute the following command:

```bash
python -m venv myenv
```
This creates a virtual Python environment to run PyDump1090fs from. 

_**Activate the Environment**_

To activate the enviroment use the following command:

```bash
source myenv/bin/activate
```
Once the environment is running install the python libraries. 

### Installing the Python Modules (Linux)

The following python modules are required:

__json__: For handling JSON data, reading configuration files, and parsing JSON responses.

__logging__: For logging information, warnings, and errors during the execution of the application.

__pandas__: For data manipulation and analysis. It provides powerful data structures like DataFrames to work with your aircraft data.

__requests__: For making HTTP requests to fetch aircraft data from a given URL.

__fuzzywuzzy__: For performing fuzzy string matching, which helps in matching flight data with approximate values. 

__Levinshtein__: Computation package for Lenshtein distance and edit operations, string similarity, approximage median strings, generally string averaging, string sequence and set similarity. Used in fuzzy string matching. According to the [pypi.org website](https://pypi.org/project/python-Levenshtein/), this module was renamed from _python-Levenshtein_.


Install the required Python modules:

```bash
pip install -r requirements.txt 
```
## Application Setup

There are two configuration files required for py1090Dump. Both files shoule be placed in /etc/py1090dumpfa.  


|File|Description|
|:---|:---|
|__aircraftdefaults.json__| Contans all the keys found in the aircraft.json file with default value of None for each of the keys|
|__receiverlocation.json__| For distance calculations the latitude and longitude for the Pi Aware receiver should be added to this file. Use the coordinates assigned to your Pi Aware receiver. This will be used in a future release to calulate aircraft distance from your Pi Aware system. You can also override the default URL if the script is executed remotely. |
|||

__NOTE:__ An alterative location for the aircraft.json file is http://localhost/dump1090-fa/data/aircraft.json. 


Sample receiverlocation.json file:

```json
{
    "lat": 29.9844353,
    "lon": -95.3414425,
    "url": "http://192.168.1.100:8080/skyaware/data/aircraft.json"
}
```

aircrafdefaults.json

```
{
  "now": null,
  "aircraft": [
    {
      "hex": null,
      "flight": null,
      "alt_baro": null,
      "alt_geom": null,
      "gs": null,
      "track": null,
      "geom_rate": null,
      "baro_rate": null,
      "squawk": null,
      "emergency": null,
      "category": null,
      "nav_qnh": null,
      "nav_altitude_mcp": null,
      "nav_heading": null,
      "lat": null,
      "lon": null,
      "nic": null,
      "rc": null,
      "seen_pos": null,
      "version": null,
      "nic_baro": null,
      "nac_p": null,
      "nac_v": null,
      "sil": null,
      "sil_type": null,
      "gva": null,
      "sda": null,
      "mlat": null,
      "tisb": null,
      "messages": null,
      "seen": null,
      "rssi": null,
      "nav_modes": null
    }
  ]
}
```
