import requests
LAT = "34.54344"
LNG = "36.20352"
START_DATE = "A2017001"
END_DATE = "A2017001"
BASE_URL = "https://modis.ornl.gov/rst/api/v1/"

def find_in_products(products, start_date, end_date):
    result = []
    for product in products:
        result.append(get_subsets(product, start_date, end_date))
    return result


def get_dates_of_product(product, filter_str=None):
    dates = requests.get(BASE_URL + product + "/dates",
                         params={"latitude": LAT, "longitude": LNG}).json()["dates"]
    if filter_str:
        dates = list(filter(lambda x: x["calendar_date"] > filter_str, dates))
    return list(map(lambda x: x["modis_date"], dates)), list(map(lambda x: x["calendar_date"], dates))

def filter_end_dates(start_date, dates):
    return list(filter(lambda x: x > start_date, dates))


def get_subsets(product, start_date, end_date, lat=LAT, lng=LNG):
    r_data = requests.get(BASE_URL+product + "/subset", params={
                          "latitude": lat, "longitude": lng, "startDate": start_date, "endDate": end_date, "kmAboveBelow": 3, "kmLeftRight": 3})
    data = r_data.json()
    print("Got response from MODIS" + str(r_data.status_code))
    if r_data.status_code == 200:
        return data
    return None

def grab_mcd15a2h(let=None,lng=None):
    return get_subsets("MCD15A2H",START_DATE,END_DATE)

def grab_mcd12q1(let=None,lng=None):
    return get_subsets("MCD12Q1",START_DATE,END_DATE)
    