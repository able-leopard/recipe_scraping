import sys


from .my_imports import *
from .core_scraping_code import *

"""
Class for parsing 5 things:
1. recipe name
2. serving size
3. ingredients
4. instructions
5. photo link

Anything that is site dependent is written under this class
"""
class BonAppetitParser:
    
    domain_name = 'https://www.bonappetit.com'
    site_name = 'bonappetit.com'
    
    #manually adding all the page links to be fed to the to_do_list:
    base_link = 'https://www.bonappetit.com/search?content=recipe&page='

    start_to_do_links = []

    for i in range(697):
        current_link = base_link + str(i)
        start_to_do_links.append(current_link)

    #ignoring page 0
    start_to_do_links = start_to_do_links[1:]

    start_viewed_links = []
    
    #Takes in a BeautifulSoup page. Returns a list of sub links in that page.
    @classmethod
    def find_sub_links(cls, soup_page) -> list:
    
        #getting all the recipe links
        recipe_links = soup_page.select('h4.hed a')

        sub_links = []
        for i_link in recipe_links:
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
        for i in soup_page.select('h1'):
            result.append(i.text)

        recipe_name = result
        recipe_name = result[0] + "\n"
        
        return recipe_name

    #Takes in a BeautifulSoup page. Returns the serving size.
    @classmethod
    def get_serving_size(cls, soup_page):

        serving_size = soup_page.select('span.recipe__header__servings')
        serving_size = serving_size[0].text
       
        original_serving_size = "\n"+serving_size.capitalize() +"\n"
    
        return original_serving_size
    
    #Takes in a BeautifulSoup page. Returns the ingredients.
    @classmethod    
    def get_ingredients(cls, soup_page):
        
        #getting the ingredient text
        result = []
        for i in soup_page.select('h3.ingredients__group__header, ul.ingredients__group li div.ingredients__text'):
            current_ingredient = i.text
            result.append(current_ingredient)

        #storing the result as unformatted_ingredients variable    
        original_ingredients = result
        
        #converting list to string and adding extra line in the end
        original_ingredients = '\n'.join(map(str, original_ingredients))+"\n"

        #manually adding header
        original_ingredients = "\n"+"Ingredients"+ original_ingredients
        
        #the first item in the list contains all the ingredients, converting list into str
#         original_ingredients =  result[0]

        return original_ingredients
    
    #Takes in a BeautifulSoup page. Returns the instructions.
    @classmethod
    def get_instructions(cls, soup_page):
        result = []
        for i in soup_page.select('h4.subhed, li.step div p'):
            current_instruction = i.text
            result.append(current_instruction)

        #storing the result as unformatted_instructions variable     
        original_instructions = result

        #converting list to string and adding extra line in the end
        original_instructions = '\n'.join(map(str, original_instructions))+"\n"

        #manually adding header
        original_instructions = "\n"+"Directions \n"+ original_instructions
        
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

    #     try:
    #         check_photo_link = cls.get_photo_link(soup_page, link)
    #     except IndexError as e:
    #         raise NotRecipe("can't find the photo link")

        else:
            save_all_files(soup_page, link, cls, dir_to_store)
