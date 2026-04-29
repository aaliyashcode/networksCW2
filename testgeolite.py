import geoip2.database

# This reader object should be reused across lookups as creation of it is
# expensive.
with geoip2.database.Reader('GeoLite2-City.mmdb') as reader:
    response = reader.city('154.54.75.150')
    print(response.country.iso_code)