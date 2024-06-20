import json

def seed(es_client, target_index):
    print(f"Checking if {target_index} should be seeded.")
    all_query = {"query": {"match_all": {}}}

    results = es_client.search(index=target_index, body=all_query)
    count = results["hits"]["total"]["value"]

    if count == 0:
        print("Need to seed index as it is empty.")
        if target_index == "datasources":
            print("Seeding datasources")
            for source in json.load(open("/backend/api/seeds.json")):
                body = json.dumps(source)
                es_client.index(index=target_index, body=body)
    else:
        print("No need to seed as it is not empty.")
