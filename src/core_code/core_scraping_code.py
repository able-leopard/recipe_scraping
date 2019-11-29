import urllib
from urllib.request import urlopen as uReq
from urllib.parse import urljoin
from urllib.error import HTTPError


import bs4
from bs4 import BeautifulSoup as soup
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import sys
import os

import requests
import http.cookiejar, urllib.request
import time
import random

import hashlib
import re
import mimetypes
import json
import datetime

import logging
"""
Takes in a url.
Returns a BeautifulSoup page.

Removes the url from to_do_links.
Adds the url to viewed_links.

The webdriver will already wait for the page to load by default via the .get() method
https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
"""
def generate_soup_page(url, driver, to_do_links, viewed_links):
    
    driver_browser = driver
    
    #getting the link
    driver_browser.get(url)
    
    #getting the html
    html = driver_browser.execute_script("return document.documentElement.outerHTML")
    
    #converting to BeautifulSoup page
    sel_soup_page = soup(html, 'html.parser')
    
    #removing link from to-do list
    if url in to_do_links:
        to_do_links.remove(url)
    else:
        pass
    
    #adding link to viewed list
    viewed_links.append(url)
    
    return sel_soup_page

"""
Takes in a BeautifulSoup page.
Generates a list of sub links in that page.
Check if the url has already been viewed or is already in the to do list.
If none of the above, then add it unto the to do list.

Appends two lists: viewed_links, to_do_links
"""
def append_todo_and_viewed(soup_page, viewed_links:list, to_do_links:list, Parser):
    
    #finding a list of sub links in the BeautifulSoup page
    url_list = Parser.find_sub_links(soup_page)
    
    for i in url_list:
    
        #pass if the link is already viewed
        if i in viewed_links:
            pass

        #pass if the link is already in to do list
        elif i in to_do_links:
            pass

        #if link is not viewed and not in to do list, add it to to do list
        else:
            to_do_links.append(i)

"""
Takes in a BeautifulSoup page and a class parser.
Returns the name of the photo being saved
"""   
def get_photo_name(soup_page, Parser, link):
     
    #grabbing the image link
    photo_link = Parser.get_photo_link(soup_page, link)

    #normalizing image type
    image_type = mimetypes.guess_type(urllib.parse.urlparse(photo_link).path, strict=True)[0]

    #extracting the abbreviation, jpeg, jpg, png, etc.
    image_abbreviation = image_type[image_type.find('/')+1:len(image_type)]

    #grabbing the recipe_name
    recipe_name = Parser.get_recipe_name(soup_page)

    #adding the recipe name to the image name
    image_name = recipe_name[:-1]+"."+image_abbreviation

    return image_name

"""
Creates dictionary containing 7 items
1. time scrape the created
2. hashed original url of recipe page
3. recipe name
4. serving size
5. ingredients
6. instructions
7. photo name

"""
def create_dictionary(soup_page, link, Parser):
    
    dictionary = {
                  'time':datetime.datetime.utcnow().isoformat(),
                  
                  #we're hashing the original url  
                  'original_url_hashed':hashlib.md5(link.encode('utf-8')).hexdigest(),
                  'recipe_name':Parser.get_recipe_name(soup_page),
                  'serving_size':Parser.get_serving_size(soup_page),
                  'ingredients':Parser.get_ingredients(soup_page),
                  'instructions':Parser.get_instructions(soup_page),
                  'photo_link':Parser.get_photo_link(soup_page, link)
                              }
    return dictionary

"""
Overall Text Format

We're extracting 4 text items from each page
1. Recipe Name
2. Serving Size
3. Ingredients
4. Instructions

After formatting, each for final outputs the 1-4 items will begin with a "\n" and end with a "\n"
Recipe Name, won't have a "\n" in the beginning but will have a "\n", because its the first item
Instructions, will have a "\n" in the beginning but won't have a "\n" at the end, because its the end item

Ingredients will begin with the word "Ingredients" followed by the list of ingredients seperated by \n
Instructions will begin with the word "Instructions" followed by the list of instructions seperated by \n
"""
def format_recipe_txt(recipe_dic:dict):
    
    #formatting recipe name-------------------------------------------------------
    formatted_recipe_name = recipe_dic['recipe_name']
    
    #formatting serving size------------------------------------------------------
    formatted_serving_size = recipe_dic['serving_size']
    
    #formatting ingredients-------------------------------------------------------
    original_ingredients = recipe_dic['ingredients']        
    
                            #reduces multiple empty lines into 1 empty line
    formatted_ingredients = re.sub(r'(\n\s*)+\n+', '\n', original_ingredients)
    
                            #reduces multiple empty lines into 1 empty line
    formatted_ingredients = re.sub(' +', ' ', original_ingredients) 

    #formatting instructions------------------------------------------------------
    original_instructions = recipe_dic['instructions']
    
                             #reduces multiple empty lines into 1 empty line
    formatted_instructions = re.sub(r'(\n\s*)+\n+', '\n', original_instructions)
    
                             #removes multiple white spaces
    formatted_instructions = re.sub(' +', ' ', formatted_instructions)
    
    #stripping the ending "\n"
    formatted_instructions = formatted_instructions.rstrip()
    
    all_formatted_txt_concatenated = (formatted_recipe_name+
                                      formatted_serving_size+
                                      formatted_ingredients+
                                      formatted_instructions)
    
    #reformatting some special characters
    all_formatted_txt_concatenated = all_formatted_txt_concatenated.replace(r'\xa', ' ')
    
    return all_formatted_txt_concatenated

"""
Takes in a BeautifulSoup page, the original URL and a class Parser.
Creates json file and saves it in the local directory.
"""
def save_json_file(soup_page, link, Parser, dir_to_store):
    
    #getting the hashed_id
    hashed_id = hashlib.md5(link.encode('utf-8')).hexdigest()
      
    #storing the dictionary in this variable
    dictionary_output = create_dictionary(soup_page, link, Parser)
    
    #storing dictionary in json text
    json_text = json.dumps(dictionary_output)

    #json file name with the abbreviation
    json_file_name = hashed_id[:-1]+".json"
    
    #creating the saved_recipes path
    saved_recipes_path = os.path.join(dir_to_store, 'saved_recipes')
    
    #specifying the destination folder path
    destination_path = os.path.join(saved_recipes_path, hashed_id)
    
    #complete name with the destination path
    complete_json_file_name = os.path.join(destination_path, json_file_name)
        
    #saving json file
    with open(complete_json_file_name, 'w') as f:
        f.write(json_text)
        f.close()

"""
Takes in a BeautifulSoup page, the original URL and a class Parser.
Creates the formatted txt file and saves it in the local directory.
"""
def save_txt_file(soup_page, link, Parser, dir_to_store):
    
    #getting the hashed_id
    hashed_id = hashlib.md5(link.encode('utf-8')).hexdigest()
      
    #storing the dictionary in this variable
    dictionary_output = create_dictionary(soup_page, link, Parser)
    
    #storing all the formatted text output in this variable
    all_formatted_text_output = format_recipe_txt(dictionary_output)
    
    #txt file name with the abbreviation
    txt_file_name = hashed_id[:-1]+".txt"
    
    #creating the saved_recipes path
    saved_recipes_path = os.path.join(dir_to_store, 'saved_recipes')
    
    #specifying the destination folder path
    destination_path = os.path.join(saved_recipes_path, hashed_id)
    
    #complete name with the destination path
    complete_txt_file_name = os.path.join(destination_path, txt_file_name)
    
    #writing and saving txt file
    with open(complete_txt_file_name, 'w') as f:
        f.write(all_formatted_text_output)
        f.close()

"""
Takes in a BeautifulSoup page and a class Parser.
Downloads and saves photo in local directory.
"""
def save_photo_file(soup_page, link, Parser, dir_to_store):
    
    #grabbing the image link
    photo_link = Parser.get_photo_link(soup_page, link)

    #skip downloading photo if its not a proper photo link
    if photo_link == 'not_proper_link':
        pass
    elif photo_link == None:
        pass
    else:    
        #throwing error if the link is empty
        assert photo_link != ''

        #normalizing image type
        image_type = mimetypes.guess_type(urllib.parse.urlparse(photo_link).path, strict=True)[0]

        #extracting the abbreviation, jpeg, jpg, png, etc.
        image_abbreviation = image_type[image_type.find('/')+1:len(image_type)]

        #getting the hashed_id
        hashed_id = hashlib.md5(link.encode('utf-8')).hexdigest()

        #adding the recipe name to the image name
        image_name = hashed_id[:-1]+"."+image_abbreviation

        #creating the saved_recipes path
        saved_recipes_path = os.path.join(dir_to_store, 'saved_recipes')
        
        #specifying the destination folder path
        destination_path = os.path.join(saved_recipes_path, hashed_id)

        #complete name with the destination path
        complete_image_file_name = os.path.join(destination_path, image_name)

        #creating cookie jar
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

        #this is the user agent
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7')]

        #writing and saving the file
        image_content = opener.open(photo_link).read()
        with open(complete_image_file_name, 'wb') as f:
            f.write(image_content)
            f.close()

"""
Takes in a BeautifulSoup page, the original URL and a class Parser.
Creates the json, txt, and photo file and saves it in the local directory
"""
def save_all_files(soup_page, link, Parser, dir_to_store):
    
    #creating the saved_recipes path
    saved_recipes_path = os.path.join(dir_to_store, 'saved_recipes')
    
    #creating the tracker folder if it doesn't already exist
    if os.path.exists(saved_recipes_path) != True:
        os.mkdir(saved_recipes_path)
    
    #getting the hashed_id
    hashed_id = hashlib.md5(link.encode('utf-8')).hexdigest()
    
    #specifying the destination folder path, naming folder according to the hashed_id
    destination_path = os.path.join(saved_recipes_path, hashed_id)
    
    #creating a new folder for each recipe
    os.mkdir(destination_path)
    
    #saving all files
    save_json_file(soup_page, link, Parser, dir_to_store)
    save_txt_file(soup_page, link, Parser, dir_to_store)
    save_photo_file(soup_page, link, Parser, dir_to_store)

"""
Creating classes for Exceptions
"""
class NotRecipe(Exception):
    pass

class FileNotFound(Exception):
    pass

class NoServingSize(Exception):
    pass

"""
Loads in the to_do_links and viewed_links:
If the links were previously saved in json files, then the links are extracted from there.
If not, then the links are taken from the manually added start_to_do_links and start_viewed_links.

Returns a tuple of two lists (to_do_links, viewed_links)
"""
def load_links(start_to_do_links, start_viewed_links, Parser, dir_to_store):

    #specifying the destination folder path
    tracker_path = os.path.join(dir_to_store, 'tracker')

    #complete name with the destination path
    to_do_tracker_name = os.path.join(tracker_path, 'to_do_list.json')

    #complete name with the destination path
    viewed_tracker_name = os.path.join(tracker_path, 'viewed_list.json')

    
    try:
        with open(to_do_tracker_name) as json_file:
             json_to_do_links = json.load(json_file)
        to_do_links = json_to_do_links   
    
    except FileNotFoundError:
        to_do_links = start_to_do_links

    
    try:
        with open(viewed_tracker_name) as json_file:
             json_viewed_links = json.load(json_file)
        viewed_links = json_viewed_links
    
    except FileNotFoundError:
        viewed_links = start_viewed_links
        
    return to_do_links, viewed_links

"""
This function runs the scraper

Runs through the do_do_links, appends for the view_links.
Will scrape and download the necessary files if the page is identified as a recipe page.
"""
def run_the_scraper(to_do_links:list, viewed_links:list, Parser, dir_to_store):
    
    MAX_DELAY_SEC = 10
    
    print_counter = 0

    #specifying the tracker folder path
    tracker_path = os.path.join(dir_to_store, 'tracker')

    #creating the tracker folder if it doesn't already exist
    if os.path.exists(tracker_path) != True:
        os.mkdir(tracker_path)
    
    #complete name with the tracker path
    to_do_tracker_name = os.path.join(tracker_path, 'to_do_list.json')

    #complete name with the tracker path
    viewed_tracker_name = os.path.join(tracker_path, 'viewed_list.json')
    
    """
    If there is not 'DISPLAY' in the environment variables that means we're running inside a container.
    We'll be running a headless browser if we're running inside a container 
    or else we'll be displaying the browser during scraping
    """
    my_options = Options()
    if os.getenv('DISPLAY') is None:
        my_options.headless = True
        print("we're going headless!")
    else:
        my_options.headless = False
        print("we're normal")
    
    #to open up the firefox browser only once
    driver = webdriver.Firefox()
    
    #while to_do_links is not empty
    while to_do_links:
        
        #this pop operator means we're removing the 1st task from the stack
        i_link = to_do_links.pop()
        
        #this extracts the domain name from any link
        if 'https://'+ urllib.parse.urlsplit(i_link).netloc != Parser.domain_name:
        
            continue
        
        #printing progress every 10 times
        if (print_counter == 10):
            print(i_link, 
                  'to_do_links:',len(to_do_links), 
                  'viewed_links:',len(viewed_links)
                 )
            print_counter = 0
        
        print_counter += 1
         
        #grabbing the soup_page
        soup_page = generate_soup_page(i_link, driver, to_do_links, viewed_links)

        #add a random delay before grabbing the next page
        time.sleep(MAX_DELAY_SEC * random.random())
        
        #appending todo and viewed lists
        append_todo_and_viewed(soup_page, viewed_links, to_do_links, Parser)
        
        #saving the progress to json file
        with open(to_do_tracker_name, 'w') as f:
            json.dump(to_do_links, f)
        
        with open(viewed_tracker_name, 'w') as f:
            json.dump(viewed_links, f)
        
        #if the page is a recipe page, then we will scrape and download the required files
        try:
            Parser.execute_if_recipe_page(soup_page, i_link, dir_to_store)
        except NotRecipe:
            continue
        except FileExistsError:
            continue
        except UnicodeEncodeError:
            continue
        except NoServingSize:
            continue

def run_scraper_on_repeat(run_the_scraper, to_do_links, viewed_links, Parser, dir_to_store):
    
    need_to_repeat = 100
    while need_to_repeat > 0:
        try:
            page = run_the_scraper(to_do_links, viewed_links, Parser, dir_to_store)
        except HTTPError:
            need_to_repeat -= 1
            time.sleep(30)
            if need_to_repeat == 0:
                raise
        else:
            need_to_repeat = 0

"""
Creating log file in new folder
"""
def run_log_file(Parser, dir_to_store):
    
    #specifying the logger folder path
    logger_path = os.path.join(dir_to_store, 'logger')

    #creating the tracker folder if it doesn't already exist
    if os.path.exists(logger_path) != True:
        os.mkdir(logger_path)

    #complete name with the logger path
    log_file_name = 'scraper.log'
    complete_logger_name = os.path.join(logger_path, log_file_name)    
        
    #creating/ appending the log file
    if os.path.isfile(complete_logger_name) == False:
        
    #use this line when logging for the 1st time
        logging.basicConfig(filename=log_file_name,level=logging.DEBUG)

    #continue logging where I left off
    #https://stackoverflow.com/questions/41764941/python-logging-create-log-if-not-exists-or-open-and-continue-logging-if-it-does
    else:
        logging.FileHandler(filename=log_file_name, mode='a', encoding=None, delay=False)
        logging.debug('msg')
        logging.info('msg')
        logging.warning('msg')