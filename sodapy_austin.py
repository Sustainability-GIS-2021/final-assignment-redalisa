# run pip install sodapy before running 
# code from https://dev.socrata.com/foundry/data.austintexas.gov/egpd-hqdi
from sodapy import Socrata
# Extract data from zip file
# Crash Fatality data 2019 Austin TX
client = Socrata("data.austintexas.gov", None)
results = client.get("egpd-hqdi")
# Convert to pandas DataFrame
crash_aust = pd.DataFrame.from_records(results)

crash_aust['x_coord'] = crash_aust['x_coord'].astype('float')
crash_aust['y_coord'] = crash_aust['y_coord'].astype('float')

# creating a geometry column 
geometry = [Point(xy) for xy in zip(crash_aust['x_coord'], crash_aust['y_coord'])]
# Creating a Geographic data frame 
A_crash_stats = gpd.GeoDataFrame(crash_aust, crs=CRS("WGS84"), geometry=geometry)

# Rename columns with names over 10 characters long in order to save the file properly 

A_crash_stats = A_crash_stats.rename(columns={"fatal_crash_number": "crash_num", 
                                              "number_of_fatalities": "fatalities",
                                             "case_number":"case_num", "killed_driver_pass":"driver_pass",
                                             "ran_red_light_or_stop_sign":"red_stop", "dl_status_incident": "dl_status",
                                             "suspected_impairment": "impaired", "restraint_type": "restaint",
                                             "type_of_road" : "road_type", "failure_to_stop_and_render": "fail_stop"})
                                             
A_crash_stats.to_file("data/crash_stats_Austin.shp")