#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 11:30:12 2024

@author: maxbld

Affiche sur une carte les données de géolocalisation de 
l'utilisateur et des établissements.

"""

import rdflib
from rdflib import Graph
import folium
import random
import geopy.distance
from pyroutelib3 import Router


def visualize_data(data, latitude_user, longitude_user, perimetre_user, query_element):

    """
    Description:
        Affiche sur une carte folium des lieux et la position d'un utilisateur

    Entrée :
        - data 
            données RDF serialisé
            Pour l'instant un fichier ttl est importé. 
            A voir comment le script .py se comporte avec une source de données beaucoup plus grande
        - latitude_user
        - longitude_user
        - perimetre_user

    Sortie :
        - m 
            Carte folium avec les résultats
    """

    latitude_user = float(latitude_user)
    longitude_user = float(longitude_user)
    perimetre_user = float(perimetre_user)

    #Coordonnées de l'utilisateur 
    coords_user = (latitude_user, longitude_user)

    #Initialisation router
    router = Router("car")
    depart = router.findNode(latitude_user, longitude_user)

    m = folium.Map([latitude_user, longitude_user])

    #Création de liste pour prendre uniquement une destination pour le tracé d'un itinéraire
    mean_lat = []
    mean_lon = []
    for i in data:
        mean_lat.append(float(i.lat))
        mean_lon.append(float(i.lon))

    
    #Change d'icône en fonction du type d'établissement
    """if query_element=="Restaurant":
        image = "iconeresto.png"
        icon = folium.CustomIcon(
            image,
            icon_size=(38, 95)
        )
    elif query_element=="Hotel":
        image = "iconehotel.jpeg"
        icon = folium.CustomIcon(
            image,
            icon_size=(38, 95)
        )
    elif query_element=="PointOfInterest":    
        image = "iconeloisir.png"
        icon = folium.CustomIcon(
            image,
            icon_size=(38, 95)
        )
    else:
        exit()"""


    # Afficher tous les points dans le périmètre utilisateur
    for row in data:
        name = row.name
        lat = float(row.lat)
        lon = float(row.lon)
        #print(lat, lon)
        coords_resto = (lat, lon)
        distance = int(geopy.distance.geodesic(coords_user, coords_resto).km)
        
        if float(perimetre_user/1000) > float(distance):
            popup_description = name + "\n\n" + " -> distance en km :" + str(distance)
            #print("condition fonctionne")
            folium.Marker(
                location=[lat, lon],
                tooltip=popup_description,
                popup=popup_description,
                icon=folium.Icon(color="blue"),
            ).add_to(m)


    # tracé d'un itinéraire   
    """arrivee = router.findNode(float(mean_lat[0]), float(mean_lon[0]))
    status, itineraire = router.doRoute(depart, arrivee)
    itineraire_coordonnees = list(map(router.nodeLatLon, itineraire)) # liste des points du parcours
    folium.PolyLine(
        itineraire_coordonnees,
        color="blue",
        weight=2.5,
        opacity=1
        ).add_to(m)"""


    #tracé du périmètre
    # le radius est le rayon en metres
    folium.Circle(
        location=[latitude_user, longitude_user],
        radius=perimetre_user,
        color="black",
        weight=1,
        fill_opacity=0.6,
        opacity=1,
        fill_color="green",
        fill=False,  # gets overridden by fill_color
        popup="{} meters".format(perimetre_user),
        tooltip="I am in meters",
    ).add_to(m)


    # tracé du marqueur utilisateur
    folium.Marker(
        location=[latitude_user, longitude_user],
        tooltip="Votre position",
        popup="Votre position",
        icon=folium.Icon(color="red"),
    ).add_to(m)
    
    url_carte = "index.html"
    
    m.save(url_carte)
    
    return url_carte