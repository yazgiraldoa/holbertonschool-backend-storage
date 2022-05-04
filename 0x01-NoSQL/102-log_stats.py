#!/usr/bin/env python3
"""
Python script that provides some stats
about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    gets = nginx_collection.count_documents({'method': 'GET'})
    posts = nginx_collection.count_documents({'method': 'POST'})
    puts = nginx_collection.count_documents({'method': 'PUT'})
    patchs = nginx_collection.count_documents({'method': 'PATCH'})
    deletes = nginx_collection.count_documents({'method': 'DELETE'})
    params = {'method': 'GET', 'path': '/status'}
    status_check = nginx_collection.count_documents(params)

    ips_data = nginx_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}, {"$limit": 10}
    ])

    print(f'{nginx_collection.count_documents({})} logs')
    print('Methods:')
    print(f'\tmethod GET: {gets}')
    print(f'\tmethod POST: {posts}')
    print(f'\tmethod PUT: {puts}')
    print(f'\tmethod PATCH: {patchs}')
    print(f'\tmethod DELETE: {deletes}')
    print(f'{status_check} status check')
    print('IPs:')
    for ip in ips_data:
        print(f"\t{ip.get('_id')}: {ip.get('count')}")
