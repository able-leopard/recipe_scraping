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
class CooksParser:
    
    domain_name = 'https://www.cooks.com'
    site_name = 'cooks.com'
       
    #manually adding all the page links to be fed to the to_do_list:
    start_to_do_links = ["https://www.cooks.com/rec/browse/appetizers/",
                           "https://www.cooks.com/rec/browse/beans/",
                           "https://www.cooks.com/rec/browse/beverages/",
                           "https://www.cooks.com/rec/browse/breads/",
                           "https://www.cooks.com/rec/browse/breakfast/",
                           "https://www.cooks.com/rec/browse/cakes/",
                           "https://www.cooks.com/rec/browse/candies/",
                           "https://www.cooks.com/rec/browse/casseroles/",
                           "https://www.cooks.com/rec/browse/cookies/",
                           "https://www.cooks.com/rec/browse/crockpot/",
                           "https://www.cooks.com/rec/browse/desserts/",
                           "https://www.cooks.com/rec/browse/dips-dressings/",
                           "https://www.cooks.com/rec/browse/eggs/",
                           "https://www.cooks.com/rec/browse/equal/",
                           "https://www.cooks.com/rec/browse/fish/",
                           "https://www.cooks.com/rec/browse/fruit/",
                           "https://www.cooks.com/rec/browse/holiday/",
                           "https://www.cooks.com/rec/browse/international/",
                           "https://www.cooks.com/rec/browse/italian/",
                           "https://www.cooks.com/rec/browse/jams/",
                           "https://www.cooks.com/rec/browse/low-fat/",
                           "https://www.cooks.com/rec/browse/main-dishes/",
                           "https://www.cooks.com/rec/browse/meat-dishes/",
                           "https://www.cooks.com/rec/browse/mens-favorites/",
                           "https://www.cooks.com/rec/browse/mexican/",
                           "https://www.cooks.com/rec/browse/microwave/",
                           "https://www.cooks.com/rec/browse/old-time/",
                           "https://www.cooks.com/rec/browse/outdoor/",
                           "https://www.cooks.com/rec/browse/party/",
                           "https://www.cooks.com/rec/browse/pastas/",
                           "https://www.cooks.com/rec/browse/pickles/",
                           "https://www.cooks.com/rec/browse/pies/",
                           "https://www.cooks.com/rec/browse/potatoes/",
                           "https://www.cooks.com/rec/browse/poultry/",
                           "https://www.cooks.com/rec/browse/puddings/",
                           "https://www.cooks.com/rec/browse/rice/",
                           "https://www.cooks.com/rec/browse/salads/",
                           "https://www.cooks.com/rec/browse/sandwiches/",
                           "https://www.cooks.com/rec/browse/sauces/",
                           "https://www.cooks.com/rec/browse/seafood/",
                           "https://www.cooks.com/rec/browse/side-dishes/",
                           "https://www.cooks.com/rec/browse/snacks/",
                           "https://www.cooks.com/rec/browse/soups/",
                           "https://www.cooks.com/rec/browse/special-occasions/",
                           "https://www.cooks.com/rec/browse/tex-mex/",
                           "https://www.cooks.com/rec/browse/vegetables/",
                           "https://www.cooks.com/rec/review/"
                        ]

    start_viewed_links = []

    #Takes in a BeautifulSoup page. Returns a list of sub links in that page.
    @classmethod
    def find_sub_links(cls, soup_page) -> list:
    
        #getting rid of some tags because it leads to links that wastes time
        for i in soup_page.select('div#breadcrumb'):
            i.decompose()

        for i in soup_page.select('a.option'):
            i.decompose()

        #getting all the recipe links & next page links
        all_links = soup_page.select('div.grid_10 div a.lnk')

        sub_links = []
        for i_link in all_links:
            i_link = i_link['href']
            i_link = urljoin(cls.domain_name, i_link)
            sub_links.append(i_link)

        #removing the duplicates
        sub_links = list(dict.fromkeys(sub_links))

        return sub_links
    
    #Takes in a BeautifulSoup page. Returns the recipe name.
    @classmethod
    def get_recipe_name(cls, soup_page):
        result = []
        for i in soup_page.select('span.fn'):
            result.append(i.text)

        recipe_name = result
        recipe_name = result[0] + "\n"
        
        return recipe_name.title()

    #Takes in a BeautifulSoup page. Returns the serving size.
    #There is no serving size for this site
    @classmethod
    def get_serving_size(cls, soup_page):

        serving_size = soup_page.select('span.recipe__header__servings')
        if serving_size:
            serving_size = serving_size[0].text

            original_serving_size = "\n"+serving_size.capitalize() +"\n"

            return original_serving_size
        else:
            return ""

    #Takes in a BeautifulSoup page. Returns the ingredients.
    @classmethod    
    def get_ingredients(cls, soup_page):
        
        #getting the ingredient text
        result = []
        for i in soup_page.select('span.ingredient'):
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
        for i in soup_page.select('div.instructions'):
            current_instruction = i.text
            result.append(current_instruction)

        #storing the result as unformatted_instructions variable     
        original_instructions = result

        #converting list to string and adding extra line in the end
        original_instructions = '\n'.join(map(str, original_instructions))+"\n"

        #manually adding header
        original_instructions = "\n"+"Directions: \n"+ original_instructions
        
        return original_instructions

    #Takes in a BeautifulSoup page. Returns the photo link.
    @classmethod
    def get_photo_link(cls, soup_page, link):
        
        photo = soup_page.select('img.ba-picture--fit')
        if photo:
            raw_photo_link = photo[0]['srcset']
            raw_photo_link = raw_photo_link.split(' ')[0]

            formatted_photo_link = urljoin(link, raw_photo_link) #getting the full photo link

            #checking if the photo link is actually a proper photo link
            file_abb = ['jpeg', 'jpg', 'png']        
            if not any(x in formatted_photo_link for x in file_abb):
                formatted_photo_link = 'not_proper_link'
            return formatted_photo_link

        else:
            return None
        
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

    #     try:
    #         check_serving_size = cls.get_serving_size(soup_page)
    #     except IndexError as e:
    #         raise NotRecipe("can't find the serving size")

        try:
            check_ingredients = cls.get_ingredients(soup_page)
        except IndexError as e:
            raise NotRecipe("can't find the ingredients")

        try:
            check_instructions = cls.get_instructions(soup_page)
        except IndexError as e:
            raise NotRecipe("can't find the instructions")

    #     try:
    #         check_photo_link = cls.get_photo_link(soup_page, link)
    #     except IndexError as e:
    #         raise NotRecipe("can't find the photo link")

        else:
            save_all_files(soup_page, link, cls, dir_to_store)