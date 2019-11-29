# recipe_scraping

**To run on virtual environment**

```
pip install requirements.txt
```
```
cd core_code
run.py sys.argv[1] sys.argv[2]
```
sys.argv[1] is the site you want to parse
sys.argv[2] is the directory that you want to store your recipes in.

**To run on Docker**
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



**Remember to add Geckodriver in your PATH (Need this to run Selenium**
I used Ubuntu and this linked was able to help me:
- https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu
Here is a good article for Mac:
- https://medium.com/dropout-analytics/selenium-and-geckodriver-on-mac-b411dbfe61bc
