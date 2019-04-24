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

sqlite_file = 'nps.db'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor() # Object that allows us to use Python to act on the database

# Often easier to start with the "simplest" table and go on from there
c.execute('''DROP TABLE IF EXISTS 'State';''')
c.execute('''CREATE TABLE State (StateId INTEGER PRIMARY KEY AUTOINCREMENT, State TEXT)''')
state_lst = []

with open('nps.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if not row[4] in state_lst:
            state_lst.append(row[4])
        state_lst_itself = state_lst[1:]

# print(state_lst_itself)
c.executemany('INSERT INTO State (State) VALUES(?)', zip(state_lst_itself))

c.execute('''DROP TABLE IF EXISTS 'Park';''')
c.execute('''CREATE TABLE Park (ParkId INTEGER PRIMARY KEY AUTOINCREMENT, ParkName TEXT, ParkType TEXT, ParkLocation TEXT, StateId INTEGER, Description TEXT, CONSTRAINT fk_States FOREIGN KEY (StateId) REFERENCES State(StateId))''')
# Three quotations make it possible for this to become a multi-line string, which can make it easier to organize and read
each_lst = []
with open('nps.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    readCSV.__next__()

    for row in readCSV:
        state_name = (row[4],)
        # print(type(state_name))
        c.execute("SELECT StateId FROM State WHERE State.State = ?" , state_name)
        fetch_state_name = c.fetchone()

        state_id = int(fetch_state_name[0])
        # print(fetch_state_name)
        each_lst.append((row[2], row[1], row[3], state_id, row[5]))

# print(each_lst)
c.executemany('INSERT INTO Park(ParkName, ParkType, ParkLocation, StateId, Description) VALUES (?,?,?,?,?)', each_lst)

conn.commit()
conn.close()



######
# Application configurations
from flask import Flask, render_template, session, redirect, url_for, g
app = Flask(__name__)

DATABASE = 'nps.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


##### Set up Controllers (route functions) #####

## Main route
@app.route('/')
def index():

    cur = get_db().cursor()
    cur.execute("select * from Park")
    rows = cur.fetchall()

    park_num = len(rows)

    return render_template('index.html', park_num = park_num)

@app.route('/all_states')
def all_states():

    cur = get_db().cursor()
    cur.execute("select * from State")
    rows = cur.fetchall()

    state_list = []
    for each in rows:
        state_name = each[1]
        state_list.append(state_name)

    return render_template('all_states.html', state_name = state_name, state_list = state_list)

@app.route('/state/<state>')
def each_state(state):

    cur = get_db().cursor()
    cur.execute("select State, ParkName, ParkType, ParkLocation, Description from Park natural inner join State")
    parks = cur.fetchall() # It will be rows of pakrs in the certain state. It could be one or multiple locations.

    # print(parks)
    park_dic = {}
    park_dic["park_lst"]=[]

    for each_park in parks:
        if each_park[0] == state:
            park_dic["park_lst"].append(each_park[1:])

    return render_template('each_state.html', state_name=state, park_lst=park_dic["park_lst"])


if __name__ == '__main__':
   app.run()
