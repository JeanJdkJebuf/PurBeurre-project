##############################################
# Assigning Values to Variables
# for PurBeurre-project
##############################################


##############################################
# User informations
##############################################

USERNAME = ""
PASSWORD = ""

##############################################
# string and lists used for database
##############################################

# website used
SITE = "https://world.openfoodfacts.org/cgi/search.pl?search_terms={}\
&search_tag=category&page_size=1000&json=1"

# list of categories
CATEGORIES = ["'viande'", "'poisson'", "'pates'", "'legumes'", "'gateau'",
 "'conserve'", "'fromage'", "'fruit'", "'dessert'", "'yaourt'", "'boisson'"]

# insert categories request
INSERT_REQ_CATEGORY = ("INSERT INTO Categories VALUES({}, {})")
# insert products request
INSERT_REQ_PRODUCTS = ("INSERT INTO Products VALUES {}")

# mysql research for choose_product(self, parent, category_number) function
PRODUCT_SEARCH = ("SELECT id_products, product_name, ingredients, \
url_ingredient, markets_for_product, allergens, categories_hierarchy, \
nutrition_grades FROM Products WHERE category_id={}")

# this list displays informations regarding showing_product(),
# a function for the class Menu_graphic()
DISPLAY_INFO = ["Product name", "Ingredients", \
"Website link", "Market place", "allergens"]

# Request made for finding a better product
REQUEST_SUBSTITUTE = ("SELECT product_name, ingredients, \
url_ingredient, markets_for_product, allergens, id_products FROM Products \
WHERE id_products <> {} AND nutrition_grades = {} \
AND categories_hierarchy LIKE '%{}%' LIMIT 0,1;")

# insert data into Favorites, request made for showin_product()
INSERT_FAVORITE = ("INSERT INTO Favorites(id_link_product) \
VALUES({}) ON DUPLICATE KEY UPDATE \
id_link_product=id_link_product")

# getting data from Favorites
GETTING_FAV_DATA = ("SELECT product_name, ingredients, \
url_ingredient, markets_for_product, allergens \
FROM Products INNER JOIN Favorites ON Products.id_products = Favorites.id_link_product;")

# text explaining main menu
explain_menu = "\nCette application vous aide à trouver des substituts alimentaires\n \
Appuyer sur Produits pour choisir une catégorie\n \
Appuyer sur Mes favoris pour consulter vos favoris \n \
Amusez vous !\n" 

# text explaining categories
# \n is meant for indentations, to make program sexy
expl_cat = "\n\nChoisissez une catégorie \n \
Pour accéder à des produits correspondants \n \
à cette catégorie \n \
\n Appuyer sur Menu principal pour retourner \n \
à la page principale\n \n \n \n \n \n \n \n \n"

# text showing user number of products
show_num = "Produit {} à {} (total : {})"

expl_prod = "\n \n Cliquez sur un produit \n \
Pour obtenir les informations de ce produit \n \
et celles du substitut \n \
Vous pourrez l'ajouter aux favoris \n \
et le consulter sur l'onglet Mes favoris \n"

expl_fav = "\n\n\n\n Choisissez un produit pour \n \
 consulter ses informations \n\n\
 Cliquez sur le lien du site \n \
 pour obtenir les informations complètes \n \
 du site OpenFoodFacts  \
\n\n\n\n\n\n\n\n\n\n\n"
