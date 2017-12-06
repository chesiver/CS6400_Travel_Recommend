import pandas as pd

data = pd.read_csv('wikitravel.csv')
data['id'] = data.index
data = data[['id','name','city', 'country', 'intro']]
filename = "destinations.data"
with open(filename, mode="wb") as outfile:
    outfile.write(data.to_json(orient='records', lines = True))

cities = data['city'].drop_duplicates()
cities.index = pd.RangeIndex(len(cities.index))
cities = cities.to_frame()
cities['id'] = cities.index
cities = cities[['id', 'city']]
filename = "cities.data"
with open(filename, mode="wb") as outfile:
    outfile.write(cities.to_json(orient='records', lines = True))

countries = data['country'].drop_duplicates()
filename = "countries.data"
with open(filename, mode="wb") as outfile:
    for country in countries:
         outfile.write("{\"country\":" + "\"" + country + "\"" + "}\n")
            
countries = data['country'].drop_duplicates()
countries.index = pd.RangeIndex(len(countries.index))
countries = countries.to_frame()
countries['id'] = countries.index
countries = countries[['id', 'country']]
filename = "countries.data"
with open(filename, mode="wb") as outfile:
    outfile.write(countries.to_json(orient='records', lines = True))

outfile = "travel.data"

dest_index = "{\"index\": {\"_index\": \"travelsearch\", \"_type\": \"destination\"}}" + "\n"
city_index = "{\"index\": {\"_index\": \"travelsearch\", \"_type\": \"cities\"}}" + "\n"
country_index = "{\"index\": {\"_index\": \"travelsearch\", \"_type\": \"countries\"}}"+ "\n"

with open(outfile, mode="wb") as outfile:
    with open('destinations.data', mode="r") as infile:
        for line in infile:
            outfile.write(dest_index)
            outfile.write(line)
    with open('cities.data', mode="r") as infile:
        for line in infile:
            outfile.write(city_index)
            outfile.write(line)
    with open('countries.data', mode="r") as infile:
        for line in infile:
            outfile.write(country_index)
            outfile.write(line)