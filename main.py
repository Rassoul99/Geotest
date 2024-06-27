#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 13:01:31 2024

@author: maxbld

Orchestre les différents modules.

"""

from generate import generate_user_geo
import cli
from extract import data
from query import sparql_query
from compute import distances_euclidiennes

latitude_user, longitude_user, perimetre_user = generate_user_geo()

cli.se_geolocaliser(latitude_user, longitude_user)
cli.choisir_perimetre(perimetre_user)
query_element = cli.choisir_preferences()

queried_data = sparql_query(query_element, data)

cli.retourner_lieux(queried_data)

computed_data = distances_euclidiennes(latitude_user, longitude_user, queried_data)

cli.retourner_distances(queried_data, computed_data)

cli.afficher_carte(queried_data, latitude_user, longitude_user, perimetre_user, query_element)

