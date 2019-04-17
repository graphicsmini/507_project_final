import os
from flask import Flask, render_template, session, redirect, url_for # tools that will make it easier to build on things
from flask_sqlalchemy import SQLAlchemy # handles database stuff for us - need to pip install flask_sqlalchemy in your virtual env, environment, etc to use this and run this
import requests, json
from bs4 import BeautifulSoup
from advanced_expiry_caching import Cache
# import numpy as np
import pandas as pd

######
# Constants
START_URL = "https://www.nps.gov/index.htm"
FILENAME = "nps_cache.json"
PROGRAM_CACHE = Cache(FILENAME)

# assuming constants exist as such
# use a tool to build functionality here
def access_page_data(url):
    data = PROGRAM_CACHE.get(url)
    if not data:
        data = requests.get(url).text
        PROGRAM_CACHE.set(url, data) # default here with the Cache.set tool is that it will expire in 7 days, which is probs fine, but something to explore
    return data

###### Scraping the data from the website

main_page = access_page_data(START_URL)
main_soup = BeautifulSoup(main_page, features="html.parser")
# print(main_soup.prettify())

list_of_topics = main_soup.find('ul', class_='dropdown-menu SearchBar-keywordSearch')
# all_links = list_of_topics.find_all('a')
# print(all_links)

states_urls = []
for link in list_of_topics.find_all('a'):
    # print(link.get('href'))
    states_urls.append("{}{}".format("https://www.nps.gov",link.get('href')))
# print(states_urls)


nps_dic = {} #dictionary of lists

nps_dic['Type'] = []
nps_dic['Name'] = []
nps_dic['Location'] = []
nps_dic['State'] = []
nps_dic['Description'] = []


for url in states_urls:
    state_page = access_page_data(url)
    state_soup = BeautifulSoup(state_page, features="html.parser")
    # print(state_soup.prettify())

    for each_item in state_soup.find("h1", class_="page-title"):
        sitestate = each_item
        # print(sitestate) <--- Check whether it prints out the list of states

    for each_item in state_soup.find("ul", id="list_parks").find_all('li', class_="clearfix"):
        # print('===============')
        # print(each_item)
        # print('===============')

        sitetype = each_item.find('h2')
        sitename = each_item.find('h3').find('a')
        sitelocation = each_item.find('h4')
        sitedescription = each_item.find('p')

        nps_dic['State'].append(sitestate)

        if (sitetype) and (sitetype.text != ""):
            nps_dic['Type'].append(sitetype.text)
        else:
            nps_dic['Type'].append("None")

        if (sitename) and (sitename.text != ""):
            nps_dic['Name'].append(sitename.text)
        else:
            nps_dic['Name'].append("None")

        if (sitelocation) and (sitelocation.text != ""):
            nps_dic['Location'].append(sitelocation.text)
        else:
            nps_dic['Location'].append("None")

        if (sitedescription) and (sitedescription.text != ""):
            nps_dic['Description'].append(sitedescription.text.strip())
        else:
            nps_dic['Description'].append("None")

        # print(nps_dic)

##### Save the scraped data into CSV file.
nps_data = pd.DataFrame.from_dict(nps_dic)
nps_data.to_csv('nps.csv')
# for each in nps_dic.keys():
#     print(len(nps_dic[each]))

###### Now with 'nps.csv' file, I am going to make db file using sqlalchemy.
import sqlite3
import csv
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Float, REAL

sqlite_file = 'nps.sqlite'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor() # Object that allows us to use Python to act on the database

# Often easier to start with the "simplest" table and go on from there

c.execute('''CREATE TABLE State (Id INTEGER PRIMARY KEY AUTOINCREMENT, State TEXT)''')
state_lst = []
with open('nps.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if not row[4] in state_lst:
            state_lst.append(row[4])

# print(state_lst)
c.executemany('INSERT INTO State (State) VALUES (?)', state_lst)
#
# c.execute('''CREATE TABLE Park (Id INTEGER PRIMARY KEY AUTOINCREMENT, ParkName TEXT, ParkType TEXT, ParkLocation TEXT, State TEXT, Description TEXT, CONSTRAINT fk_State FOREIGN KEY (State) REFERENCES State(Id))''')
# # Three quotations make it possible for this to become a multi-line string, which can make it easier to organize and read
# each_lst = []
# with open('nps.csv') as csvfile:
#     readCSV = csv.reader(csvfile, delimiter=',')
#     for row in readCSV:
#         each_lst.append((row[0], row[2], row[1], row[3], row[4], row[5]))
#
# # print(each_lst)
# c.executemany('INSERT INTO Park(ParkName, ParkType, ParkLocation, State, Description) VALUES (?,?,?,?,?)', each_lst)




# ######
# # Application configurations
# app = Flask(__name__)
# app.debug = True
# app.use_reloader = True
# app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'
#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./nps.db' # TODO: decide what your new database name will be -- that has to go here
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
#
# # Set up Flask debug stuff
# db = SQLAlchemy(app) # For database use
# session = db.session # to make queries easy
#
#
# ##### Set up Models #####
#
# class State(db.Model):
#     __tablename__ = "states"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64))
#
#
# class Park(db.Model):
#     __tablename__ = "parks"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64))
#     type = db.Column(db.String(64))
#     location = db.Column(db.String(64))
#     state_id = db.Column(db.Integer, db.ForeignKey("states.id"))
#     description = type = db.Column(db.String(64))
#
#     def __repr__(self):
#         return "{}({}), {}, {}".format(self.name, self.type, self.location, self.decription)
#
