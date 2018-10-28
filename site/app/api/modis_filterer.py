import json


lista_bandain = ["LC_Type1", "LC_Type2", "LC_Type3",
                 "LC_Type4", "LC_Prop1", "LC_Prop2", "LC_Prop3"]


def re_scale_mcd12q1(band, data):
    result = []
    if band == "LC_Type1":
        for pixel in data:
            if pixel >= 1 and pixel <= 5:
                pixel = 7
            elif pixel == 8 or pixel == 9:
                pixel = 6
            elif pixel == 12 or pixel == 14:
                pixel = 11
            elif pixel == 13:
                pixel = 5
            elif pixel == 17:
                pixel = 10
            elif pixel == 6 or pixel == 7 or pixel == 10:
                pixel = 12
            else:
                pixel = 0
            result.append(pixel)
        return result
    if band == "LC_Type2":
        for pixel in data:
            pixel = int(pixel)
            if pixel == 0:
                pixel = 10
            elif pixel >= 1 and pixel <= 5:
                pixel = 7
            elif pixel == 8 or pixel == 9:
                pixel = 6
            elif pixel == 12 or pixel == 14:
                pixel = 11
            elif pixel == 13:
                pixel = 5
            elif pixel == 6 or pixel == 7 or pixel == 10:
                pixel = 12
            else:
                pixel = 0
            result.append(pixel)
        return result
    if band == "LC_Type3":
        for pixel in data:
            pixel = int(pixel)
            if pixel == 0:
                pixel = 10
            elif pixel >= 5 and pixel <= 8:
                pixel = 7
            elif pixel == 3 or pixel == 1:
                pixel = 11
            elif pixel == 10:
                pixel = 5
            elif pixel == 4:
                pixel = 6
            else:
                pixel = 0
            result.append(pixel)
        return result
    if band == "LC_Type4":
        for pixel in data:
            if pixel == 0:
                pixel = 10
            elif pixel == 8:
                pixel = 5
            else:
                pixel = 0
            result.append(pixel)
        return result
    if band == "LC_Prop1":

        for pixel in data:

            if pixel == 3:
                pixel = 10
            elif pixel >= 11 and pixel <= 16:
                pixel = 7
            elif pixel == 21 or pixel == 22:
                pixel = 6
            elif pixel == 31 or pixel == 41:
                pixel = 12
            else:
                pixel = 0
            result.append(pixel)
        return result
    if band == "LC_Prop2":
        for pixel in data:
            if pixel == 3:
                pixel = 10
            elif pixel == 9:
                pixel = 5
            elif pixel == 10:
                pixel = 7
            elif pixel == 20:
                pixel = 6
            elif pixel == 1:
                pixel = 15
            else:
                pixel = 0
        return result
    if band == "LC_Prop3":
        for pixel in data:
            if pixel == 3:
                pixel = 5
            elif pixel == 10:
                pixel = 7
            elif pixel == 1:
                pixel = 15
            elif pixel == 20:
                pixel = 6
        return result

    return data


def filter_mcd12q1(data):
    filtered_data = {
        "xllcorner": "3407201.74",
        "yllcorner": "4027577.41",
        "cellsize": 463.312716528,
        "nrows": 5,
        "ncols": 5,
        "band": "all",
        "latitude": 36.23109,
        "longitude": 37.99964,
        "header": "https://modis.ornl.gov/rst/api/v1/MCD12Q1/subset?latitude=36.23109&longitude=37.99964&startDate=A2010001&endDate=A2015001&kmAboveBelow=1&kmLeftRight=1",
        "subset": [
        ]
    }
    for subset in data["subset"]:
        if subset["band"] not in lista_bandain:
            continue
        subset["data"] = re_scale_mcd12q1(subset["band"], subset["data"])
        filtered_data["subset"].append(subset)
    return filtered_data


def re_scale(band, data):
    result = []
    if band == "Fpar_500m":
        for pixel in data:
            if pixel >= 250:
                pixel = 0
            else:
                pixel = pixel * 0.01
                result.append(pixel)
        return result
    if band == "Lai_500m":
        for pixel in data:
            if pixel >= 250:
                pixel = 0
            else:
                pixel = pixel*0.01
                result.append(pixel)
        return result

    return data


lista_bands_exclu = ["FparLai_QC", "FparExtra_QC",
                     "FparStdDev_500m", "LaiStdDev_500m"]


def filter_mcd15a2h(data):
    filtered_data = {
        "xllcorner": "3405348.44",
        "yllcorner": "4025724.23",
        "cellsize": 463.312716528,
        "nrows": 13,
        "ncols": 13,
        "band": "all",
                "latitude": 36.23109,
                "longitude": 37.99964,
                "header": "https://modis.ornl.gov/rst/api/v1/MCD15A2H/subset?latitude=36.23109&longitude=37.99964&startDate=A2014001&endDate=A2014049&kmAboveBelow=3&kmLeftRight=3",
                "subset": [
                ]
    }
    for subset in data["subset"]:
        if subset["band"] in lista_bands_exclu:
            continue
        subset["data"] = re_scale(subset["band"], subset["data"])
        filtered_data["subset"].append(subset)
    return filtered_data
