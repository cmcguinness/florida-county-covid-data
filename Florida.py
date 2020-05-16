"""
Get a snapshot of the county by county COVID-19 stats for Florida
"""
import requests
import datetime
import json

if __name__ == '__main__':
    url = 'https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/arcgis/rest/services/Florida_COVID19_Cases/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json'
    page = requests.get(url)

    if not page.ok:
        page.raise_for_status()

    json_data = json.loads(page.content)

    ts = datetime.datetime.now().strftime("%Y-%m-%d")

    f = open('data/' + ts + ' countydata.csv', 'w')
    comma = ''
    for key in json_data['features'][0]['attributes']:
        f.write(comma + key)
        comma = ','
    f.write('\n')

    for row in json_data['features']:
        comma = ''
        for key in row['attributes']:
            f.write(comma + str(row['attributes'][key]))
            comma = ','
        f.write('\n')

    f.close()
