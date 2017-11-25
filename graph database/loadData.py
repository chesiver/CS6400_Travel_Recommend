import csv
import requests
import json
import time

es_base_url = {
    'destination': 'http://localhost:9200/travelsearch/destination',
}

def getNodesCSV(filename):
    with open(filename, 'r') as input, open('nodes.csv', 'w') as output:
        reader = csv.DictReader(input, delimiter=',')
        writer = csv.writer(output, delimiter=',')
        all = []
        all.append(['id:ID', 'country', 'city', 'name', 'intro'])
        url = es_base_url['destination'] + '/_search'
        exist = {}
        for row in reader:
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"country": row['country']}},
                            {"match": {"city": row['city']}},
                            {"match": {"name": row['name']}}
                        ]
                    }
                },
                "size": 1
            }
            data = requests.post(url, data=json.dumps(query)).json()
            if (len(data['hits']['hits']) > 0):
                hit = data['hits']['hits'][0]
                if (hit['_source']['country'] != row['country'] or
                    hit['_source']['city'] != row['city'] or
                    hit['_source']['name'] != row['name'] or
                    hit['_id'] in exist):
                    continue
                exist[hit['_id']] = 1
                print(row)
                print(hit)
                print()
                all.append([hit['_id']] + [row['country'], row['city'], row['name'], row['intro']])
        writer.writerows(all)


def getConnectionCSV(filename):
    url = es_base_url['destination'] + '/_search'
    with open(filename, 'r') as input, open('relations.csv', 'w') as output:
        reader = list(csv.DictReader(input, delimiter=','))
        writer = csv.writer(output, delimiter=',')
        all = []
        all.append([':START_ID', ':END_ID', 'score'])
        exist = {}
        for row in reader:
            exist[row['id:ID']] = 1
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
                    endId = hit['_id']
                    if (startId == endId or startId not in exist or endId not in exist):
                        continue
                    print(startId, endId, hit['_score'])
                    all.append([startId, endId, hit['_score']])
        writer.writerows(all)


if __name__ == '__main__':
    # getNodesCSV('wikitravel.csv')
    getConnectionCSV('nodes.csv')
    # test_country = {'type': '', 'country': 'Japan', 'name': 'Gokoku Shrine', 'city': 'Hiroshima', 'intro': "Located on the castle grounds, this concrete shrine has great significance to locals, having been rebuilt after the atomic blast and now the center for most annual Shinto traditions in the city. But other than a historical marker, there's not much to see for travelers, other than festivals (especially New Year's Eve)."}
    # print(searchCountryByIntro(test_country))