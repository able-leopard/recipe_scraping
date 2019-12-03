# recipe_scraping

A web crawler that is able to scrape over 10 recipe websites for over 200,000 recipes.

Each recipe saves
- Recipe title
- Serving size
- Ingredients
- Cooking instructions
- Photo if available

**To set up virtual environment and run scraper**

```
git clone https://github.com/able-leopard/recipe_scraping.git
```
```
pip install requirements.txt
```
```
cd core_code
run.py sys.argv[1] sys.argv[2]
```
- sys.argv[1] is the site you want to parse
- sys.argv[2] is the directory that you want to store your recipes in.

**To run scraper directly on Docker**
```
git clone https://github.com/able-leopard/recipe_scraping.git
```
```
sudo docker build -t scraping_recipes .
```
- This is the build the docker image
- “scraping_recipes” is the name

```
sudo docker run -it scraping_recipes
```
- for creating a container and terminal in the container

```
python -m core_code.run sys.argv[1] sys.argv[2]
```
- to run the actual file



**Remember to add Geckodriver in your PATH (Need this to run Selenium)**

I used Ubuntu and this linked was able to help me:
- https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu
Here is a good article for Mac:
- https://medium.com/dropout-analytics/selenium-and-geckodriver-on-mac-b411dbfe61bc

**Snippet Demo**

![](recipe_scraping_GIF_downsized_large.gif)

Extended video demo here: https://www.youtube.com/watch?v=2sBrkzGQQlU&feature=youtu.be
