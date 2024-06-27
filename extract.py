#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 11:29:53 2024

@author: maxbld

Récupère les données .ttl et les parse

"""

from rdflib import Graph

data = Graph()

data = data.parse("C:/Users/khadi/Documents/Datascientest 2023-2024/2023-2024/Projet geo tourisme/dst_projet_tourisme/data/flux-19287-202401180748.ttl")