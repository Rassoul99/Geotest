#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 11:28:38 2024

@author: maxbld

Génère ou récupère les données de géolocalisation de l'utilisateur.

"""

import random

def generate_user_geo():
    
    latitude_user = random.uniform(47.9,49.5)
    longitude_user = random.uniform(5.0,5.8)
    perimetre_user = random.uniform(7000,15000)
    
    return latitude_user, longitude_user, perimetre_user