#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
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
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
import numpy as np 

# Fonction pour générer les données de géolocalisation de l'utilisateur
def generate_user_geo():
    latitude_user = random.uniform(47.9, 49.5)
    longitude_user = random.uniform(5.0, 5.8)
    perimetre_user = random.uniform(7000, 15000)
    return latitude_user, longitude_user, perimetre_user

# Fonction pour interagir avec l'utilisateur et choisir la géolocalisation
def se_geolocaliser():
    st.subheader("Géolocalisation de l'utilisateur")
    entree = st.radio("Choisissez le mode de géolocalisation :", ('manuel', 'aléatoire'))

    if entree == "manuel":
        try:
            latitude_user = st.number_input("Choisissez une latitude :", format="%.15f")
            longitude_user = st.number_input("Choisissez une longitude :", format="%.15f")
        except:
            st.error("Mauvaise entrée.")
            st.stop()

    elif entree == "aléatoire":
        latitude_user, longitude_user, _ = generate_user_geo()
        st.write(f"Latitude aléatoire : {latitude_user:.15f}")
        st.write(f"Longitude aléatoire : {longitude_user:.15f}")

    return latitude_user, longitude_user

# Fonction pour choisir le périmètre de déplacement
def choisir_perimetre():
    st.subheader("Choix du périmètre")
    entree = st.radio("Choisissez le périmètre :", ('manuel', 'aléatoire'))

    if entree == "manuel":
        try:
            perimetre_user = st.number_input("Périmètre de déplacement (en mètres) :")
        except:
            st.error("Mauvaise entrée.")
            st.stop()

    elif entree == "aléatoire":
        _, _, perimetre_user = generate_user_geo()
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
    
    # Convertir en DataFrame
    df = pd.DataFrame(queried_data, columns=["name", "lat", "lon"])
    df['lat'] = df['lat'].astype(float)
    df['lon'] = df['lon'].astype(float)
    return df

# Fonction pour calculer les distances euclidiennes entre l'utilisateur et les lieux trouvés
def distances_euclidiennes(latitude_user, longitude_user, queried_data):
    st.subheader("Calcul des distances")
    latlon_list = []
    euclidean_distances = []

    for row in queried_data.itertuples(index=False):
        latlon_list.append((row.lat, row.lon))

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

    for row in data.itertuples():
        name = row.name
        lat = row.lat
        lon = row.lon
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

# Fonction pour prétraiter les données et afficher des visualisations simples
def preprocess_and_visualize_data(data, latitude_user, longitude_user, perimetre_user):
    st.subheader("Prétraitement des données et visualisations")

    # Extraction des catégories et comptage
    categories = ["Restaurant", "Hôtel", "PointOfInterest"]
    counts = [0] * len(categories)

    for row in data.itertuples():
        for i, cat in enumerate(categories):
            if cat.lower() in row.name.lower():
                counts[i] += 1

    # Création d'un DataFrame pour les visualisations
    df = pd.DataFrame({
        'Catégorie': categories,
        'Nombre de lieux': counts
    })

    # Affichage du nombre de lieux par catégorie sous forme de bar plot
    st.write("Nombre de lieux par catégorie :")
    fig = px.bar(df, x='Catégorie', y='Nombre de lieux', labels={'Nombre de lieux': 'Nombre de lieux', 'Catégorie': 'Catégorie'})
    st.plotly_chart(fig)

    # Distribution des distances entre l'utilisateur et les lieux
    distances = []
    coords_user = (latitude_user, longitude_user)
    for row in data.itertuples():
        lat = float(row.lat)
        lon = float(row.lon)
        coords_resto = (lat, lon)
        distance = geopy.distance.geodesic(coords_user, coords_resto).km
        distances.append(distance)

    st.write("Distribution des distances :")
    fig = px.histogram(distances, nbins=30, labels={'value': 'Distance (km)', 'count': 'Nombre de lieux'})
    st.plotly_chart(fig)

    # Statistiques descriptives des distances
    st.write("Statistiques descriptives des distances :")
    st.write(pd.Series(distances).describe())

    # Carte avec marquers colorés selon les distances
    st.subheader("Carte avec marquers colorés selon les distances")
    m = folium.Map([latitude_user, longitude_user])
    for row, dist in zip(data.itertuples(), distances):
        lat = float(row.lat)
        lon = float(row.lon)
        color = 'green' if dist <= perimetre_user / 1000 else 'red'
        popup_description = row.name + "\n\n" + f"Distance : {dist:.2f} km"
        folium.Marker(
            location=[lat, lon],
            tooltip=popup_description,
            popup=popup_description,
            icon=folium.Icon(color=color),
        ).add_to(m)
    folium_static(m)

# Fonction pour les analyses avancées sur les données
def advanced_analysis(data):
    st.subheader("Analyses avancées")

    # K-Means clustering
    kmeans = KMeans(n_clusters=3)
    data['Cluster'] = kmeans.fit_predict(data[['lat', 'lon']])
    
    # Affichage des clusters sur un scatter plot
    fig = px.scatter(data, x='lat', y='lon', color='Cluster', title='Clusters K-Means', labels={'lat': 'Latitude', 'lon': 'Longitude'})
    st.plotly_chart(fig)

    # Statistiques descriptives par cluster
    cluster_stats = data.groupby('Cluster')[['lat', 'lon']].agg(['mean', 'std', 'min', 'max'])
    st.write("Statistiques descriptives par cluster :")
    st.write(cluster_stats)

    # Heatmap des corrélations
    #corr = data[['lat', 'lon', 'Cluster']].corr()
    #fig = px.imshow(corr, text_auto=True, aspect="auto")
    #st.plotly_chart(fig)

# Chargement des données RDF
data = Graph()
data.parse("/workspaces/Geotest/flux-19287-202401180748.ttl")

# Début de l'application Streamlit
def main():
    st.title("Application de Géolocalisation et de Tourisme")

    with st.sidebar:
        st.header("Menu")
        menu = st.radio("Choisissez une page :", ["Home", "Prétraitement des données", "Carte interactive", "Analyse avancée"])

    latitude_user, longitude_user = se_geolocaliser()
    perimetre_user = choisir_perimetre()
    query_element = choisir_preferences()
    
    queried_data = sparql_query(query_element, data)
    computed_data = distances_euclidiennes(latitude_user, longitude_user, queried_data)

    if menu == "Home":
        st.write("Bienvenue sur l'application de géolocalisation et de tourisme.")
        st.write("Utilisez le menu sur la gauche pour naviguer entre les différentes sections.")
    
    if menu == "Prétraitement des données":
        preprocess_and_visualize_data(queried_data, latitude_user, longitude_user, perimetre_user)
        
    if menu == "Analyse avancée":
        advanced_analysis(queried_data)

    if menu == "Carte interactive":
        visualize_data(queried_data, latitude_user, longitude_user, perimetre_user, query_element)

if __name__ == "__main__":
    main()
