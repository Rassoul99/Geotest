#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 15:56:46 2024

@author: maximeb
"""


from flask import Flask, json, request, send_file
from rdflib import Graph
from query import sparql_query
import json
import socket
import requests
import os

# Load RDF data
data = Graph()
data = data.parse("C:/Users/khadi/Documents/Datascientest 2023-2024/2023-2024/Projet geo tourisme/dst_projet_tourisme/data/flux-19287-202401180748.ttl")
# latitude_user, longitude_user, perimetre_user = generate_user_geo()

api = Flask(__name__)

@api.route('/', methods=['GET'])
def get_results():
    
    #metadata
    
    hostname=socket.gethostname()
    ip = requests.get('https://api.ipify.org').content.decode('utf8')    
        
    query_element = request.args.get('query_element')
    nom = request.args.get('nom')
    ma_lat = request.args.get('ma_lat')
    ma_lon = request.args.get('ma_lon')
    file = request.args.get('file')
   
    
    j = {'infos_utilisateur':{'nom': nom,
                                'ma_lat': ma_lat,
                                'ma_lon': ma_lon,
                                'ip_adress': ip,
                                'hostname': hostname},
         'objects':[]}
    
    queried_data = sparql_query(query_element, data)

    for row in queried_data:
        d = {'name': f'{row.name}',
             'lat': f'{row.lat}',
             'lon': f'{row.lon}'}
        j['objects'].append(d)
        
    results = json.dumps(j, ensure_ascii=False, indent=4)
    
    if file == 'true':
        
        filename = 'json_file.json'
        path = os.getcwd() + '/' + filename
        
        with open(path, 'w') as f:
            f.write(results)
        
        return send_file(path, as_attachment=True)
        
        
        
    return results

if __name__ == '__main__':
    api.run()