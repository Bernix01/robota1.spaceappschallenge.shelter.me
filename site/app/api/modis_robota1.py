from .modis_filterer import filter_mcd12q1, filter_mcd15a2h
from .modis_grabber import grab_mcd12q1, grab_mcd15a2h
from .modis_geojson import toGeoJson

def do_mcd12q1():
    modis_data = grab_mcd12q1()
    filtered_modist_data = filter_mcd12q1(modis_data)
    return toGeoJson(filtered_modist_data)


def do_mcd15a2h():
    modis_data = grab_mcd15a2h()
    filtered_modist_data = filter_mcd15a2h(modis_data)
    return toGeoJson(filtered_modist_data)
