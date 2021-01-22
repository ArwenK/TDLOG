let ingredient = [];

window.addEventListener("load", function() {
    function sendData() {
        // retrieve the form
        var form = document.getElementById("myForm");

        // construct an HTTP request
        var xhr = new XMLHttpRequest();
        xhr.open(form.method, form.action, true);
        xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

        // build the recipe data
        var data = {};
        data["Nom"] = form.elements["name_recipe"].value;
        data["Categorie"] = form.elements["category_recipe"].value;
        data["Nombre"] = form.elements["nb_people"].value;
        data['Liste ingredients'] = ingredient;
        data['Recette'] = "True";

        // send the collected data as JSON
        xhr.send(JSON.stringify(data));
    }

    var form = document.getElementById("myForm");
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        sendData();
    });
});


function Ajouter(form) {
    var o = new Option(form.name_ingredient.value, form.quantity.value);
    form.liste.options[form.liste.options.length] = o;
    ingredient.push({Ingredient : "True", Nom: form.name_ingredient.value, Quantite: form.quantity.value, Categorie: form.category_ingredient.options[form.category_ingredient.options.selectedIndex].text})
}

function Inserer(form) {
    var o = new Option(form.name_ingredient.value, form.quantity.value);
    if (form.liste.options.selectedIndex >= 0) {
        form.liste.options.length++;
        for (var i = form.liste.options.length - 1; i > form.liste.options.selectedIndex; i--) {
            var p = new Option(form.liste.options[i - 1].text, form.liste.options[i - 1].value);
            form.liste.options[i] = p;
        }
        form.liste.options[form.liste.options.selectedIndex] = o;
        ingredient.push({Ingredient : "True", Nom: form.name_ingredient.value, Quantite: form.quantity.value, Categorie: form.category_ingredient.options[form.category_ingredient.options.selectedIndex].text})
    } else {
        alert("Insertion impossible. Sélectionnez une ligne");
    }
}

function Supprimer(list) {
    if (list.options.selectedIndex >= 0) {
        list.options[list.options.selectedIndex] = null;

    } else {
        alert("Suppression impossible : aucune ligne sélectionnée");
    }
}

function SupprimerTout(list) {
    list.options.length = 0;
}

function remplirSelect(){
var form = document.getElementById("form_recipe");
var j = [{
  "Nom": "Caf\u00e9 au lait",
  "Categorie": "boisson",
  "Liste ingredients": [
    {
      "Nom": "Lait",
      "Categorie": "Produits laitiers",
      "Quantite": 2.0,
      "Ingredient": true
    },
    {
      "Nom": "Caf\u00e9",
      "Categorie": "Divers",
      "Quantite": 10.0,
      "Ingredient": true
    }
  ],
  "Recette": true
},

{
      "Nom": "Chocolat chaud",
      "Categorie": "boisson",
      "Liste ingredients": [
        {
          "Nom": "Lait",
          "Categorie": "Produits laitiers",
          "Quantite": 2.0,
          "Ingredient": true
        },
        {
          "Nom": "Cacao",
          "Categorie": "Divers",
          "Quantite": 1.0,
          "Ingredient": true
        }
      ],
      "Recette": true
    }
  ];
var i;
for (i = 0; i < j.length; i++) {
    var o = new Option(j[i].Nom, i+1);
    form.recipe.options[form.recipe.options.length] = o;
}
}
