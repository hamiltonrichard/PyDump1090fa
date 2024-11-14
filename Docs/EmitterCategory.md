Emitter Category ADS-B DO-260B 2.2.3.2.5.2

This information can be used to identify the aircraft category found in the aircraft.json data. I use this in the sample application to break down aircraft based on categories A1 thru A7.  

Of particular interest is category 'A6' which is used for high performance aircraft. During testing I identfied a Aero L-39 Albatros. I'm assuming if I "see" one of NASA's Northrop T-38 Talons it would fall under the 'A6' catagory as well.  

Category 'A7' has helped idenfiy helicopters operated by law enforcement agencies and television stations.  

|Category|Description|
| :---: | :--- |
|A0 | No ADS-B emitter category information. Do not use this emitter category. If no emitter category fits your installation, seek guidance from the FAA as appropriate.|
|A1 | Light (< 15500 lbs) – Any airplane with a maximum takeoff weight less than 15,500 pounds. This includes very light aircraft (light sport aircraft) that do not meet the requirements of 14 CFR § 103.1.|
|A2 | Small (15500 to 75000 lbs) – Any airplane with a maximum takeoff weight greater than or equal to15,500 pounds but less than 75,000 pounds.|
|A3 | Large (75000 to 300000 lbs) – Any airplane with a maximum takeoff weight greater than or equal to 75,000 pounds but less than 300,000 pounds that does not qualify for the high vortex category.|
|A4 |  High vortex large (aircraft such as B-757) – Any airplane with a maximum takeoff weight greater than or equal to 75,000 pounds but less than 300,000 pounds that has been determined to generate a high wake vortex. Currently, the Boeing 757 is the only example.|
|A5 | Heavy (> 300000 lbs) – Any airplane with a maximum takeoff weight equal to or above 300,000 pounds.|
|A6 | High performance (> 5g acceleration and 400 kts) – Any airplane, regardless of weight, which can maneuver in excess of 5 G’s and maintain true airspeed above 400 knots.|
|A7 | Rotorcraft – Any rotorcraft regardless of weight.|
|B0 | No ADS-B emitter category information|
|B1 | Glider / sailplane – Any glider or sailplane regardless of weight.|
|B2 | Lighter-than-air – Any lighter than air (airship or balloon) regardless of weight.|
|B3 | Parachutist / skydiver |
|B4 | Ultralight / hang-glider / paraglider – A vehicle that meets the requirements of 14 CFR § 103.1. Light sport aircraft should not use the ultralight emitter category unless they meet 14 CFR § 103.1.|
| B5 | Reserved|
| B6 | Unmanned aerial vehicle – Any unmanned aerial vehicle or unmanned aircraft system regardless of weight.|
| B7 | Space / trans-atmospheric vehicle|
| C0 | No ADS-B emitter category information|
| C1 | Surface vehicle – emergency vehicle|
| C2 | Surface vehicle – service vehicle|
| C3 | Point obstacle (includes tethered balloons)|
| C4 | Cluster obstacle|
| C5 | Line obstacle|
| C6 | Reserved |
| C7 | Reserved|

source [Emitter Category ADS-B DO-260B 2.2.3.2.5.2](https|//www.adsbexchange.com/emitter-category-ads-b-do-260b-2-2-3-2-5-2/#|~|text=A4%20%3A%20High%20vortex%20large%20%28aircraft%20such%20as,been%20determined%20to%20generate%20a%20high%20wake%20vortex.)