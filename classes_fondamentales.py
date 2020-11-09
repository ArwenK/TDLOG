#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 15:33:56 2020

@author: alicekrychowskimac
"""
import datetime

# On pourrait faire une dataclass
class Ingredient:
    """
    Représente un ingredient
    - nom de type str
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
        string = str(self.nom) + ", " + str(self.categorie) +", " + str(self.quantite)
        return string

    @property
    def __eq__(self, other):
        """Returns True if self and other are equal"""
        return self.nom == other.nom and self.quantite == other.quantite

    @property
    def __ne__(self, other):
        """Returns True if self and other are different"""
        return not self.__eq__(other)

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

    @property
    def __repr__(self):
        """
        Returns a string corresponding to the Python representation.
        """
        return "Recette(" + str(self.__nom) + ", " + str(self.__categorie) + ")"

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
        print(self.__repr__ + " : ")
        for ingredient in self.liste_ingredients:
            print(ingredient.__repr__)
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
    - horaire (non implémenté)
    - une liste de recettes liste_recettes
    """

    def __init__(self):
        self.liste_recettes = []
        self.nb_personnes = 0

    @property
    def __repr__(self):
        """
        Returns a string corresponding to the Python representation.
        """
        return "Repas"

#    @property
#    def __eq__(self, other):
#        """Returns True if self and other are equal"""
#        return self.__nom == other.get_nom
#
#    @property
#    def __ne__(self, other):
#        """Returns True if self and other are different"""
#        return not self.__eq__(other)

    @property
    def afficher_repas(self):
        """
        Affiche les recettes du repas
        """
        print(self.__repr__ + " : ")
        for recette in self.liste_recettes:
            print("")
            recette.afficher_recette
        return None

    #@nb_personnes.setter
    def set_nb_personnes(self, nombre):
        """ Affecte ou modifie le nom de la recette"""
        assert (isinstance(nombre, int)), "Le nombre de personnes n'est pas de type int"
        self.nb_personnes = nombre
        return None

    def ajouter_recette(self, recette):
        """
        Ajoute une recette à un repas
        """
        message_erreur = "il faut ajouter un element de la classe Recette"
        assert (isinstance(recette, Recette)), message_erreur
        self.liste_recettes.append(recette)
        return None

    def supprimer_recette(self, recette):
        """
        Supprime une recette d'un repas
        """
        message_erreur = "il faut supprimer un element de la classe Recette"
        assert (isinstance(recette, Recette)), message_erreur
        assert (len(self.liste_recettes) != 0), "La liste est vide"
        self.liste_recettes.remove(recette)
        return None


if __name__ == "__main__":
#    #Test of the class Ingredient
    Lait = Ingredient("Lait", "Produit laitier", 2.)
    cacao = Ingredient("Cacao", "Divers", 1.)
    cafe = Ingredient("Café", "Divers", 1.)
    R = Recette("Chocolat chaud", "boisson")
    R.ajouter_ingredient(Lait)
    R.ajouter_ingredient(cacao)
    R.afficher_recette
    R.supprimer_ingredient(cacao)
    R.ajouter_ingredient(cafe)
    R.nom("Café au lait")
    R.afficher_recette
    repas = Repas()
    repas.ajouter_recette(R)
    repas.afficher_repas
    repas.supprimer_recette(R)
    repas.afficher_repas
    repas.set_nb_personnes(24)
    repas.set_nb_personnes(23)
    print(repas.nb_personnes)
