#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 11:29:43 2024

@author: maxbld

Affiche des informations à l'utilisateur.

Permet à l'utilsateur d'entrer des préférences qui modifieront
la requête SPARQL.

"""

from sys import exit
from time import sleep
from display import visualize_data
import webbrowser

def se_geolocaliser(latitude_user, longitude_user):
    """
    Géolocalise l'utilisateur selon deux modes : manuel ou aléatoire.
    
    Parameters
    ----------
    latitude_user : float
        Valeur angulaire des parallèles Nord-Sud (-90° au pôle sud, 0° à l'équateur, 90° au pôle nord).
    longitude_user : float
        Valeur angulaire des méridiens Est-Ouest (-180° à 180°, 0° au méridien de Greenwich).

    Returns
    -------
    None.

    """
    
        # Géolocalisation de l'utilisateur
    
    entree=input("""Choisissez le mode de géolocalisation :
        
        (a) manuel
        (b) aléatoire
    """)
    
    if entree=="a": # manual
        try: 
            latitude_user = float(input("Choisissez une latitude : "))
            longitude_user = float(input("Choisissez une longitude : "))
        except:
            print("Mauvaise entrée.")
            exit()
            
    elif entree=="b": #random
    
        print(f"Ma géolocalisation générée aléatoirement dans le département de la Meuse : \n{latitude_user}, {longitude_user}")
    
    else:
        
        print("Mauvaise entrée.")
        exit()

def choisir_perimetre(perimetre_user):
    """
    Propose deux modes pour déterminer le périmètre de déplacement de l'utilisateur : manuel ou aléatoire.

    Parameters
    ----------
    perimetre_user : float
        Périmètre en mètre de déplacement de l'utilisateur.

    Returns
    -------
    None.

    """
    
    entree=input("""\nChoisissez le périmètre :
        
        (a) manuel
        (b) aléatoire
    """)
    
    if entree=="a":
    
        try:
            perimetre_user = int(input("\nPérimètre de déplacement : "))
        except:
            print("Mauvaise entrée.")
            exit()
    
    elif entree=="b":
        
        print(f"\nMon périmètre de déplacement généré aléatoirement : {perimetre_user}")
    
    else:
        
        print("Mauvaise entrée.")
        exit()
    
def choisir_preferences():
    """
    

    Returns
    -------
    query_element : TYPE
        DESCRIPTION.

    """
        
    entree=input("""\nQue cherchez vous :
        (a) Restaurant
        (b) Hôtel
        (c) Point d'intérêt touristique
          """)
    
    if entree=="a":
        query_element="Restaurant"
    elif entree=="b":
        query_element="Hotel"
    elif entree=="c":
        query_element="PointOfInterest"
    else:
        print("Mauvaise entrée.")
        exit()
        
    return query_element

def retourner_lieux(queried_data):
    input("\nAppuyez sur une touche pour afficher le nom des lieux et leur géolocalisation :")
    for row in queried_data:
        print(f"{row.name} - {row.lat},{row.lon}")
        sleep(0.01)
        
def retourner_distances(queried_data, euclidean_distances):
    i=0
    input("\nAppuyez sur une touche pour afficher le noms des lieux et leur distance :")
    for row in queried_data:
        print(f"{row.name} - ", euclidean_distances[i])
        i=i+1
        sleep(0.01)
        
def afficher_carte(queried_data, latitude_user, longitude_user, perimetre_user, query_element):
    input("\nAppuyez sur une touche pour générer la carte :")
    url_carte = visualize_data(queried_data, latitude_user, longitude_user, perimetre_user, query_element)
    input("\nAppuyez sur une touche pour afficher la carte dans votre navigateur :")
    webbrowser.open(url_carte, new=0, autoraise=True)