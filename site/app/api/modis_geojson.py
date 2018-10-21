from pyproj import Proj,transform
import json
import geojson
import math


def xy_to_latlon(x, y, dst='epsg:4326'):
    # in:  x,y as numpy arrays (ETRS-TM35FIN)
    # out: lat,lon as numpy arrays (dd.ddd, WGS84 default)
    #      (might also be lon,lat...)
    import pyproj

    proj_latlon = pyproj.Proj(init=dst) # default: WGS84
    proj_etrs = pyproj.Proj(init='epsg:3067') # ETRS-TM35FIN

    return pyproj.transform(proj_etrs, proj_latlon, x, y)


def meterDistance(Idxo,Idxf,cellSize):
    dividedCellCenterDistance = cellSize/5
    if Idxo < Idxf:
        sign = -1
    else:
        sign = 1

    if abs(Idxo - Idxf) == 1:
        distanceMeters = sign*dividedCellCenterDistance
    elif abs(Idxo - Idxf) == 0:
        distanceMeters = 0
    else:
        distanceIdx = abs(Idxo - Idxf)
        distanceMeters = ((distanceIdx-1)*sign*dividedCellCenterDistance)+distanceIdx*sign*dividedCellCenterDistance
    return distanceMeters


def toGeoJson(file):
    latitude = file["latitude"]
    longuitude = file["longitude"]
    cellsize = file["cellsize"]

    row = file["nrows"]
    col = file["ncols"]

    medX = (row-1)//2
    medY = (col-1)//2

    values = []
    for content in file['subset']:
        data = content['data']
        location = []
        for x in range(row):
            for y in range(col):

                value = data[x+y]
                dmX = meterDistance(medX,x,cellsize)
                dmY = meterDistance(medY,y,cellsize)

                Dx, Dy = xy_to_latlon(dmX,dmY)
                Nlong = longuitude + Dx/10000
                Nlat = latitude + Dy

                location.append((Nlat,Nlong))

                values.append(geojson.Feature(geometry=geojson.Point(location),
                            properties = {'values' : value}))
    return geojson.GeometryCollection(values)