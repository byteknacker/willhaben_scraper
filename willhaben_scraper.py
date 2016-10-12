import numpy as np
from bs4 import BeautifulSoup
import urllib2

url_root = "https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote"
VIENNA_area_id = 900

areaId = VIENNA_area_id # selects geographic search location, in this case Vienna
viewed_page = 9 # can change this one during iteration
modifier = "?areaId={}&page={}&view=&nonewsearch=true".format(areaId, viewed_page)

print modifier

# download page by viewed_page count, start with one
address = url_root + modifier
response = urllib2.urlopen(address)
soup = BeautifulSoup(response.read(), "lxml")

def wh_number_format(dirty_num):
    # willhaben follows thousand-dot-number-comma-decimals format, hence:
    # minus sign at end goes away
    dirty_num = dirty_num.replace("-","").strip()
    # dots in middle and end of number go away
    dirty_num = dirty_num.replace(".","")
    #commas become dots
    dirty_num = dirty_num.replace(",",".")
    #trailing dots go away, dots in middle can stay:
    if dirty_num[-1] == ".":
        dirty_num = dirty_num[:-1]
    return float(dirty_num)

#test_case = ["1000", "1.200,04", "1.200,40","3,384"]
#print [wh_number_format(x) for x in test_case]

# apartment_array = np.array([0, u'EVA Immobilien', 95.0, 4, 1210.0])

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False



willhaben_data = []
#title row:
willhaben_data.append(["id", "owner", "sq. meters", "num_rooms", "zipcode"])

counter = 0
max_counter = 20

for li in soup.find_all("li", {"itemtype": "http://schema.org/Residence"}):
    description = li.find("span", {"class" : "desc-left"}).get_text()
    # extract sq m (span class desc-left), anzahl zimmer (span class wh-pipe)
    sqm = float(description.replace(" ", "").split()[0][:-2])
    try:
        num_rooms = int(description.replace(" ", "").split()[1].replace("Zimmer",""))
    except IndexError:
        num_rooms = "nan"
    # extract rent(span class pull-right, dot denotes thousands, comma denotes decimal places)
    rent = wh_number_format(li.find("span", {"class": "pull-right"}).get_text())
    # extract zip code
    # extract address (address-lg)
    address_text = li.find("span", {"class": "address-lg"}).get_text().split()
    # okay but inefficient:
    # zipcode = [zipcode for zipcode in address_text if len(zipcode) == 4 and is_number(zipcode)][0]
    # more straightforward:
    zipcode = li.find("span", {"class": "address-lg"}).get_text().split("\n")[-10]
    # extract owner / contact (comes after the <br> in the address span)
    owner =  li.find("span", {"class": "address-lg"}).get_text().split("\n")[-3].strip()
    # add row to array: id, name, sqmeters, numrooms, rent, zip
    new_row = [counter, owner, sqm, num_rooms, zipcode]
    willhaben_data.append(new_row)
    counter += 1
    if counter > max_counter:
        break

data_array = np.asarray(willhaben_data[1:])


print willhaben_data








