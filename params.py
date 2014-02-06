#
# Parameter file for Night Sky Orb
#   Edit parameters to match location
#

# Location lattitude and longitude of observation location:
lat = 46.4186
lon = -93.5153

# Elevation in meters of observation location:
alt = 100

# Timezone of observation location:
tz = 'US/Central'

# Starting and Ending hour of clock (must be 8 hour span for 1 matrix)
start_hr = 19
end_hr = 3

# URL of ClearDarkSky map for closest observation point with predefined map
#
#  Use Long Lake Conservation Center in Minnesota
#
clear_dark_sky_url = "http://www.cleardarksky.com/txtc/LngLkCCMNcsp.txt"

# Definition of "Good Sky"
#    Cloud Coverage: 9 = less than 10%
#                    8 = less than 20%
#                    7 = less than 30%
#                    6 = less than 40%
#                    5 = less than 50%
#                    4 = less than 60%
#                    3 = less than 70%
#                    2 = less than 80%
#                    1 = less than 90%
#
cloud_min = 7

#
#    Transparancy: 
#                  4 = perfect transparancy 
#                  3 = better than average
#                  2 = average or better transparancy
#                  1 = poor transparancy or better
#
transparancy_min = 2

#
#   Seeing:
#                  4 = Perfect Seeing
#                  3 = better than average
#                  2 = average or better seeing
#                  1 = poor seeing or better
seeing_min = 2

# URL of NASA website to parse for Two Line Element Set of ISS
nasa_url = "http://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/orbit/ISS/SVPOST.html"

