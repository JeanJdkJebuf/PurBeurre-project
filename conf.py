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
explain_menu = "\nThis application helps you finding substitutes\n \
Press Products button to find products\n \
Press My favorites to consult your substitutes \n \
Have fun !\n" 

# text explaining categories
# \n is meant for indentations, to make program sexy
expl_cat = "\n\nChoose a category to access \n \
products corresponding to this category \n \
\n Press main menu to return main page\n \n \n \n \n \n \n \n \n"

# text showing user number of products
show_num = "Product {} to {} (total : {})"

expl_prod = "\n \n Choose a product to get \n \
informations. You will have info regarding \n \
that product , and a substitute. \n \
You will be able to add it to \n \
your favorites and consult it later on \n"

expl_fav = "\n\n\n\n Choose a favorite to consult \n \
 its informations \n\n\
 Click on website link \n \
 to get full informations on \n \
 Open Food Facts website \
\n\n\n\n\n\n\n\n\n\n\n"
