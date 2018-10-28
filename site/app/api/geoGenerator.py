import random
import json
import geojson

arreglo=[15,7,5,10,11,6,0,12]

originX= 36.23109
originY = 37.99964

def gen_data():
    values = []
    while len(values)<300:
        values.append(geojson.Feature(geometry = geojson.Point((originX+random.randrange(2,20)/1000, originY + random.randrange(2,20)/1000)),properties = {'values':arreglo[random.randint(0,len(arreglo)-1)]}))
    return geojson.FeatureCollection(values)
