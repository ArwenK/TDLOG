#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 15:33:56 2020

@author: alicekrychowskimac
"""
import datetime
# datetime(year, month, day, hour, minute, second, microsecond)
import json
#import sqlalchemy
#print (sqlalchemy.__version__)

# On pourrait faire une dataclass
class Ingredient:
    """
    Représente un ingredient
    - nom de type str (/!\ sensible à la casse => Poire != poire)
    - categorie de type str
    - quantite de type float
    """

    def __init__(self, nom0, cat0, quan0):
        assert (isinstance(nom0, str)), "nom n'est pas de type str"
        assert (isinstance(cat0, str)), "categorie n'est pas de type str"
        assert (isinstance(quan0, float)), "quantite n'est pas de type float"
        self.nom = nom0
        self.categorie = cat0
        #va surement etre changé pour faire appel à la base de donnée
        self.quantite = quan0

    def clone(self):
        """ Copie profonde de l'ingrédient """
        nouveau = Ingredient(self.nom, self.categorie, self.quantite)
        return nouveau

    @property
    def get_nom(self):
        """
        Retourne le nom de l'ingredient.
        """
        return self.nom

    @property
    def get_categorie(self):
        """
        Retourne la categorie de l'ingredient.
        """
        return self.categorie

    @property
    def get_quantite(self):
        """
        Retourne la quantite de l'ingredient.
        """
        return self.quantite

    @property
    def __repr__(self):
        """
        Returns a string corresponding to the Python representation.
        """
        string = str(self.nom) + ", " + str(self.categorie) + ", " + str(self.quantite)
        return string

    @property
    def dict_ingredient(self):
        """
        Returns a dictionnary corresponding to the ingredient.
        """
        return {'Nom' : self.nom, 'Categorie' : self.categorie,
                'Quantite' : self.quantite, 'Ingredient' : True}


    def __eq__(self, other):
        """
        Renvoie True si self et other sont égaux.
        Attention : on ne vérifie pas la quantité !
        """
        assert(isinstance(other, Ingredient)), "Il faut comparer deux ingrédients"
        booleen = (self.nom == other.nom and self.categorie == other.categorie)
        return booleen

    @property
    def __ne__(self, other):
        """Returns True if self and other are different"""
        return not self.__eq__(other)

    def __iadd__(self, autre_ingredient):
        assert(self == autre_ingredient), "Les ingrédients ne sont pas les mêmes"
        self.quantite += autre_ingredient.quantite
        return self



class Recette:
    """
    Represents une recette
    - nom de type str
    - categorie de type str
    - une liste d'ingredient
    """

    def __init__(self, nom0, cat0):
        assert (isinstance(nom0, str)), "nom n'est pas de type str"
        assert (isinstance(cat0, str)), "categorie n'est pas de type str"
        self.__nom = nom0
        self.__categorie = cat0
        self.liste_ingredients = []

    @property
    def get_nom(self):
        """
        Retourne le nom de l'ingredient.
        """
        return self.__nom

    @property
    def get_categorie(self):
        """
        Retourne la categorie de l'ingredient.
        """
        return self.__categorie


    def to_string(self, back="\n"):
        """
        Returns a string corresponding to the Python representation.
        """
        string = "Recette(" + str(self.__nom) + ", " + str(self.__categorie) + ") : " + back
        for ingredient in self.liste_ingredients:
            string += ingredient.__repr__ + back
        return string

    @property
    def __repr__(self):
        """
        Returns a string corresponding to the Python representation.
        """
        string = self.to_string("\n")
        return string

    @property
    def html_repr(self):
        """
        Returns a string corresponding to the html representation.
        """
        return self.to_string("<br>")

    @property
    def dict_recette(self):
        """
        Renvoie un dictionnaire correspondant à la recette.
        """
        liste_dict_ingredients = []
        for ingredient in self.liste_ingredients:
            liste_dict_ingredients.append(ingredient.dict_ingredient)
        dicti = {'Nom' : self.__nom, 'Categorie' : self.__categorie,
                 'Liste ingredients' : liste_dict_ingredients, 'Recette' : True}
        return dicti

    @property
    def __eq__(self, other):
        """Returns True if self and other are equal"""
        return self.__nom == other.get_nom

    @property
    def __ne__(self, other):
        """Returns True if self and other are different"""
        return not self.__eq__(other)

    @property
    def afficher_recette(self):
        """
        Affiche les ingrédients de la recette
        """
        print(self.__repr__)
        return None

    #@nom.setter
    def nom(self, nouveau_nom):
        """ Modifie le nom de la recette"""
        assert (isinstance(nouveau_nom, str)), "Le nouveau nom n'est pas de type str"
        self.__nom = nouveau_nom
        return None

    #@categorie.setter
    def categorie(self, nouvelle_categorie):
        """ Modifie la categorie de la recette"""
        assert (isinstance(nouvelle_categorie, str)), "categorie n'est pas de type str"
        self.__categorie = nouvelle_categorie
        return None

    def ajouter_ingredient(self, ingredient):
        """
        Ajoute un ingredient à la recette
        """
        message_erreur = "il faut ajouter un element de la classe Ingredient"
        assert (isinstance(ingredient, Ingredient)), message_erreur
        self.liste_ingredients.append(ingredient)
        return None

    def supprimer_ingredient(self, ingredient):
        """
        Supprime un ingredient de la recette
        """
        message_erreur = "il faut supprimer un element de la classe Ingredient"
        assert (isinstance(ingredient, Ingredient)), message_erreur
        assert (len(self.liste_ingredients) != 0), "La liste est vide"
        self.liste_ingredients.remove(ingredient)
        return None



class Repas:
    """
    Represente un repas
    - Nb_personnes de type int
      (la valeur 0 correspond à une valeur non précisée par l'utilisateur)
    - une date de type datetime
    - une liste de recettes liste_recettes
    """

    def __init__(self):
        """
        Initialise un repas au moment de sa création par l'utilisateur.
        Par défaut, le nombre de personne est 0, et la date est la date actuelle
        """
        self.liste_recettes = []
        self.nb_personnes = 0
        self.date = datetime.datetime.now()
        # date actuelle


    def to_string(self, back="\n"):
        """
        Returns a string corresponding to the Python representation.
        """
        string = back + "Repas du " + self.date.strftime("%m/%d/%Y à %H:%M:%S")+" :"+ back + back
        for recette in self.liste_recettes:
            string += "" + recette.to_string(back) + back
        return string

    @property
    def __repr__(self):
        """
        Returns a string corresponding to the Python representation.
        """
        return self.to_string("\n")

    @property
    def html_repr(self):
        """
        Returns a string corresponding to the Python representation.
        """
        return self.to_string("<br>")

    @property
    def dict_repas(self):
        """
        Renvoie un dictionnaire correspondant au repas.
        Utilisé pour le stockage dans un fichier JSON.
        """
        liste_dict_recettes = []
        for recette in self.liste_recettes:
            liste_dict_recettes.append(recette.dict_recette)
        dicti = {'Nombre de personnes' : self.nb_personnes, 'Liste recettes' : liste_dict_recettes,
                 'Date et heure' : self.date.isoformat(), 'Repas' : True}
        return dicti

    @property
    def afficher_repas(self):
        """
        Affiche les recettes du repas.
        """
        print(self.__repr__)
        return None

    #@nb_personnes.setter
    def set_nb_personnes(self, nombre):
        """ Affecte ou modifie le nombre de personnes associées au repas"""
        assert (isinstance(nombre, int)), "Le nombre de personnes n'est pas de type int"
        self.nb_personnes = nombre
        return None

    def set_date(self, annee, mois, jour, heure, minute):
        """ Modifie la date et l'horaire du repas"""
        assert (isinstance(annee, int)), "L'année n'est pas un entier"
        assert (isinstance(mois, int)), "Le mois n'est pas un entier"
        assert (isinstance(jour, int)), "Le jour n'est pas un entier"
        assert (isinstance(heure, int)), "L'heure n'est pas un entier"
        assert (isinstance(minute, int)), "Les minutes n'est pas un entier"
        try:
            self.date = datetime.datetime(annee, mois, jour, heure, minute)
        except ValueError as erreur:
            print("Les nombres doivent repecter le format usuel de date et d'heure, ici :", erreur)
        return None

    def set_date_JSON(self, string):
        """ Importe la date et l'horaire du repas"""
        # self.date = datetime.fromisoformat(string)
        # ça ne marche pas, peut-etre que ma version de Python est trop vieille
        annee = int(string[0:4])
        liste_indices = [(5, 7), (8, 10), (11, 13), (14, 16)]
        liste_nombre = []
        for couple in liste_indices:
            indice1, indice2 = couple
            if string[indice1] == 0:
                nombre = int(string[(indice1+1):indice2])
            else:
                nombre = int(string[indice1:indice2])
            liste_nombre.append(nombre)
        mois, jour, heure, minute = liste_nombre
        self.set_date(annee, mois, jour, heure, minute)
        return None

    def ajouter_recette(self, recette):
        """
        Ajoute une recette à un repas.
        """
        message_erreur = "il faut ajouter un element de la classe Recette"
        assert (isinstance(recette, Recette)), message_erreur
        self.liste_recettes.append(recette)
        return None

    def supprimer_recette(self, recette):
        """
        Supprime une recette d'un repas.
        """
        message_erreur = "il faut supprimer un element de la classe Recette"
        assert (isinstance(recette, Recette)), message_erreur
        assert (len(self.liste_recettes) != 0), "La liste est vide"
        self.liste_recettes.remove(recette)
        return None


class RecetteEncoder(json.JSONEncoder):
    """
    Permet de stocker une recette dans un fichier JSON
    """
    #code d'après https://docs.python.org/fr/2.7/library/json.html
    def default(self, obj):
        if isinstance(obj, Recette):
            return obj.dict_recette
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

class RepasEncoder(json.JSONEncoder):
    """
    Permet de stocker un repas dans un fichier JSON
    """
    #code d'après https://docs.python.org/fr/2.7/library/json.html
    def default(self, obj):
        if isinstance(obj, Repas):
            return obj.dict_repas
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

def decoder_ingredient(dct):
    """
    assert (isinstance(dct, dict)), "La fonction prend en argument un dictionnaire"
    Permet de décoder un ingredient d'après un dictionnaire
    (format utilisé pour le stockage dans un fichier JSON)
    """
    if 'Ingredient' in dct:
        ingredient = Ingredient(dct['Nom'], dct['Categorie'], dct['Quantite'])
        return ingredient
    print("Ce dictionnaire n'est pas un ingrédient")
    return dct

def decoder_recette(dct):
    """
    Permet de décoder une recette d'après un dictionnaire
    (format utilisé pour le stockage dans un fichier JSON)
    """
    assert (isinstance(dct, dict)), "La fonction prend en argument un dictionnaire"
    if 'Recette' in dct:
        recette = Recette(dct['Nom'], dct['Categorie'])
        for element in dct['Liste ingredients']:
            ingredient = decoder_ingredient(element)
            recette.ajouter_ingredient(ingredient)
        return recette
    print("Ce dictionnaire ne représente pas une recette")
    return dct

def decoder_repas(dct):
    """
    Permet de décoder un repas d'après un dictionnaire
    (format utilisé pour le stockage dans un fichier JSON)
    """
    assert (isinstance(dct, dict)), "La fonction prend en argument un dictionnaire"
    if 'Repas' in dct:
        repas = Repas()
        repas.set_date_JSON(dct['Date et heure'])
        repas.set_nb_personnes(dct['Nombre de personnes'])
        for element in dct['Liste recettes']:
            recette = decoder_recette(element)
            repas.ajouter_recette(recette)
        return repas
    print("Ce dictionnaire ne représente pas un repas")
    return dct


def generer_courses(menu):
    """
    menu est une liste de repas.
    On génère un dictionnaire de dictionnaires
    dict_principal = {
    "Fruits" : {"Poires" : 3, "Pommes" : 5}
    "Féculents" : {"Pommes de terre" : 20, "Pates" : 500}
    }
    """
    dict_principal = {}
    for repas in menu:
        assert(isinstance(repas, Repas)), "Un menu doit etre constitué de repas"
        for recette in repas.liste_recettes:
            for ingredient in recette.liste_ingredients:
                cat = ingredient.get_categorie
                nom = ingredient.get_nom
                quantite = ingredient.quantite
                if cat in dict_principal:
                    dict_secondaire = dict_principal[cat]
                    if nom in dict_secondaire:
                        dict_secondaire[nom] += quantite
                    else:
                        dict_secondaire[nom] = quantite
                else:
                    dict_principal[cat] = {nom : quantite}
    return dict_principal

def to_string_courses(dict_principal, back="\n"):
    """
    dict_principal = {
    "Fruits" : {"Poires" : 3, "Pommes" : 5}
    "Féculents" : {"Pommes de terre" : }
    }
    On convertit le dictionnaire en string
    On renvoit string
    """
    INDENTATION = "     "
    string = "Liste des courses" + back
    for cat in dict_principal.keys():
        string += cat + back
        dict_secondaire = dict_principal[cat]
        for nom in dict_secondaire:
            quantite = dict_secondaire[nom]
            string += INDENTATION  + str(nom) + " : " + str(quantite) + back
    return string

def afficher_courses(dict_principal):
    """
    dict_principal = {
    "Fruits" : {"Poires" : 3, "Pommes" : 5}
    "Féculents" : {"Pommes de terre" : }
    }
    On affiche le dictionnaire dans la console Python.
    """
    print(to_string_courses(dict_principal, "\n"))
    return None


def html_courses(dict_principal):
    """
    dict_principal = {
    "Fruits" : {"Poires" : 3, "Pommes" : 5}
    "Féculents" : {"Pommes de terre" : }
    }
    On revoit une string qui permet d'afficher le dictionnaire au format html.
    """
    return to_string_courses(dict_principal, "<br>")

if __name__ == "__main__":
    #Test de la classe Ingredient
    Lait = Ingredient("Lait", "Produits laitiers", 2.)
    cacao = Ingredient("Cacao", "Divers", 1.)
    cafe = Ingredient("Café", "Divers", 1.)
    cacao2 = Ingredient("Cacao", "Divers", 2.)
    cacao2 += cacao
    print(cacao2.__repr__)

    #Test de la classe Recette
    R1 = Recette("Chocolat chaud", "boisson")
    R1.ajouter_ingredient(Lait)
    R1.ajouter_ingredient(cacao)
    print(R1.html_repr)
    R1.afficher_recette
    R2 = Recette("Chocolat chaud", "boisson")
    R2.ajouter_ingredient(Lait)
    R2.ajouter_ingredient(cacao)
    R2.supprimer_ingredient(cacao)
    R2.ajouter_ingredient(cafe)
    R2.nom("Café au lait")
    R2.afficher_recette

    #Test de la classe Repas
    repas = Repas()
    repas.ajouter_recette(R1)
    repas.afficher_repas
    repas.ajouter_recette(R2)
    repas.set_date(2020, 1, 12, 16, 30)
    repas.afficher_repas
    print(repas.html_repr)

    #Fonctionnalités JSON
    test = json.dumps(R2, indent=2, cls=RecetteEncoder)
    with open("data_file_recettes.json", "w") as write_file:
        json.dump(R2, write_file, indent=2, cls=RecetteEncoder)
    with open("data_file_recettes.json", "r") as data_file:
        data_recettes = json.load(data_file)
    with open("data_file.json", "w") as write_file:
        json.dump(repas, write_file, indent=2, cls=RepasEncoder)
    with open("data_file.json", "r") as data_file:
        data = json.load(data_file)
    print("\nDécodage")
    nouveau_repas = decoder_repas(data)
    nouveau_repas.afficher_repas

    # Liste de course
    dicti = generer_courses([nouveau_repas])
    afficher_courses(dicti)
    print(html_courses(dicti))

    #Suite test de la classe Repas
    repas.supprimer_recette(R2)
    repas.afficher_repas
    repas.set_nb_personnes(24)
    repas.set_nb_personnes(23)
    print(repas.nb_personnes)
