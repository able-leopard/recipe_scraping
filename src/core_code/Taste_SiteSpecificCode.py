import sys

from .my_imports import *
from .core_scraping_code import *

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

class TasteParser:
    
    domain_name = 'https://www.taste.com.au'
    site_name = 'taste.com.au'

    #loading all these into the to_do_links to kick things off
    start_to_do_links = [
                         "https://www.taste.com.au/search-recipes/?q=bake",     #19,000
                         "https://www.taste.com.au/search-recipes/?q=fry",      #14,000
                         "https://www.taste.com.au/search-recipes/?q=boil",     #16,000
                         "https://www.taste.com.au/search-recipes/?q=pan",      #22,000
                         "https://www.taste.com.au/search-recipes/?q=plate",    #12,000
                         "https://www.taste.com.au/search-recipes/?q=dish",      #9,000
                         "https://www.taste.com.au/search-recipes/?q=cook",     #29,000
                         "https://www.taste.com.au/search-recipes/?q=make",     #13,000
                         "https://www.taste.com.au/search-recipes/?q=dinner",   #21,000
                         "https://www.taste.com.au/search-recipes/?q=lunch",    #12,039
                         "https://www.taste.com.au/search-recipes/?q=snack",     #5,000
                         "https://www.taste.com.au/search-recipes/?q=low",      #21,000
                         "https://www.taste.com.au/search-recipes/?q=high",     #22,000
                         "https://www.taste.com.au/search-recipes/?q=vegetable", #7,000
                         "https://www.taste.com.au/search-recipes/?q=chicken",   #7,000
                        ]

    start_viewed_links = []
    
    #Takes in a BeautifulSoup page. Returns a list of sub links in that page.
    @classmethod
    def find_sub_links(cls, soup_page) -> list:
    
        #getting the next page links
        next_page_links = soup_page.select('div.next a')

        #getting all the recipe links
        recipe_links = soup_page.select('div.title a')

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

        all_cooking_info = soup_page.select('ul.recipe-cooking-infos li')
            
        for i in all_cooking_info:
            current_item = i.text
            if 'serving' in current_item.lower():
                servings = current_item.strip()

                
                original_serving_size = "\n" + servings +"\n"
    
                return original_serving_size
    
    #Takes in a BeautifulSoup page. Returns the ingredients.
    @classmethod    
    def get_ingredients(cls, soup_page):
        
        #getting the ingredient text
        result = []
        for i in soup_page.select('div.ingredient-description'):
            current_ingredient = i.text
            result.append(current_ingredient)

        #storing the result as unformatted_ingredients variable    
        original_ingredients = result
        
        #converting list to string and adding extra line in the end
        original_ingredients = '\n'.join(map(str, original_ingredients))+"\n"

        #manually adding header
        original_ingredients = "\n"+"Ingredients: \n"+ original_ingredients
        
        #the first item in the list contains all the ingredients, converting list into str
#         original_ingredients =  result[0]

        return original_ingredients
    
    #Takes in a BeautifulSoup page. Returns the instructions.
    @classmethod
    def get_instructions(cls, soup_page):
        result = []
        for i in soup_page.select('div.recipe-method-step-content'):
            current_instruction = i.text
            result.append(current_instruction)

        #storing the result as unformatted_instructions variable     
        original_instructions = result

        #converting list to string and adding extra line in the end
        original_instructions = ''.join(map(str, original_instructions))+"\n"

        #manually adding header
        original_instructions = "\n"+"Directions"+ original_instructions
        
        return original_instructions

    #Takes in a BeautifulSoup page. Returns the photo link.
    @classmethod
    def get_photo_link(cls, soup_page, link):
        photo = soup_page.select('img.main-icon')
        raw_photo_link = photo[0]['src']
        formatted_photo_link = urljoin(link, raw_photo_link) #getting the full photo link
        
        #checking if the photo link is actually a proper photo link
        file_abb = ['jpeg', 'jpg', 'png']        
        if not any(x in formatted_photo_link for x in file_abb):
            formatted_photo_link = 'not_proper_link'

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

        #special for this website to screen out sites without serving size
        check_serving_size = cls.get_serving_size(soup_page)
        if type(check_serving_size) != str:
                raise NoServingSize("no serving size")

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