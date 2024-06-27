#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 13:01:31 2024

Application Streamlit pour la géolocalisation et le tourisme.

"""

import streamlit as st
import random
from rdflib import Graph
import folium
from streamlit_folium import folium_static
import geopy.distance
from pyroutelib3 import Router
from numpy import sqrt


# Fonction pour générer les données de géolocalisation de l'utilisateur
def generate_user_geo():
    latitude_user = random.uniform(47.9, 49.5)
    longitude_user = random.uniform(5.0, 5.8)
    perimetre_user = random.uniform(7000, 15000)
    return latitude_user, longitude_user, perimetre_user


# Fonction pour interagir avec l'utilisateur et choisir la géolocalisation
def se_geolocaliser(latitude_user, longitude_user):
    st.subheader("Géolocalisation de l'utilisateur")
    entree = st.radio("Choisissez le mode de géolocalisation :", ('manuel', 'aléatoire'))

    if entree == "manuel":
        try:
            latitude_user = st.number_input("Choisissez une latitude :", value=latitude_user)
            longitude_user = st.number_input("Choisissez une longitude :", value=longitude_user)
        except:
            st.error("Mauvaise entrée.")
            st.stop()

    elif entree == "aléatoire":
        st.write(f"Latitude aléatoire : {latitude_user}")
        st.write(f"Longitude aléatoire : {longitude_user}")

    return latitude_user, longitude_user


# Fonction pour choisir le périmètre de déplacement
def choisir_perimetre(perimetre_user):
    st.subheader("Choix du périmètre")
    entree = st.radio("Choisissez le périmètre :", ('manuel', 'aléatoire'))

    if entree == "manuel":
        try:
            perimetre_user = st.number_input("Périmètre de déplacement (en mètres) :", value=perimetre_user)
        except:
            st.error("Mauvaise entrée.")
            st.stop()

    elif entree == "aléatoire":
        st.write(f"Périmètre aléatoire : {perimetre_user} mètres")

    return perimetre_user


# Fonction pour choisir les préférences de l'utilisateur
def choisir_preferences():
    st.subheader("Choix des préférences")
    entree = st.selectbox("Que cherchez-vous ?", ("Restaurant", "Hôtel", "Point d'intérêt touristique"))

    if entree == "Restaurant":
        query_element = "Restaurant"
    elif entree == "Hôtel":
        query_element = "Hotel"
    elif entree == "Point d'intérêt touristique":
        query_element = "PointOfInterest"
    else:
        st.error("Mauvaise entrée.")
        st.stop()

    return query_element


# Fonction pour interroger les données à l'aide de requêtes SPARQL
def sparql_query(query_element, data):
    st.subheader("Requête SPARQL")
    select = "SELECT ?name ?lat ?lon "
    where = f"WHERE {{?restaurant rdf:type core:{query_element}. ?restaurant rdfs:label ?name. ?restaurant core:isLocatedAt ?localisationuri. ?localisationuri schema1:geo ?geouri. ?geouri schema1:latitude ?lat ; schema1:longitude ?lon.}}"
    q = select + where

    queried_data = data.query(q)

    return queried_data


# Fonction pour calculer les distances euclidiennes entre l'utilisateur et les lieux trouvés
def distances_euclidiennes(latitude_user, longitude_user, queried_data):
    st.subheader("Calcul des distances")
    latlon_list = []
    euclidean_distances = []

    for row in queried_data:
        couple = f"{row.lat},{row.lon}"
        latlon_list.append(tuple(map(float, couple.split(','))))

    for n in latlon_list:
        euclidean_distances.append(sqrt((n[0] - latitude_user) ** 2 + (n[1] - longitude_user) ** 2))

    return euclidean_distances


# Fonction pour afficher les données sur une carte interactive
def visualize_data(data, latitude_user, longitude_user, perimetre_user, query_element):
    st.subheader("Affichage de la carte")
    latitude_user = float(latitude_user)
    longitude_user = float(longitude_user)
    perimetre_user = float(perimetre_user)

    m = folium.Map([latitude_user, longitude_user])

    coords_user = (latitude_user, longitude_user)

    for row in data:
        name = row.name
        lat = float(row.lat)
        lon = float(row.lon)
        coords_resto = (lat, lon)
        distance = int(geopy.distance.geodesic(coords_user, coords_resto).km)

        if float(perimetre_user / 1000) > float(distance):
            popup_description = name + "\n\n" + " -> distance en km :" + str(distance)
            folium.Marker(
                location=[lat, lon],
                tooltip=popup_description,
                popup=popup_description,
                icon=folium.Icon(color="blue"),
            ).add_to(m)

    folium.Circle(
        location=[latitude_user, longitude_user],
        radius=perimetre_user,
        color="black",
        weight=1,
        fill_opacity=0.6,
        opacity=1,
        fill_color="green",
        fill=False,
        popup="{} meters".format(perimetre_user),
        tooltip="I am in meters",
    ).add_to(m)

    folium.Marker(
        location=[latitude_user, longitude_user],
        tooltip="Votre position",
        popup="Votre position",
        icon=folium.Icon(color="red"),
    ).add_to(m)

    folium_static(m)


# Chargement des données RDF
data = Graph()
data.parse("C:/Users/khadi/Documents/Datascientest 2023-2024/2023-2024/Projet geo tourisme/dst_projet_tourisme/data/flux-19287-202401180748.ttl")

# Début de l'application Streamlit
def main():
    st.title("Application de Géolocalisation et de Tourisme")
    
    latitude_user, longitude_user, perimetre_user = generate_user_geo()
    latitude_user, longitude_user = se_geolocaliser(latitude_user, longitude_user)
    perimetre_user = choisir_perimetre(perimetre_user)
    query_element = choisir_preferences()
    
    queried_data = sparql_query(query_element, data)
    computed_data = distances_euclidiennes(latitude_user, longitude_user, queried_data)
    
    visualize_data(queried_data, latitude_user, longitude_user, perimetre_user, query_element)

if __name__ == "__main__":
    main()
