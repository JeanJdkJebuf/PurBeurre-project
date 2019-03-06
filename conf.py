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
url_ingredient, markets_for_product, allergens, nutrition_grades \
FROM Products WHERE category_id={}")

# this list displays informations regarding showing_product(),
# a function for the class Menu_graphic()
DISPLAY_INFO = ["Product name", "Ingredients", \
"Website link", "Market place", "allergens"]
