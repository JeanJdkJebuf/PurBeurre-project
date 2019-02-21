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
CATEGORIES = ["'viande'", "'poisson'", "'pates'", "'legumes'", "'gateau'"]

# insert categories request
INSERT_REQ_CATEGORY = ("INSERT INTO Categories VALUES({}, {})")
