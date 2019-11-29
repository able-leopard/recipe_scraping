import sys

from my_imports import *
from core_scraping_code import *

# from BBC_SiteSpecificCode import BBCParser
# from BonAppetit_SiteSpecificCode import BonAppetitParser
# from ChowHound_SiteSpecificCode import ChowHoundParser
# from Cooks_SiteSpecificCode import CooksParser
# from CookStr_SiteSpecificCode import CookStrParser
# from Epicurious_SiteSpecificCode import EpicuriousParser
from FoodNetwork_SiteSpecificCode import FoodNetworkParser
# from GeniusKitchen_SiteSpecificCode import GeniusKitchenParser
# from MyFoodAndFamily_SiteSpecificCode import MyFoodAndFamilyParser
# from SeriousEats_SiteSpecificCode import SeriousEatsParser
# from Taste_SiteSpecificCode import TasteParser
# from TheKitchn_SiteSpecificCode import TheKitchnParser


all_parsers = [
            #    BBCParser,
            #    BonAppetitParser, 
            #    ChowHoundParser,
            #    CooksParser,
            #    CookStrParser,
            #    EpicuriousParser,
               FoodNetworkParser,
            #    GeniusKitchenParser,
            #    MyFoodAndFamilyParser,
            #    SeriousEatsParser,
            #    TasteParser,
            #    TheKitchnParser
               ]

#command line arguments to be passed in
site_to_parse = sys.argv[1]
dir_to_store = sys.argv[2]

#code needed to run the scraper
if not os.path.isdir(dir_to_store):
   print('That`s not a real directory')

for cls in all_parsers:
    if cls.site_name == site_to_parse:
        start_to_do_links = cls.start_to_do_links
        start_viewed_links = cls.start_viewed_links
        to_do_links, viewed_links = load_links(start_to_do_links, start_viewed_links, cls, dir_to_store)
        run_scraper_on_repeat(run_the_scraper, to_do_links, viewed_links, cls, dir_to_store)
        break
else:
    print('Sorry bro, but I don`t have a site with such name')