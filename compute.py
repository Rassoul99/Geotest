#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 11:30:02 2024

@author: maxbld

Génère de nouvelles données à partir des données existantes
(géolocalisation de l'utilisateur, données du flux de 
datatourisme).

"""

from numpy import sqrt


def distances_euclidiennes(latitude_user, longitude_user, queried_data):
    
    latlon_list=[]
    euclidean_distances=[]
    
    for row in queried_data:
        couple = f"{row.lat},{row.lon}"
        latlon_list.append(tuple(map(float, couple.split(','))))
        
    for n in latlon_list:
        euclidean_distances.append(sqrt((n[0]-latitude_user)**2 + (n[1]-longitude_user)**2))   
    
    return euclidean_distances