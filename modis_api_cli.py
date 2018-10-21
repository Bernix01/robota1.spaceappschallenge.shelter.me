import requests
from pick import pick
LAT = "36.23109"
LNG = "37.99964"
START_DATE = "2008-01-01"
END_DATE = "2009-12-31"
BASE_URL = "https://modis.ornl.gov/rst/api/v1/"
PRODUCTS_NAME = []
PRODUCTS = []


def setup_products():
    products_req = requests.get(BASE_URL + "products").json()
    PRODUCTS_NAME = list(map(lambda x: x["product"], products_req["products"]))
    PRODUCTS_NAME.append("All")
    PRODUCTS = products_req["products"] + \
        [{"product": "all", "description": "Search in all products"}]
    print("Found " + str(len(PRODUCTS)) + "products. Choose one")
    return PRODUCTS_NAME, PRODUCTS


def find_in_products(products, *args):
    for product in products:
        pass


def find_in_product(product):
    res = requests.get(BASE_URL)


def get_dates_of_product(product, filter_str=None):
    dates = requests.get(BASE_URL + product + "/dates",
                         params={"latitude": LAT, "longitude": LNG}).json()["dates"]
    if filter_str:
        dates = list(filter(lambda x: x["calendar_date"] > filter_str, dates))
    return list(map(lambda x: x["modis_date"], dates)), list(map(lambda x: x["calendar_date"], dates))


def filter_end_dates(start_date, dates):
    return list(filter(lambda x: x > start_date, dates))


def get_subset(product, start_date, end_date):
    r_data = requests.get(BASE_URL+product + "/subset", params={
                          "latitude": LAT, "longitude": LNG, "startDate": start_date, "endDate": end_date, "kmAboveBelow": 3, "kmLeftRight": 3})
    data = r_data.json()
    import json
    with open(product+"_"+start_date+"_"+end_date+"_"+LAT+"_"+LNG+'.json', 'w') as outfile:
        json.dump(data, outfile)
    return r_data.status_code == 200


if __name__ == "__main__":
    PRODUCTS_NAME, PRODUCTS = setup_products()
    title = "Found " + str(len(PRODUCTS)) + \
        "products. Choose one to search in:"
    curr_prod, index = pick(PRODUCTS_NAME, title)
    print("Searching for " + curr_prod)
    print(PRODUCTS[index]["description"])
    date_filter_str = input("Enter search start filter: ")
    MODIS_DATES, CALENDAR_DATES = get_dates_of_product(
        curr_prod, date_filter_str)
    title = "Choose start date"
    cal_start_date, index_sdate = pick(CALENDAR_DATES, title)
    modis_start_date = MODIS_DATES[index_sdate]
    title = "Choose end date"
    cal_end_date, index_edate = pick(filter_end_dates(
        cal_start_date, CALENDAR_DATES), title)
    modis_end_date = MODIS_DATES[index_edate]
    print("Ok, so searching for " + curr_prod)
    print(PRODUCTS[index]["description"])
    print("From " + cal_start_date + "(" + modis_start_date +
          ") To: " + cal_end_date + "(" + modis_end_date + ")")
    if get_subset(curr_prod, modis_start_date, modis_end_date):
        print("Done!")
    else:
        print("Fail!")
