# Class FileGeocoder
# This class is modeled on geopy's geocoder class. While it is not a formal
# part of geopy, it does implement a geocode() method that is plug compatible
# with geopy's geocoders (e.g. ArcGIS, GoogleV3, Nominatim, etc.)
#
# Why would you want to use this class instead? Because all the aforementioned
# geocoders will shut you down after a few hundred API calls unless you pay
# for their service and Data Science students are poor. Also, even if you pay,
# real geocoder API calls are *slow*. So, if you have to geocode 130,000 places,
# as the author recently had too, you want something that is both free and
# fast.
#
# Enter the FileGeocoder. Upon initialization
#   FileGeocoder()
# it loads a very large csv file that associates US cities, towns, and counties
# with latitudes and longitudes. You can then make calls to it like
#   geocoder.geocode("Boulder, CO")
# and it should return to you a geopy location object with the lat, long of
# Boulder filled in. The current implementation cannot deal with street addresses
# or non-US towns, but if you need to geocode a list of places like
#   ['Camp McGregor, NM',
#     'El Mirage, AZ',
#     'York, NE',
#     'Onchiota, NY',
#     'Lawrence, KS',
#     'Phoenix, AZ',
#     'Houston, TX',
#     'Phoenix, AZ',
#     'Beaverton, OR',
#     'Taft, CA',
#     'Goose Creek, SC']
# it should do the trick free and fast.

from geopy.location import Location # for compatibility with geopy geocoders
from geopy.location import Point
import pandas as pd
import numpy as np

class FileGeocoder:

    def __init__(self, file_name = '../data/US_lat_long.csv'):
        US_lat_long = pd.read_csv(file_name)
        self.places = {}
        for i in range(US_lat_long.shape[0]):
            place = US_lat_long.iloc[i,:]
            self.places[(place.city, place.state)] = (place.latitude, place.longitude)

    def geocode(self, query):
        '''Return a geopy.location.Location object with lat, long of a query strings
        which is expected to be in the format of "city, two char state code",
        e.g. "Boulder, CO" or "Houston, TX"
        Or return None of it cannot geocode the query string
        This method is written to be compatible with the geocode method of
        geopy geocoder classes like GoogleV3, ArcGIS, and Novatim, which all have a
        geocode method. FileGeocoder's implementation is much more restrictive since
        it cannot deal with street addresses or non-US locations, but it is cheap and
        fast.
        '''
        tokens = query.split(',')
        if len(tokens)<=1:
            return None
        city = tokens[0].lstrip().rstrip()
        state = tokens[1].lstrip().rstrip()
        key = (city, state)
        if key in self.places:
          lat, long = self.places[key]
          if np.isnan(lat) or np.isnan(long):
              return None
          point = Point(latitude=lat, longitude=long)
          loc = Location(address = city + ', ' + state, point=point)
        else:
          loc = None
        return loc
