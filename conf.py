##############################################
# Assigning Values to Variables
# for PurBeurre-project
##############################################


##############################################
# User informations
##############################################

USERNAME = "guillaume"
PASSWORD = "4151ergIUzed26er"

##############################################
# string and lists used for database
##############################################

# website used
SITE = "https://world.openfoodfacts.org/cgi/search.pl?search_terms={}\
&search_tag=category&page_size=1000&json=1"

# list of categories
CATEGORIES = ["'viande'", "'poisson'", "'pates'", "'legumes'", "'gateau'",
 "'conserve'", "'fromage'"]

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