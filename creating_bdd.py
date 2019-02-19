#!/usr/bin/python3
# -*- coding: utf-8 -*
# creating bdd on user data

# import mods and files
import pymysql
from conf import *

class Basedata (object):
    "user as mysql user@'localhost', passw as mysql password"
    def __init__(self, user='', passw=''):
        # defining default data
        self.user =user
        self.passw =passw
        #creating client data
        self.connection = pymysql.connect(host='localhost', \
                             user= self.user, \
                             password= self.passw, \
                             charset='utf8', \
                             cursorclass=pymysql.cursors.DictCursor)

    # creating function that is going to create bdd for this project
    def create_database(self):
        "this function creates tables"

        try:
            # DELETE IF EXISTS DATABASE named comparatif_alimentaire
            with self.connection.cursor() as cursor:
                cursor.execute('DROP DATABASE IF EXISTS comparatif_alimentaire;')
                self.connection.commit()
            
            # CREATING new database named comparatif_alimentaire
            with self.connection.cursor() as cursor:
                cursor.execute("CREATE SCHEMA IF NOT EXISTS \
                `comparatif_alimentaire` DEFAULT CHARACTER SET utf8 ;")
                cursor.execute("USE `comparatif_alimentaire` ;")
            
            # CREATING table Categories within comparatif_alimentaire
            with self.connection.cursor() as cursor:
                cursor.execute("""CREATE TABLE IF NOT EXISTS `comparatif_alimentaire`.`Categories` (
                            `id_categories` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                            `category_name` VARCHAR(30) NOT NULL,PRIMARY KEY (`id_categories`))
                            ENGINE = InnoDB;""")

            # CREATING table Products within comparatif_alimentaire
            with self.connection.cursor() as cursor:
                cursor.execute("""CREATE TABLE IF NOT EXISTS `comparatif_alimentaire`.`Products` (
                `id_products` INT UNSIGNED NOT NULL,
                `product_name` VARCHAR(55) NOT NULL,
                `ingredients` TEXT(1900) NULL,
                `url_ingredient` VARCHAR(250) NOT NULL,
                `markets_for_product` VARCHAR(90) NULL,
                `allergens` VARCHAR(255) NULL,
                `nutrition_grades` VARCHAR(10) NULL,
                `category_id` INT UNSIGNED NOT NULL,
                PRIMARY KEY (`id_products`),
                INDEX `fk_category_id_idx` (`category_id` ASC),
                CONSTRAINT `fk_category_id`
                  FOREIGN KEY (`category_id`)
                  REFERENCES `comparatif_alimentaire`.`Categories` (`id_categories`)
                  ON DELETE NO ACTION
                  ON UPDATE NO ACTION)
                ENGINE = InnoDB;""")
            
            # CREATING table favorites within comparatif_alimentaire
            with self.connection.cursor() as cursor:
                cursor.execute("""CREATE TABLE IF NOT EXISTS `comparatif_alimentaire`.`favorites` (
                `id_favorites` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                `id_link_product` INT UNSIGNED NOT NULL,
                PRIMARY KEY (`id_favorites`),
                INDEX `fk_product_id_idx` (`id_link_product` ASC),
                CONSTRAINT `fk_product_id`
                  FOREIGN KEY (`id_link_product`)
                  REFERENCES `comparatif_alimentaire`.`Products` (`id_products`)
                  ON DELETE NO ACTION
                  ON UPDATE NO ACTION)
                ENGINE = InnoDB;""")

        except:
            pass

        # this function picks data from openfoodfact.org and puts it into var.
        def add_data(self):
            
        
#test
if __name__ == '__main__' :
    bd= Basedata(username, password)
    bd.create_database()