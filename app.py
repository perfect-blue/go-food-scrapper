# -*- coding: utf-8 -*-
"""
Created on Sat Dec 6 00:47:45 2020

@author: Muhammad Ravi
"""

#Web scrapping Library
import requests
import pandas as pd
import regex as re
from bs4 import BeautifulSoup

#Flask Library
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
s = requests.Session()

class RestaurantList(Resource):
      def get(self,place):
          page=1
          session_response=s.get(f"https://gofood.co.id/{place}/restaurants?page={page}")
          soup = BeautifulSoup(session_response.text, 'html.parser')
          
          #get IDs
          article_tags=soup.find_all(name="a", class_="jsx-2918202441")
          ids = [re.search(".{8}-.{4}-.{4}-.{4}-.{12}",tag.get("href")).group() for tag in article_tags]
          
          #names
          name_tags = soup.find_all(name="h3", class_="jsx-329069638 m-0 font-maison-bold")
          names=[name.getText() for name in name_tags]
          
          result={'Location':place,'restaurants':[{"id":ids[i], "name":names[i]} for i in range(len(names))]}
          return result


api.add_resource(RestaurantList, '/restaurants/<string:place>')

app.run(port=5000)          
          
