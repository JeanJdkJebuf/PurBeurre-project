# PurBeurre-project
Ce projet consiste à utiliser les données de l'api d'**OpenFoodFacts** pour créer une base de donnée, et de l'utiliser via un client lourd.

## Description
Dans le cadre du projet, l'utilisateur répond aux attentes de la société Pur Beurre, qui désire avoir un programme de substitution d'aliments.
L'utilisateur choisit un produit, le programme lui renvoie un substitut, plus sain.

## Installation

1. **Identifiants mysql**  
Vous devez en premier lieux disposer d'un serveur local mysql, et d'identifiants (*xxxxx*:localhost, ainsi que du mot de passe correspondant).
Vous devrez par la suite entrer votre username (symbolisé par *xxxxx* dans l'exemple, ci-dessus) et votre PASSWORD entre guillemets dans le fichier conf.py.  
Exemple ci-dessous:  
USERNAME = "xxxxx"  
PASSWORD = "motdepasse"


Il faudra ensuite installer plusieurs mods:

2. **L'outil tkinter**  
comme tkinter est basé sur la librairie Tk (en c++), vous devez avoir tkinter installé dans votre système d'exploitation.  
* En debian : `apt install python3-tk`

3. **L'outil pip**    
Enfin, vous devrez utiliser l'outil pip une fois sur votre environnement virtuel pour installer les modules spécifiques au bon fonctionnement du programme.  
`pip install -r requirements.txt`

4. **Pymysql**  
Si vous rencontrez des problèmes pour installer pymysql, vous devrez faire en mode root :  
* En debian : `apt install python3-pymysql`  
Il faut avoir une version mysql 5.5 ou supérieure pour pouvoir utiliser pymysql


## Utilisation

Après avoir installé les différents outils nécessaires au bon fonctionnement du programme, il va falloir peupler la base de donnée.
Pour ce faire, Veuillez simplement lancer le fichier **creating_bdd.py** et patienter lors du peuplement de la base de donnée.  
Un décompte vous permettra de connaitre l'avancement global de la progression.

Enfin, vous pourrez lancer le programme, via le script **main.py**  
Une interface graphique se lancera alors.

L'onglet **Products** vous permettra de choisir une catégorie, parmis les 11 proposées.  
Une fois votre catégorie choisie, vous pourrez sélectionner l'un des 10 produits proposés sur la page, ou cliquer sur next ou previous, pour consulter d'autres produits.

Une fois le **produit** choisit, en cliquant dessus une page indépendante s'ouvrira, affichant les caractéristiques du produit, ainsi que celles du substitut.  
Vous pourrez, si vous le désirez, ajouter le substitut aux favoris, ou encore cliquer sur le lien des produits, afin d'ouvrir votre navigateur web et consulter les informations de ces derniers sur le site (https://fr.openfoodfacts.org)

A tout moment, vous pourrez revenir à l'onglet principal en cliquant sur l'onglet **Main menu**

Enfin, vous pourrez consulter vos produits favoris à tout moment en cliquant depuis l'onglet principal sur le bouton **My favorites**.  
Une liste exaustive de tous les produits ajoutés s'affichera. Vous pourrez en cliquant dessus consulter ses informations.

## Informations diverses

Vous trouverez dans le dossier ressources une image .png du modèle physique de données pris en utilisant **MySQL Workbench**

Je n'ai pas réussi à faire exporter tkinter par pip, ce dernier utilisant plusieurs bibliothèques pour fonctionner. Il faut donc obligatoirement l'installer sans utiliser pip, tkinter n'étant pas dans la bibliothèque de pip.