import sys

from my_imports import *
from core_scraping_code import *

"""
***SITE SPECIFIC CODE***
This code does 7 things:

1. recipe name <-- parse on a recipe page
2. serving size <-- parse on a recipe page
3. ingredients <-- parse on a recipe page
4. instructions <-- parse on a recipe page
5. photo link <-- parse on a recipe page

6. Extracts sublinks (mainly next page links and recipe pages)
7. execute_if_recipe_page to filter to scrape only recipe pages
"""
class FoodNetworkParser:
    
    domain_name = 'https://www.foodnetwork.ca'
    site_name = 'foodnetwork.ca'

    #loading all these into the to_do_links to kick things off
    start_to_do_links = ["https://www.foodnetwork.ca/search/?q=Fish&did=4294967287&pn=1",
                           "https://www.foodnetwork.ca/search/?q=healthy&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=food&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=mexican&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=chinese&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=vegan&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=dinner&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=lunch&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=Brunch&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=breakfast&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=snack&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=quick&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=cook&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=kitchen&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=salad&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=dish&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=dessert&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=recipe&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=fish&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=chicken&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=pork&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=beef&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=green&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=bean&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=delicious&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=seafood&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=bake&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=Vegetables&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=fruit&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=Nuts&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=North%20American&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=Main&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=Potatoes&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=rice&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=pasta&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=grain&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=bbq&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=Eggs/Dairy&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=Cheese&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=Italian&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=asian&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=canadian&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=north&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=indian&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=Turkey&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=soup&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=side&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=sweet&did=4294967287",
                           "https://www.foodnetwork.ca/search/?q=appetizer&did=4294967287"              
                  ]

    start_viewed_links = []
    
    #Takes in a BeautifulSoup page. Returns a list of sub links in that page.
    @classmethod
    def find_sub_links(cls, soup_page) -> list:
    
        #getting the next page links
        next_page_links = soup_page.select('section.searchResults a.page-link')

        #getting all the recipe links
        recipe_links = soup_page.select('section.searchResults a.searchResultsEntry-titleLink')

        #combining them together
        all_links = next_page_links + recipe_links

        sub_links = []
        for i_link in all_links:
            i_link = i_link['href']
            i_link = urljoin(cls.domain_name, i_link)
            sub_links.append(i_link)

        return sub_links

    #Takes in a BeautifulSoup page. Returns the recipe name.
    @classmethod
    def get_recipe_name(cls, soup_page):
        result = []
        for i in soup_page.select('h1'):
            result.append(i.text)

        recipe_name = result
        recipe_name = result[0] + "\n"
        
        return recipe_name

    #Takes in a BeautifulSoup page. Returns the serving size.
    @classmethod
    def get_serving_size(cls, soup_page):
        serving_label = []
        for i in soup_page.select('span.recipeDetails-infoLabel'):
            current_label = i.text
            serving_label.append(current_label)

        serving_size = []  
        for i in soup_page.select('span.recipeDetails-infoValueWrapper'):
            current_value = i.text
            serving_size.append(current_value)

        original_serving_size = [serving_label, serving_size]
        original_serving_size = "\n"+ serving_label[-1].capitalize() + " " + serving_size[-1] +"\n"
        
        return original_serving_size
    
    #Takes in a BeautifulSoup page. Returns the ingredients.
    @classmethod    
    def get_ingredients(cls, soup_page):
        result = []
        for i in soup_page.select('section.recipe-ingredients'):
            current_ingredient = i.text
            result.append(current_ingredient)

        #storing the result as unformatted_ingredients variable    
        original_ingredients = result

        #the first item in the list contains all the ingredients, converting list into str
        original_ingredients =  result[0]

        return original_ingredients
    
    #Takes in a BeautifulSoup page. Returns the instructions.
    @classmethod
    def get_instructions(cls, soup_page):
        result = []
        for i in soup_page.select('section.recipeInstructions, section.recipeDescriptionText'):
            current_instruction = i.text
            result.append(current_instruction)

        #storing the result as unformatted_instructions variable     
        original_instructions = result

        #the first item in the list contains the whole instructions, converting the list into str
#         original_instructions =  result[0]

        return original_instructions[0]

    #Takes in a BeautifulSoup page. Returns the photo link.
    @classmethod
    def get_photo_link(cls, soup_page, link):
        photo = soup_page.select('img.recipe-photo')
        raw_photo_link = photo[0]['src']
        formatted_photo_link = urljoin(link, raw_photo_link) #getting the full photo link
        
        return formatted_photo_link  
    
    """
    Takes in a BeautifulSoup page and link.
    Checks of the BeautifulSoup page has the follow five criterias:
        1. Recipe Name
        2. Serving Size
        3. Ingredients
        4. Instructions
        5. Photo Link

    If all of the above criterias are satisfied, then the save_all_files function
    is executed to download and save the json, txt, and img files.

    If 1 or more criterias are not satisfied, the the save_all_files function will
    not be executed.
    """
    @classmethod
    def execute_if_recipe_page(cls, soup_page, link, dir_to_store):

        try:
            check_recipe_name = cls.get_recipe_name(soup_page)
        except IndexError as e:
            raise NotRecipe("can't find the name of the recipe")

        try:
            check_serving_size = cls.get_serving_size(soup_page)
        except IndexError as e:
            raise NotRecipe("can't find the serving size")

        try:
            check_ingredients = cls.get_ingredients(soup_page)
        except IndexError as e:
            raise NotRecipe("can't find the ingredients")

        try:
            check_instructions = cls.get_instructions(soup_page)
        except IndexError as e:
            raise NotRecipe("can't find the instructions")

        try:
            check_photo_link = cls.get_photo_link(soup_page, link)
        except IndexError as e:
            raise NotRecipe("can't find the photo link")

        else:
            save_all_files(soup_page, link, cls, dir_to_store)