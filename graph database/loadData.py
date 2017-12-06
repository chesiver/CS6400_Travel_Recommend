import csv
import requests
import json
import time

es_base_url = {
    'destination': 'http://localhost:9200/travelsearch/destination',
}

def getNodesCSV(filename):
    with open(filename, 'r') as input, open('nodes.csv', 'w') as output:
        reader = csv.reader(input, delimiter=',')
        writer = csv.writer(output, delimiter=',')
        writer.writerow(['id:ID', 'country', 'city', 'name', 'intro'])
        for row in reader:
            writer.writerow(row)


def getConnectionCSV(filename):
    url = es_base_url['destination'] + '/_search'
    with open(filename, 'r') as input, open('relations.csv', 'w') as output:
        reader = csv.DictReader(input, delimiter=',')
        writer = csv.writer(output, delimiter=',')
        writer.writerow([":START_ID", ":END_ID", "score"])
        for row in reader:
            startId = row['id:ID']
            query = {
                "query": {
                    "match": {
                        "intro": row['intro']
                    }
                },
                "size": 10
            }
            data = requests.post(url, data=json.dumps(query)).json()
            if (len(data['hits']['hits']) > 0):
                for hit in data['hits']['hits'][1:]:
                    destination = hit['_source']
                    endId = destination['id']
                    if startId == endId: continue
                    print(startId, endId, hit['_score'])
                    writer.writerow([startId, endId, hit['_score']])


if __name__ == '__main__':
    # getNodesCSV('./../data/wikitravel.csv')
    getConnectionCSV('./nodes.csv')
    # test_country = {'type': '', 'country': 'Japan', 'name': 'Gokoku Shrine', 'city': 'Hiroshima', 'intro': "Located on the castle grounds, this concrete shrine has great significance to locals, having been rebuilt after the atomic blast and now the center for most annual Shinto traditions in the city. But other than a historical marker, there's not much to see for travelers, other than festivals (especially New Year's Eve)."}
    # print(searchCountryByIntro(test_country))