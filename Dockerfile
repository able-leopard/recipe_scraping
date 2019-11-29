FROM python:3

# Installing all the libaries
RUN mkdir /code

#have to fix this later, put this folder inside the code folder
RUN mkdir /code/scraping_results 
WORKDIR /code

# Installing necessary python package
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /code/

#this makes sure its installing python3 and pip3
RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install -r requirements.txt

#Copy the rest of the code and folders
#make sure to copy only the code here
#space seperates the copied files
COPY src geckodriver /code/

#just using this as entry point
ENTRYPOINT ["/bin/bash"]

# CMD ["/Bon_Appetit/code/recipe_scraping_Bon_Appetit_v1.ipynb"]
ENV PYTHONPATH=/code
ENV PATH="/code:${PATH}"

EXPOSE 8888
