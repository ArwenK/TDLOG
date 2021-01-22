#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 16:22:32 2021

@author: krychowskiantoine
"""


from flask import Flask, render_template, url_for, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user, login_required
import datetime
import json
from flask_sqlalchemy import SQLAlchemy
import logging as lg


ENTREE = '1'
PLAT = '2'
DESSERT = '3'
GOUTER = '4'
BOISSON = '5'
AUTRES = '6'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.sqlite'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#db.init_app(app)


login_manager = LoginManager()
login_manager.login_view = 'app.login'
login_manager.init_app(app)

tags = db.Table(
    'tags',
    db.Column('recette_id', db.Integer, db.ForeignKey('recette.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True))

tags2 = db.Table(
    'tags2',
    db.Column('repas_id', db.Integer, db.ForeignKey('repas.id'), primary_key=True),
    db.Column('recette_id', db.Integer, db.ForeignKey('recette.id'), primary_key=True))

tags3 = db.Table(
    'tags3',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('recette_id', db.Integer, db.ForeignKey('recette.id'), primary_key=True))

tags4 = db.Table(
    'tags4',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('repas_id', db.Integer, db.ForeignKey('repas.id'), primary_key=True))


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/liste')
def liste():
    if current_user.is_authenticated: 
        liste = current_user.generer_liste_course()
    else:
        liste = "Il faut vous connecter pour accéder à votre liste de courses! "
    with open("static/JSON/data_file2.json", "r") as data_file:
        data = json.load(data_file)
    repas = decoder_repas(data)
    exemple_liste = html_courses(generer_courses([repas]))
    return render_template("liste.html", liste_courses = liste, exemple = exemple_liste)


@app.route('/recettes')
def recettes():
    if current_user.is_authenticated: 
        carnet = current_user.dict_carnet_recettes()["Liste recettes"]
        # afficher une liste avec les recettes ici comme ça on peut afficher recette.Nom
#        carnet_recette_JSON = json.dumps(current_user.dict_carnet_recettes(), indent=2)
#        print(carnet)
#        print(carnet_recette_JSON)
    else:
        carnet = []
        print("Il faut vous connecter pour générer une recette! ")
    if current_user.is_authenticated: 
        liste = current_user.afficher_recettes()
    else:
        liste = "Il faut vous connecter pour accéder à vos recettes! "
    return render_template("recettes.html", liste_recettes= liste, carnet_recettes = carnet)


@app.route('/recettes/ajouter-recette',  methods=['get', 'post'])
def ajouter_recette():
    if not current_user.is_authenticated: 
        print("Utilisateur non connecté, redirection vers login...")
        return redirect(url_for('login'))
    if request.method == 'POST':
        dct = request.get_json()
        print(dct)
        recette = decoder_recette(dct)
        db.session.add(recette)
        db.session.commit()
        current_user.ajouter_recette(recette)
        db.session.commit()
        print("On ajoute la recette", recette.__repr__) 
    return render_template("ajouter-recette.html")


#@app.route('/recettes/post-recette')
#def post_recette():
#    recipe = request.form['recipe']
#    nb_people = request.form['nb_people']
#    print(recipe, nb_people)
#    return 'Traitement en cours'


@app.route('/planning')
def planning():
    with open("static/JSON/data_file2.json", "r") as data_file:
        data = json.load(data_file)
    nouveau_repas = decoder_repas(data)
    r = nouveau_repas.html_repr
    return render_template("planning.html", repas = r )

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('mon_compte'))
    else:
        return render_template("login.html")

@app.route('/post-login', methods=['get', 'post'])
def post_login():
    email = request.form['email']
    password = request.form['password']
    print(email, password)
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        print("Please check your login details and try again.")
        return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    
    print("Utilisateur connecté !")
    return redirect(url_for('index'))

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        print("Already exist")
        return redirect(url_for('signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, username = name, password=generate_password_hash(password, method='sha256'))
    print(email, name, password)
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    print('Utilisateur enregistré')
    
    #log the new user in
    login_user(new_user, remember= True)
    print("Utilisateur connecté !")
    return redirect(url_for('index'))

@app.route('/mon-compte')
@login_required
def mon_compte():
    name = current_user.username
    return render_template("mon-compte.html", name = name)

@app.route('/logout', methods=['post'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




# On pourrait faire une dataclass
class Ingredient(db.Model):
    """
    Représente un ingredient
    - nom de type str (/!\ sensible à la casse => Poire != poire)
    - categorie de type str
    - quantite de type float
    """
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    categorie = db.Column(db.String(80), nullable=False)
    quantite = db.Column(db.Float, nullable=True)

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

    def __iadd__(self, autre_ingredient):
        self.quantite += autre_ingredient.quantite
        return self
    


class Recette(db.Model):
    """
    Represents une recette
    - nom de type str
    - categorie de type str
    - un nombre de personnes
    - une liste d'ingredient
    """
    id = db.Column(db.Integer, primary_key=True)
    __nom = db.Column(db.String(80), nullable=False)
    __categorie =  db.Column(db.String(80), nullable=False)
    personnes = db.Column(db.Integer)
    liste_ingredients = db.relationship(
        'Ingredient', secondary=tags, lazy='subquery',
        backref=db.backref('recette', lazy=True))

    def __init__(self, nom0, cat0, ingredients, personnes=0):
        assert (isinstance(nom0, str)), "nom n'est pas de type str"
        assert (isinstance(cat0, str)), "categorie n'est pas de type str"
        self.__nom = nom0
        self.__categorie = cat0
        self.liste_ingredients = ingredients
        self.personnes = personnes

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
        Returns a string corresponding to the representation.
        """
        string = "Recette(" + str(self.__nom) + ", " + str(self.__categorie) + ") : " + back
        for ingredient in self.liste_ingredients:
            string += "- " + ingredient.__repr__ + back
        string += back
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



class Repas(db.Model):
    """
    Represente un repas
    - Nb_personnes de type int
      (la valeur 0 correspond à une valeur non précisée par l'utilisateur)
    - une date de type datetime
    - une liste de recettes liste_recettes
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    nb_personnes = db.Column(db.Integer)
    liste_recettes = db.relationship(
        'Recette', secondary=tags2, lazy='subquery',
        backref=db.backref('repas', lazy=True))

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
        string = back + "Repas du " + self.date.strftime("%d/%m/%Y à %H:%M:%S")+" :"+ back + back
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

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(1000))
    carnet_recettes = db.relationship(
        'Recette', secondary=tags3, lazy='subquery',
        backref=db.backref('user', lazy=True))
    menu = db.relationship(
        'Repas', secondary=tags4, lazy='subquery',
        backref=db.backref('user', lazy=True))
    
    def __init__(self, email, username, password): 
        self.username = username 
        self.email = email
        self.password = password
        self.menu = []
        self.carnet_recettes = []
        
    def repre(self):
        """
        Renvoie une représentation
        """
        return str(self.password)
        
    def ajouter_recette(self, recette):
        """
        Ajoute une recette à un utilisateur.
        """
        message_erreur = "il faut ajouter un element de la classe Recette"
        assert (isinstance(recette, Recette)), message_erreur
        self.carnet_recettes.append(recette)
    
    def supprimer_recette(self, recette):
        """
        Supprime une recette du carnet de recette d'un utilisateur.
        """
        message_erreur = "il faut supprimer un element de la classe Recette"
        assert (isinstance(recette, Recette)), message_erreur
        assert (len(self.carnet_recettes) != 0), "Le carnet de recettes est vide"
        self.carnet_recettes.remove(recette)
        return None
        
    def ajouter_repas(self, repas):
        """
        Ajoute un repas à un utilisateur.
        """
        message_erreur = "il faut ajouter un element de la classe Repas"
        assert (isinstance(repas, Repas)), message_erreur
        self.menu.append(repas)
    
    def supprimer_repas(self, repas):
        """
        Supprime un repas du menu.
        """
        message_erreur = "il faut supprimer un element de la classe Repas"
        assert (isinstance(repas, Repas)), message_erreur
        assert (len(self.menu) != 0), "La liste est vide"
        self.carnet_recettes.remove(repas)
        return None
        
    def generer_liste_course(self):
        if len(self.menu) == 0:
            return "Vous n'avez aucun repas de prévu"
        string = html_courses(generer_courses(self.menu))
        return string
    
    def afficher_recettes(self):
        if len(self.carnet_recettes) == 0:
            return "Vous n'avez pas encore enregistré de recette"
        string = ""
        for recette in self.carnet_recettes:
            string += recette.html_repr
        return string
    
    def dict_carnet_recettes(self):
        """
        Renvoie un dictionnaire correspondant au carnet de recette.
        Utilisé pour le stockage dans un fichier JSON.
        """
        liste_dict_recettes = []
        for recette in self.carnet_recettes:
            liste_dict_recettes.append(recette.dict_recette)
        dicti = {'Liste recettes' : liste_dict_recettes}
        return dicti
        

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

class CarnetEncoder(json.JSONEncoder):
    """
    Permet de stocker un repas dans un fichier JSON
    """
    #code d'après https://docs.python.org/fr/2.7/library/json.html
    def default(self, obj):
        liste = []
        for indice in range(len(obj)): 
            if isinstance(obj[indice], Recette):
                liste.append(obj[indice].dict_recette)
        return liste
#        # Let the base class default method raise the TypeError
#        return json.JSONEncoder.default(self, obj)

def decoder_ingredient(dct):
    """
    assert (isinstance(dct, dict)), "La fonction prend en argument un dictionnaire"
    Permet de décoder un ingredient d'après un dictionnaire
    (format utilisé pour le stockage dans un fichier JSON)
    """
    if 'Ingredient' in dct:
        if dct['Categorie'] == {} :
            dct['Categorie'] = "Bug de catégorie"
        ingredient = Ingredient(dct['Nom'], dct['Categorie'], float(dct['Quantite']))
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
        categorie = dct['Categorie']
        if categorie == ENTREE:
            categorie = 'Entrée'
        elif categorie == PLAT:
            categorie = 'Plat'
        elif categorie == DESSERT:
            categorie = 'Dessert'
        elif categorie == GOUTER:
            categorie = 'Gouter'
        elif categorie == BOISSON:
            categorie = 'Boisson'
        elif categorie == AUTRES:
            categorie = 'Autre'
        recette = Recette(dct['Nom'], categorie, [], int(dct['Nombre']))
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
    INDENTATION = "     - "
    string = "Liste des courses" + back
    for cat in dict_principal.keys():
        string += back + cat + back
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

#db.create_all()
#lg.warning('Database initialized!')

if __name__ == "__main__":
    app.run()
