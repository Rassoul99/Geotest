#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 12:04:30 2024

@author: maxbld

Interroge la base de données à l'aide de requêtes SPARQL définies
par les préférences utilisateurs entrées dans le fichier cli.py.

"""

from rdflib import Graph

def sparql_query(query_element, data):
    
    select = "SELECT ?name ?lat ?lon "
    where = "WHERE {?restaurant rdf:type core:"+query_element+". ?restaurant rdfs:label ?name. ?restaurant core:isLocatedAt ?localisationuri. ?localisationuri schema1:geo ?geouri. ?geouri schema1:latitude ?lat ; schema1:longitude ?lon.}"
    q = select+where
    
    queried_data = data.query(q)
    
    return queried_data